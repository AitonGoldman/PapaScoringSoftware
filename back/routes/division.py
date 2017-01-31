from blueprints import admin_login_blueprint,admin_manage_blueprint
from flask import jsonify,current_app,request
import json
from werkzeug.exceptions import BadRequest,Conflict
from util import db_util
from util.permissions import Admin_permission,Scorekeeper_permission
from flask_login import login_required,current_user
from routes.utils import fetch_entity,check_player_team_can_start_game,set_token_start_time,remove_player_from_queue,get_valid_sku,get_queue_from_division_machine,send_push_notification,get_player_list_to_notify
from orm_creation import create_division, create_division_machine
import datetime
from sqlalchemy import and_,or_
import random


@admin_manage_blueprint.route('/division',methods=['GET'])
def route_get_divisions():
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)            
    divisions = {division.division_id:division.to_dict_simple() for division in tables.Division.query.all()}
    #FIXME : this is a hack, and should be fixed
    divisions['metadivisions'] = {metadivision.meta_division_id:metadivision.to_dict_simple() for metadivision in tables.MetaDivision.query.all()}
    return jsonify({'data': divisions})

@admin_manage_blueprint.route('/division/<division_id>',methods=['GET'])
def route_get_division(division_id):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)            
    return jsonify({'data': tables.Division.query.filter_by(division_id=division_id).first().to_dict_simple()})

@admin_manage_blueprint.route('/division/<division_id>/division_machine',methods=['GET'])
def route_get_division_machines(division_id):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    division_machines = tables.DivisionMachine.query.filter_by(division_id=division_id).all()
    return jsonify({'data': {division_machine.division_machine_id:division_machine.to_dict_simple() for division_machine in division_machines}})

@admin_manage_blueprint.route('/division/<division_id>/division_machine/<division_machine_id>/play_time_avg',methods=['GET'])
def route_get_division_machines_avg_playtime(division_id,division_machine_id):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    if division_machine_id == "0":
        if division_id == "0":
            division_machines = tables.DivisionMachine.query.all()        
        else:            
            division_machines = tables.DivisionMachine.query.filter_by(division_id=division_id).all()        
    else:            
        division_machines = [fetch_entity(tables.DivisionMachine,division_machine_id)]    
    #audit_logs = tables.AuditLog.query.filter_by(division_machine_id=division_machine_id).all()
    division_machine_ids = [division_machine.division_machine_id for division_machine in division_machines]            
    audit_logs = tables.AuditLog.query.filter(and_(tables.AuditLog.division_machine_id.in_(division_machine_ids),
                                                   or_(tables.AuditLog.action == "Game Started",
                                                       tables.AuditLog.action == "Score Added"))).order_by(tables.AuditLog.audit_log_id).all()
    #audit_logs = tables.AuditLog.query.filter(tables.AuditLog.division_machine_id.in_(division_machine_ids)).order_by(tables.AuditLog.audit_log_id).all()
    
    start_times = {}
    end_times = {}
    #start_time = None
    #end_time = None
    #avg_times = []
    avg_times = {}
    cur_action = None
    for audit_log in audit_logs:
        if cur_action == audit_log.action:
            continue
        cur_action = audit_log.action        
        if audit_log.action == "Game Started":
            start_times[audit_log.division_machine_id] = audit_log.action_date
            end_times[audit_log.division_machine_id] = None
        if audit_log.action == "Score Added" or audit_log.action == "Score Voided":
            end_times[audit_log.division_machine_id] = audit_log.action_date
        #if audit_log.voided_date and audit_log.action != "jagoff":
        #    end_time = audit_log.voided_date
        if audit_log.division_machine_id in end_times and end_times[audit_log.division_machine_id]:
            if audit_log.division_machine_id in start_times:                
                #if end_times[audit_log.division_machine_id] is None or start_times[audit_log.division_machine_id] is None:
                #    continue
                time_delta = end_times[audit_log.division_machine_id] - start_times[audit_log.division_machine_id]
                if audit_log.division_machine_id not in avg_times:
                    avg_times[audit_log.division_machine_id]=[]
                avg_times[audit_log.division_machine_id].append(time_delta.total_seconds())
                start_times[audit_log.division_machine_id]=None
                end_times[audit_log.division_machine_id]=None
                
    for avg_time_division_machine_id,machine_times in avg_times.iteritems():                
        total_time = 0
        avg_game_time = 0        
        total_time = sum(machine_times)        
        avg_game_time = total_time/len(machine_times)    
        division_machine = tables.DivisionMachine.query.filter_by(division_machine_id=avg_time_division_machine_id).first()
        division_machine.avg_play_time = datetime.datetime.fromtimestamp(avg_game_time).strftime('%M min')        
        #print datetime.datetime.fromtimestamp(avg_game_time).strftime('%M:%S')
        #return jsonify({'data': {division_machine.division_machine_id:division_machine.to_dict_simple() for division_machine in division_machines}})
    db.session.commit()        
    return jsonify({})


