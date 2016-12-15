from blueprints import admin_login_blueprint,admin_manage_blueprint
from flask import jsonify,current_app,request
import json
from werkzeug.exceptions import BadRequest,Conflict
from util import db_util
from util.permissions import Admin_permission,Scorekeeper_permission
from flask_login import login_required,current_user
from routes.utils import fetch_entity,check_player_team_can_start_game,set_token_start_time,remove_player_from_queue,get_valid_sku
from orm_creation import create_division, create_division_machine


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
    if division_machine.player_id or division_machine.team_id:
        raise Conflict('Machine is already being played')
    if check_player_team_can_start_game(current_app,division_machine,player) is False:
        raise BadRequest('Player can not start game - either no tickets or already on another machine')
    set_token_start_time(current_app,player,division_machine)    
    division_machine.player_id=player.player_id
    tables.db_handle.session.commit()
    remove_player_from_queue(current_app,player)    
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

@admin_manage_blueprint.route('/division/<division_id>/division_machine/<int:division_machine_id>/player',
                              methods=['DELETE'])
@login_required
@Scorekeeper_permission.require(403)
def route_remove_division_machine_player(division_id,division_machine_id):            
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)                            
    division_machine = fetch_entity(tables.DivisionMachine,division_machine_id)            
    if division_machine.player_id is None:
        raise BadRequest('No player playing on this machine')
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
    set_token_start_time(current_app,None,division_machine,team_id=team_id)    
    division_machine.team_id=team.team_id
    tables.db_handle.session.commit()
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

