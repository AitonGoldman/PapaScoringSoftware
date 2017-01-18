from blueprints import admin_login_blueprint,admin_manage_blueprint
from flask import jsonify,current_app,request
import json
from werkzeug.exceptions import BadRequest,Conflict
from util import db_util
from util.permissions import Admin_permission, Desk_permission, Token_permission, Queue_permission
from flask_login import login_required,current_user
from routes.utils import fetch_entity,check_player_team_can_start_game,set_token_start_time, remove_player_from_queue,get_queue_from_division_machine,send_push_notification,get_player_list_to_notify
import os
from flask_restless.helpers import to_dict
from orm_creation import create_queue


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
    for division_machine in division_machines:
        queues[division_machine.division_machine_id]={
            'division_machine_name':"%s"%division_machine.machine.machine_name,
            'division_machine_id':division_machine.division_machine_id,
            'division_id':division_machine.division_id,
            'player_id':division_machine.player_id,
            'queues':get_queue_from_division_machine(division_machine,json_output=True)
        }
    return jsonify({'data':queues})


@admin_manage_blueprint.route('/queue',methods=['POST'])
@login_required
@Queue_permission.require(403)
def add_player_to_queue():
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    queue_data = json.loads(request.data)
    division_machine = fetch_entity(tables.DivisionMachine, queue_data['division_machine_id'])
    if division_machine.player_id is None and division_machine.queue is None:
        raise BadRequest('No player is on machine - just jump on it')    
    player = fetch_entity(tables.Player,queue_data['player_id'])
    #check_player_team_can_start_game(current_app,division_machine,player)
    if player.division_machine:
        raise BadRequest("Can't queue - player  is already playing a machine")                
        
    if len(player.teams) > 0:
        if tables.DivisionMachine.query.filter_by(team_id=player.teams[0].team_id).first():
            raise BadRequest("Can't queue - player's team is on another machine")
    
    if check_player_team_can_start_game(current_app,division_machine,player) is False:
        raise BadRequest("Can't queue - player has no tokens")

    queue = tables.Queue.query.filter_by(player_id=player.player_id).first()
    players_to_alert = []
    if queue:
        players_to_alert = get_player_list_to_notify(player.player_id,queue.division_machine)        
        
    removed_queue = remove_player_from_queue(current_app,player)        
    if removed_queue is not None and removed_queue is not False and len(players_to_alert) > 0:        
        push_notification_message = "The queue for %s has changed!  Please check the queue to see your new position." % queue.division_machine.machine.machine_name
        send_push_notification(push_notification_message, players=players_to_alert)
    new_queue = create_queue(current_app,queue_data['division_machine_id'],queue_data['player_id'])    
    return jsonify({'data':new_queue.to_dict_simple()})

@admin_manage_blueprint.route('/queue/division_machine/<division_machine_id>/bump',methods=['PUT'])
@login_required
@Queue_permission.require(403)
def bump_player_down_queue(division_machine_id):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)    
    division_machine = fetch_entity(tables.DivisionMachine,division_machine_id)
    queue = division_machine.queue        
    allow_bump=True        
    if queue and queue.bumped:
        allow_bump=False
    player_id = queue.player_id
    player = fetch_entity(tables.Player,player_id)
    if remove_player_from_queue(current_app,player) is False:
        raise BadRequest('Expecting to remove player from head of queue, but could not')
    division_machine = fetch_entity(tables.DivisionMachine,division_machine_id)
    queue = division_machine.queue    
    if queue is None:
        #do not allow bumps if there is no queue to bump down
        return_queue = get_queue_from_division_machine(division_machine,True)            
        return jsonify({'data':{division_machine_id:{'queues':return_queue}}})        
    if allow_bump:        
        create_queue(current_app,division_machine.division_machine_id,player_id,bumped=True)
    #return jsonify({'data':moved_up_queue.to_dict_simple()})    
    return_queue = get_queue_from_division_machine(division_machine,True)    
    return jsonify({'data':{division_machine_id:{'queues':return_queue}}})


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
    players_to_alert = get_player_list_to_notify(player.player_id,division_machine)    
    remove_result = remove_player_from_queue(current_app,player)
    new_queue = get_queue_from_division_machine(division_machine,True)
    if len(players_to_alert) > 0:
        push_notification_message = """
        The queue for %s has changed! Check the queue to see your new position.
        """ % division_machine.machine.machine_name
        send_push_notification(push_notification_message, players=players_to_alert)
    
    return jsonify({'data':{division_machine.division_machine_id:{'queues':new_queue}}})


@admin_manage_blueprint.route('/queue/division_machine/<division_machine_id>',methods=['PUT'])
@login_required
@Queue_permission.require(403)
def add_player_to_machine_from_queue(division_machine_id):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)    
    division_machine = fetch_entity(tables.DivisionMachine,division_machine_id)
    if division_machine.queue_id is None:
        raise BadRequest('Trying to add player from an empty queue')
    if division_machine.player_id is not None:
        raise BadRequest('Trying to add player from a queue to a machine in use')    
    root_queue = division_machine.queue
    player = fetch_entity(tables.Player,root_queue.player_id)
    if check_player_team_can_start_game(current_app,division_machine,player=player) is False:
        raise BadRequest('Player can not start game - either no tickets or already on another machine')    
    players_to_alert = get_player_list_to_notify(player.player_id,division_machine)
    set_token_start_time(current_app,player,division_machine,commit=False)    
    division_machine.player_id = root_queue.player_id    
    if len(root_queue.queue_child)==0:
        division_machine.queue_id = None
        ##db.session.commit()        
    else:
        division_machine.queue_id = root_queue.queue_child[0].queue_id
        root_queue.queue_child[0].parent_id=None        
        ##db.session.commit()        
    db.session.delete(root_queue)
    db.session.commit()    
    return_dict = {'division_machine':division_machine.to_dict_simple()}
    #if division_machine.queue_id:
    #    return_dict['next_queue']=division_machine.queue.to_dict_simple()
    if len(players_to_alert) > 0:        
        send_push_notification("The queue for %s has changed!  Please check the queue to see your new position." % division_machine.machine.machine_name,
                               players=players_to_alert)
    return jsonify({'data': division_machine.to_dict_simple()})