@admin_manage_blueprint.route('/division_machine',methods=['GET'])
def route_get_all_division_machines():
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    division_machines = tables.DivisionMachine.query.all()
    return jsonify({'data': {division_machine.division_machine_id:division_machine.to_dict_simple() for division_machine in division_machines}})


@admin_manage_blueprint.route('/division/<division_id>/division_machine/<division_machine_id>',methods=['GET'])
def route_get_division_machine(division_id,division_machine_id):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    division_machine = fetch_entity(tables.DivisionMachine,division_machine_id)
    return jsonify({'data': division_machine.to_dict_simple()})

@admin_manage_blueprint.route('/division/<division_id>/division_machine',methods=['POST'])
@login_required
@Admin_permission.require(403)
def route_add_division_machine(division_id):        
    machine_data = json.loads(request.data)
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)                
    division = fetch_entity(tables.Division,division_id)    
    # FIXME : need to load machines as part of init
    if 'machine_id' in machine_data:                
        machine = fetch_entity(tables.Machine,int(machine_data['machine_id']))
        
    else:        
        BadRequest('no machine_id specified')
    new_division_machine = create_division_machine(current_app,machine,division)
    return jsonify({'data':new_division_machine.to_dict_simple()})

@admin_manage_blueprint.route('/division/<division_id>/division_machine/<division_machine_id>',methods=['DELETE'])
@login_required
@Admin_permission.require(403)
def route_delete_division_machine(division_id,division_machine_id):            
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)                            
    division_machine = fetch_entity(tables.DivisionMachine,division_machine_id)        
    division_machine.removed=True
    tables.db_handle.session.commit()
    return jsonify({'data':division_machine.to_dict_simple()})

@admin_manage_blueprint.route('/division/<division_id>/division_machine/<division_machine_id>/player/<player_id>',
                              methods=['PUT'])
@login_required
@Scorekeeper_permission.require(403)
def route_add_division_machine_player(division_id,division_machine_id,player_id):            
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)                            
    division_machine = fetch_entity(tables.DivisionMachine,division_machine_id)        
    player = fetch_entity(tables.Player,player_id)
    if player.active is False:
        raise Conflict('Player is not active.  Please see the front desk.')        
    if division_machine.player_id or division_machine.team_id:
        raise Conflict('Machine is already being played')
    if check_player_team_can_start_game(current_app,division_machine,player) is False:
        raise BadRequest('Player can not start game - either no tickets or already on another machine')
    if len(player.teams) > 0:
        if tables.DivisionMachine.query.filter_by(team_id=player.teams[0].team_id).first():            
            raise BadRequest('Player can not start game - his team is playing on another machine')        
    set_token_start_time(current_app,player,division_machine,commit=False)    
    division_machine.player_id=player.player_id
    ##db.session.commit()
    queue = tables.Queue.query.filter_by(player_id=player.player_id).first()
    players_to_alert = []
    if queue:
        players_to_alert = get_player_list_to_notify(player.player_id,queue.division_machine)            
    removed_queue = remove_player_from_queue(current_app,player,commit=True)
    
    if removed_queue is not None and removed_queue is not False and len(players_to_alert) > 0:                
        push_notification_message = "The queue for %s has changed!  Please check the queue to see your new position." % queue.division_machine.machine.machine_name
        send_push_notification(push_notification_message, players=players_to_alert)
    db.session.commit()
    return jsonify({'data':division_machine.to_dict_simple()})

