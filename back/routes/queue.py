from blueprints import admin_login_blueprint,admin_manage_blueprint
from flask import jsonify,current_app,request
import json
from werkzeug.exceptions import BadRequest,Conflict
from util import db_util
from util.permissions import Admin_permission, Desk_permission, Token_permission, Queue_permission
from flask_login import login_required,current_user
from routes.utils import fetch_entity,check_player_team_can_start_game,set_token_start_time, remove_player_from_queue,get_queue_from_division_machine,send_push_notification,get_player_list_to_notify,check_player_in_queue
import os
from flask_restless.helpers import to_dict
from orm_creation import create_queue
from audit_log_utils import create_audit_log
import datetime

@admin_manage_blueprint.route('/queue/player_id/<player_id>',methods=['GET'])
def get_queue_for_player(player_id):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    player = fetch_entity(tables.Player, player_id)
    queue = tables.Queue.query.filter_by(player_id=player_id).first()
    if queue:
        return jsonify({'data':queue.to_dict_simple()})
    else:
        return jsonify({'data':None})

@admin_manage_blueprint.route('/queue/division/<division_id>',methods=['GET'])
def get_queues(division_id):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    division_machines = tables.DivisionMachine.query.filter_by(division_id=division_id,removed=False)
    queues = {}
    machine_players = {}
    for division_machine in division_machines:
        queues[division_machine.division_machine_id]={
            'division_machine_name':"%s"%division_machine.machine.machine_name,
            'division_machine_id':division_machine.division_machine_id,
            'removed':division_machine.removed,
            'division_id':division_machine.division_id,
            'player_id':division_machine.player_id,
            'team_id':division_machine.team_id,
            'avg_play_time':division_machine.avg_play_time,
            'queues':get_queue_from_division_machine(division_machine,json_output=True)
        }
        if division_machine.player is None and division_machine.division.team_tournament is not True:
            machine_players[division_machine.division_machine_id]=None
        if division_machine.player is not None and division_machine.division.team_tournament is not True:
            machine_players[division_machine.division_machine_id]="%s %s" %(division_machine.player.first_name,division_machine.player.last_name)
        if division_machine.team and division_machine.team and division_machine.division.team_tournament is True:
            machine_players[division_machine.division_machine_id]=None
        if division_machine.team and division_machine.team and division_machine.division.team_tournament is True:
            machine_players[division_machine.division_machine_id]=division_machine.team.team_name
        
    return jsonify({'data':queues,'machine_players':machine_players})


@admin_manage_blueprint.route('/queue',methods=['POST'])
@login_required
@Queue_permission.require(403)
def add_player_to_queue():    
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    queue_data = json.loads(request.data)
    division_machine = fetch_entity(tables.DivisionMachine, queue_data['division_machine_id'])
    if division_machine.division.active is False:
        raise BadRequest('Division is not active')                    
    if division_machine.removed is True:
        raise BadRequest('Machine has been removed - you have been very naughty')            
    if division_machine.player_id is None and len(division_machine.queue) == 0:        
        raise BadRequest('No player is on machine - just jump on it')    
    player = fetch_entity(tables.Player,queue_data['player_id'])
    print "okay - starting with  %s"%player.player_id    
    if player.active is False:
        raise BadRequest("Player is not active - please see front desk")
    
    if player.division_machine:
        raise BadRequest("Can't queue - player  is already playing a machine")                
    if len(player.teams) > 0:
        if tables.DivisionMachine.query.filter_by(team_id=player.teams[0].team_id).first():
            raise BadRequest("Can't queue - player's team is on another machine")
    if check_player_team_can_start_game(current_app,division_machine,player) is False:
        raise BadRequest("Can't queue - player has no tokens")    
    #queue = tables.Queue.query.filter_by(player_id=player.player_id).first()
    #if queue and queue.division_machine_id == division_machine.division_machine_id:                
    #    return jsonify({'data':queue.to_dict_simple()})
    players_to_alert = []    
        
    with db.session.no_autoflush:
        try:            
            queues_to_lock = tables.Queue.query.with_for_update().filter_by(division_machine_id=division_machine.division_machine_id).all()
            queue = tables.Queue.query.filter_by(player_id=player.player_id).first()
            if queue and queue.division_machine_id == division_machine.division_machine_id:
                db.session.commit()
                return jsonify({'data':queue.to_dict_simple()})
            if queue:
                queues_to_lock = tables.Queue.query.with_for_update().filter_by(division_machine_id=queue.division_machine.division_machine_id).all()
                players_to_alert = get_player_list_to_notify(player.player_id,queue.division_machine)
            else:
                players_to_alert = []            
            removed_queue = remove_player_from_queue(current_app,player,commit=False)
            if removed_queue is not None and removed_queue is not False and len(players_to_alert) > 0:        
                push_notification_message = "The queue for %s has changed!  Please check the queue to see your new position." % queue.division_machine.machine.machine_name
                send_push_notification(push_notification_message, players=players_to_alert)
            new_queue = create_queue(current_app,queue_data['division_machine_id'],queue_data['player_id'])                                    
            db.session.commit()
            
            return jsonify({'data':new_queue.to_dict_simple()})
            #return jsonify({'data':None})
        except Exception as e:
            db.session.commit()
            print "poop %s"%e
            raise e