@admin_manage_blueprint.route('/division/<division_id>/division_machine/<division_machine_id>/undo',
                              methods=['PUT'])
@login_required
@Scorekeeper_permission.require(403)
def route_undo_division_machine_player_team(division_id,division_machine_id):            
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)                            
    division_machine = fetch_entity(tables.DivisionMachine,division_machine_id)
    if division_machine.division.team_tournament is False and division_machine.player_id is None:
        raise Conflict('Machine is not being played')
    if division_machine.division.team_tournament and division_machine.team_id is None:
        raise Conflict('Machine is not being played')    
    token = tables.Token.query.filter_by(player_id=division_machine.player_id,division_machine_id=division_machine_id,used=False).first()
    token.division_machine_id=None
    division_machine.player_id=None
    db.session.commit()    
    return jsonify({'data':division_machine.to_dict_simple()})

@admin_manage_blueprint.route('/division_machine/<int:division_machine_id>/player/<player_id>',
                              methods=['DELETE'])
@login_required
@Scorekeeper_permission.require(403)
def route_remove_division_machine_player(division_machine_id,player_id):            
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)                            
    division_machine = fetch_entity(tables.DivisionMachine,division_machine_id)            
    if division_machine.player_id is None:
        raise BadRequest('No player playing on this machine!')
    if division_machine.player_id != int(player_id):
        raise BadRequest('Player is not playing on this machine!')

    division_machine.player_id=None
    tables.db_handle.session.commit()
    return jsonify({'data':division_machine.to_dict_simple()})

@admin_manage_blueprint.route('/division',methods=['POST'])
@login_required
@Admin_permission.require(403)
def route_add_division():
    division_data = json.loads(request.data)
    if 'division_name' not in division_data or division_data['division_name'] is None or division_data['division_name'] == "":        
        raise BadRequest('division_name not found in post data')
    if 'tournament_id' not in division_data:
        raise BadRequest('tournament_id not found in division_data')
    if 'scoring_type' not in division_data:        
        raise BadRequest('did not specify scoring type')            
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)    
    if tables.Division.query.filter_by(division_name=division_data['division_name'],tournament_id=division_data['tournament_id']).first():
        raise Conflict('You are trying to create a duplicate tournament')
    
    new_division = create_division(current_app,division_data)
    return jsonify({'data':new_division.to_dict_simple()})