@admin_manage_blueprint.route('/queue/other_player',methods=['POST'])
def add_other_player_to_queue():
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    queue_data = json.loads(request.data)
    print queue_data
    division_machine = fetch_entity(tables.DivisionMachine, queue_data['division_machine_id'])

    if division_machine.division.active is False:
        raise BadRequest('Division is not active')                    
    if division_machine.removed is True:
        raise BadRequest('Machine has been removed - you have been very naughty')            
    if division_machine.player_id is None and len(division_machine.queue) == 0:        
        raise BadRequest('No player is on machine - just jump on it')    
    #player = fetch_entity(tables.Player,queue_data['player_id'])
    player = fetch_entity(tables.Player,queue_data['other_player_id'])
    print "okay - starting with  %s"%player.player_id    
    if player.active is False:
        raise BadRequest("Player is not active - please see front desk")
    if 'other_player_pin' not in queue_data or player.pin != int(queue_data['other_player_pin']):
        raise BadRequest('Invalid player id and player pin')    
    if player.division_machine:
        raise BadRequest("Can't queue - player  is already playing a machine")                
    if len(player.teams) > 0:
        if tables.DivisionMachine.query.filter_by(team_id=player.teams[0].team_id).first():
            raise BadRequest("Can't queue - player's team is on another machine")
    if check_player_team_can_start_game(current_app,division_machine,player) is False:
        raise BadRequest("Can't queue - player has no tokens")    
    queue = tables.Queue.query.filter_by(player_id=player.player_id).first()
    if queue and queue.division_machine_id == division_machine.division_machine_id:                
        return jsonify({'data':queue.to_dict_simple()})
    players_to_alert = []    
        
    with db.session.no_autoflush:
        try:
            queues_to_lock = tables.Queue.query.with_for_update().filter_by(division_machine_id=division_machine.division_machine_id).all()
            if queue:
                queues_to_lock = tables.Queue.query.with_for_update().filter_by(division_machine_id=queue.division_machine.division_machine_id).all()
                players_to_alert = get_player_list_to_notify(player.player_id,queue.division_machine)
            else:
                players_to_alert = []            
            removed_queue = remove_player_from_queue(current_app,player,commit=False)
            if removed_queue is not None and removed_queue is not False and len(players_to_alert) > 0:        
                push_notification_message = "The queue for %s has changed!  Please check the queue to see your new position." % queue.division_machine.machine.machine_name
                send_push_notification(push_notification_message, players=players_to_alert)
            new_queue = create_queue(current_app,queue_data['division_machine_id'],queue_data['other_player_id'])                                    
            db.session.commit()
            
            return jsonify({'data':new_queue.to_dict_simple()})
            #return jsonify({'data':None})
        except Exception as e:
            db.session.commit()
            print "poop %s"%e
            raise e
    

    # if division_machine.player_id is None and division_machine.queue is None:
    #     raise BadRequest('No player is on machine - just jump on it')    
    # player = fetch_entity(tables.Player,queue_data['other_player_id'])
    # if player.active is False:
    #     raise BadRequest("Player is not active - please see front desk")                        
    # if player.pin != int(queue_data['other_player_pin']):
    #     raise BadRequest('Invalid player id and player pin')
    # #check_player_team_can_start_game(current_app,division_machine,player)
    # if player.division_machine:
    #     raise BadRequest("Can't queue - player  is already playing a machine")                
        
    # if len(player.teams) > 0:
    #     if tables.DivisionMachine.query.filter_by(team_id=player.teams[0].team_id).first():
    #         raise BadRequest("Can't queue - player's team is on another machine")
    
    # if check_player_team_can_start_game(current_app,division_machine,player) is False:
    #     raise BadRequest("Can't queue - player has no tokens")

    # queue = tables.Queue.query.filter_by(player_id=player.player_id).first()
    # if queue and queue.division_machine_id == division_machine.division_machine_id:
    #     return jsonify({'data':queue.to_dict_simple()})
        
    # players_to_alert = []
    # if queue:
    #     players_to_alert = get_player_list_to_notify(player.player_id,queue.division_machine)        
    
    # removed_queue = remove_player_from_queue(current_app,player,commit=True)        
    # if removed_queue is not None and removed_queue is not False and len(players_to_alert) > 0:        
    #     push_notification_message = "The queue for %s has changed!  Please check the queue to see your new position." % queue.division_machine.machine.machine_name
    #     send_push_notification(push_notification_message, players=players_to_alert)    
    # new_queue = create_queue(current_app,queue_data['division_machine_id'],queue_data['other_player_id'])    
    # #db.session.add(new_queue)
    # db.session.commit()
    # return jsonify({'data':new_queue.to_dict_simple()})