@admin_manage_blueprint.route('/division/<division_id>',methods=['PUT'])
@login_required
@Admin_permission.require(403)
def route_edit_division(division_id):    
    division_data = json.loads(request.data)
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    
    division = fetch_entity(tables.Division,division_id)
    if 'division_id' not in division_data:        
        raise BadRequest('No DivisionId specified')
    # FIXME : need to deal with single division vs multiple division name editing (i.e. tournament_name is calculated)
    #if 'division_name' in division_data and division.division_name != division_data['division_name']:
    #    dup_division = tables.Division.query.filter_by(division_name=division_data['division_name'],tournament_id=division.tournament_id).first()
    #    if dup_division:
    #        raise Conflict('You are trying to create a duplicate division')
    #    division.division_name=division_data['division_name']
    if 'active' in division_data:
        if  division_data['active'] == True:
            division.active = True
        else:
            division.active = False    
    if 'finals_num_qualifiers' in division_data:
        division.finals_num_qualifiers = division_data['finals_num_qualifiers']    
    if 'team_tournament' in division_data:
        division.team_tournament = division_data['team_tournament']
    if 'queuing' in division_data:
        division.queuing=division_data['queuing']
    if 'use_stripe' in division_data:
        if division_data['use_stripe'] is True:            
            division.use_stripe=True
            if 'stripe_sku' in division_data:
                if get_valid_sku(division_data['stripe_sku'],current_app.td_config['STRIPE_API_KEY'])['sku'] is None:
                    raise BadRequest('Invalid sku specified')
                division.stripe_sku = division_data['stripe_sku']
            else:
                raise BadRequest('Specified use_stripe, but no sku specified')
        else:
            division.use_stripe=False
            if 'local_price' in division_data:                            
                division.local_price = division_data['local_price']
            else:
                raise BadRequest('use_stripe is false, but no local price specified')
    if 'finals_player_selection_type' in division_data:
        division.finals_player_selection_type=division_data['finals_player_selection_type']
    if 'finals_num_qualifiers_ppo_a' in division_data:
        division.finals_num_qualifiers_ppo_a=division_data['finals_num_qualifiers_ppo_a']
    if 'finals_num_qualifiers_ppo_b' in division_data:
        division.finals_num_qualifiers_ppo_b=division_data['finals_num_qualifiers_ppo_b']
    if 'ifpa_range_start' in division_data:
        division.ifpa_range_start=division_data['ifpa_range_start']
    if 'ifpa_range_end' in division_data:
        division.ifpa_range_end=division_data['ifpa_range_end']
    if 'ppo_a_ifpa_range_end' in division_data:
        division.ppo_a_ifpa_range_end=division_data['ppo_a_ifpa_range_end']
    if 'discount_ticket_count' in division_data:
        division.discount_ticket_count=division_data['discount_ticket_count']
    if 'discount_ticket_price' in division_data:
        division.discount_ticket_price=division_data['discount_ticket_price']
    if 'discount_stripe_sku' in division_data:
        division.discount_stripe_sku=division_data['discount_stripe_sku']
    if 'number_of_relevant_scores' in division_data:
        division.number_of_relevant_scores=division_data['number_of_relevant_scores']
        
    db.session.commit()
    return jsonify({'data':division.to_dict_simple()})
            
@admin_manage_blueprint.route('/division/<division_id>/division_machine/<division_machine_id>/team/<team_id>',
                              methods=['PUT'])
@login_required
@Scorekeeper_permission.require(403)
def route_add_division_machine_team(division_id,division_machine_id,team_id):            
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)                            
    division_machine = fetch_entity(tables.DivisionMachine,division_machine_id)        
    team = fetch_entity(tables.Team,team_id)
    if division_machine.team_id or division_machine.player_id:
        raise Conflict('The machine is already being played')
    if check_player_team_can_start_game(current_app,division_machine,team=team) is False:
        raise BadRequest('Player can not start game - either no tickets or already on another machine')    
    if tables.DivisionMachine.query.filter_by(player_id=team.players[0].player_id).first() or tables.DivisionMachine.query.filter_by(player_id=team.players[1].player_id).first():            
        raise BadRequest('Team can not start game - one player is playing on another machine')            
    set_token_start_time(current_app,None,division_machine,team_id=team_id)    
    division_machine.team_id=team.team_id
    tables.db_handle.session.commit()
    players_to_alert = []
    removed_queues = []
    for player in team.players:
        queue = tables.Queue.query.filter_by(player_id=player.player_id).first()        
        if queue:
            players_to_alert = players_to_alert + get_player_list_to_notify(player.player_id,queue.division_machine)            
        removed_queue = remove_player_from_queue(current_app,player,commit=True)
        removed_queues.append(removed_queue)
        db.session.commit()
    if all(item is not None and item is not False for item in removed_queues) and len(players_to_alert) > 0:    
        push_notification_message = "The queue for %s has changed!  Please check the queue to see your new position." % queue.division_machine.machine.machine_name
        send_push_notification(push_notification_message, players=players_to_alert)
        
    return jsonify({'data':division_machine.to_dict_simple()})

@admin_manage_blueprint.route('/division/<division_id>/division_machine/<int:division_machine_id>/team',
                              methods=['DELETE'])
@login_required
@Scorekeeper_permission.require(403)
def route_remove_division_machine_team(division_id,division_machine_id):            
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)                            
    division_machine = fetch_entity(tables.DivisionMachine,division_machine_id)            
    if division_machine.team_id is None:
        raise BadRequest('No team playing on this machine')
    division_machine.team_id=None
    tables.db_handle.session.commit()
    return jsonify({'data':division_machine.to_dict_simple()})