@admin_manage_blueprint.route('/queue/division_machine/<division_machine_id>/bump',methods=['PUT'])
@login_required
@Queue_permission.require(403)
def bump_player_down_queue(division_machine_id):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)    
    division_machine = fetch_entity(tables.DivisionMachine,division_machine_id)
    if len(division_machine.queue) > 0:
        #queue = division_machine.queue[0]
        queue = tables.Queue.query.filter_by(division_machine_id=division_machine_id,parent_id=None).first()
    else:
        queue = None
    allow_bump=True        
    if queue and queue.bumped:
        allow_bump=False
    if len(queue.queue_child) == 0:
        allow_bump=False
    player_id = queue.player_id
    player = fetch_entity(tables.Player,player_id)

    with db.session.no_autoflush:
        try:
            queues_to_lock = tables.Queue.query.with_for_update().filter_by(division_machine_id=division_machine.division_machine_id).all()            
            if allow_bump:
                child_queue = queue.queue_child[0]
                if child_queue and len(child_queue.queue_child) > 0:
                    grand_child = child_queue.queue_child[0]
                else:
                    grand_child = None
                queue.queue_child.remove(child_queue)
                if grand_child:
                    child_queue.queue_child.remove(grand_child)
                new_queue = tables.Queue(
                    division_machine_id=division_machine_id,
                    player_id=player_id,
                    bumped=True
                )
                db.session.add(new_queue)                
                child_queue.queue_child.append(new_queue)
                if grand_child:
                    new_queue.queue_child.append(grand_child)
                db.session.delete(queue)                    
                create_audit_log("Player Bumped",datetime.datetime.now(),
                                 "",user_id=current_user.user_id,
                                 player_id=player_id,
                                 division_machine_id=division_machine.division_machine_id,                     
                                 commit=False)
            else:
                if queue:
                    players_to_alert = get_player_list_to_notify(player.player_id,queue.division_machine)
                else:
                    players_to_alert = []                                        
                remove_player_from_queue(current_app,player,commit=False)
                
                if len(players_to_alert) > 0:        
                    push_notification_message = "The queue for %s has changed!  Please check the queue to see your new position." % queue.division_machine.machine.machine_name
                    send_push_notification(push_notification_message, players=players_to_alert)
            if player.bump_count:
                player.bump_count = player.bump_count+1
            else:
                player.bump_count = 1
            print "about to commit bump..."            
            db.session.commit()
            return_queue = get_queue_from_division_machine(division_machine,True)            
            #db.session.commit()
            return jsonify({'data':{division_machine_id:{'queues':return_queue}}})        
        except Exception as e:
            db.session.commit()
            print "poop...%s"%e
            raise Conflict("Something went wrong while bumping player down queue - please try again.")


@admin_manage_blueprint.route('/queue/player/<player_id>',methods=['DELETE'])
@login_required
@Queue_permission.require(403)
def route_remove_player_from_queue(player_id):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)    
    player = fetch_entity(tables.Player,player_id)
    queue = tables.Queue.query.filter_by(player_id=player_id).first()    
    if queue is None:
        raise BadRequest('Player is not in any queues')    
    division_machine=queue.division_machine
    try:
        queues_to_lock = tables.Queue.query.with_for_update().filter_by(division_machine_id=division_machine.division_machine_id).all()                
        players_to_alert = get_player_list_to_notify(player.player_id,division_machine)    
        remove_result = remove_player_from_queue(current_app,player,commit=False)
        new_queue = get_queue_from_division_machine(division_machine,True)
        if len(players_to_alert) > 0:
            push_notification_message = """
            The queue for %s has changed! Check the queue to see your new position.
            """ % division_machine.machine.machine_name
            send_push_notification(push_notification_message, players=players_to_alert)
        db.session.commit()
    except Exception as e:
        db.session.commit()
        raise e
    return jsonify({'data':{division_machine.division_machine_id:{'queues':new_queue}}})


@admin_manage_blueprint.route('/queue/division_machine/<division_machine_id>',methods=['PUT'])
@login_required
@Queue_permission.require(403)
def add_player_to_machine_from_queue(division_machine_id):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)    
    division_machine = fetch_entity(tables.DivisionMachine,division_machine_id)
    if len(division_machine.queue) == 0:
        raise BadRequest('Trying to add player from an empty queue')
    if division_machine.player_id is not None:
        raise BadRequest('Trying to add player from a queue to a machine in use')    
    root_queue = tables.Queue.query.filter_by(division_machine_id=division_machine_id,parent_id=None).first()
    player = fetch_entity(tables.Player,root_queue.player_id)
    if check_player_team_can_start_game(current_app,division_machine,player=player) is False:
        raise BadRequest('Player can not start game - either no tickets or already on another machine')    
    with db.session.no_autoflush:
        try:
            queues_to_lock = tables.Queue.query.with_for_update().filter_by(division_machine_id=division_machine.division_machine_id).all()            

            players_to_alert = get_player_list_to_notify(player.player_id,division_machine)
            set_token_start_time(current_app,player,division_machine,commit=False)    
            division_machine.player_id = root_queue.player_id    
            if len(root_queue.queue_child) > 0:
                root_queue.queue_child.remove(root_queue.queue_child[0])
            db.session.delete(root_queue)
            db.session.commit()    
            return_dict = {'division_machine':division_machine.to_dict_simple()}
            if len(players_to_alert) > 0:        
                send_push_notification("The queue for %s has changed!  Please check the queue to see your new position." % division_machine.machine.machine_name,
                                       players=players_to_alert)
            return jsonify({'data': division_machine.to_dict_simple()})
        except Exception as e:
            db.session.commit()
            raise e
