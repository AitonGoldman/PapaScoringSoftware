from flask_restless.helpers import to_dict
from lib.flask_lib import blueprints
from flask import jsonify,current_app,request
from werkzeug.exceptions import BadRequest,Unauthorized,Conflict
from flask_login import login_user, logout_user, current_user
import json
from lib import orm_factories,token_helpers
from lib.serializer.generic import generate_generic_serializer
from lib import serializer
from lib.route_decorators.db_decorators import load_tables
from lib.route_decorators.auth_decorators import check_current_user_is_active
from sqlalchemy.orm import joinedload
from lib.flask_lib.permissions import event_user_buy_tickets_permissions
from lib.flask_lib.permissions import player_add_to_queue_permissions
from lib.flask_lib.permissions import bump_down_queue_permissions
from lib.flask_lib.permissions import clear_tournament_queue_permissions

from lib import queue_helpers,notification_helpers
import time
from sqlalchemy.orm import joinedload

def set_player_id_based_on_type_of_login(user,input_data):
    if hasattr(user,'pss_user_id'):        
        is_player=False
        if 'player_id' in input_data:
            player_id=input_data['player_id']
        else:
            raise BadRequest('No player id specified')
    else:
        is_player=True
        player_id=current_user.player_id
    return player_id

def check_tournament_machine_and_player(app,tournament_machine_id,player_id=None):
    tournament_machine = app.tables.TournamentMachines.query.filter_by(tournament_machine_id=tournament_machine_id).first()
    if tournament_machine is None:
        raise BadRequest('tournament_machine does not exist')
    if player_id is None:
        return    
    player = app.tables.Players.query.filter_by(player_id=player_id).first()            
    if player is None:
        raise BadRequest('player does not exist')                
    return tournament_machine,player

def clear_tournament_queue_route(app,tournament_id):
    queue_groups = queue_helpers.get_queue_for_tounament(app,tournament_id)        
    with app.tables.db_handle.session.no_autoflush:                
        try:
            queues_to_lock_for_for_removal = app.tables.Queues.query.with_for_update().join(app.tables.TournamentMachines).filter_by(tournament_id=tournament_id).all()
            for tournament_machine_id, queue_group in queue_groups:
                for queue in queue_group:
                    queue.player_id=None
                    queue.bumped=False
            app.tables.db_handle.session.commit()
            return {'result':'clear!'}
        except Exception as e:            
            app.tables.db_handle.session.commit()
            return {'result':'internal error : %s' % e,'added_queue':{}}

@blueprints.event_blueprint.route('/queue/tournament/<tournament_id>',methods=['DELETE'])
@clear_tournament_queue_permissions.require(403)
@check_current_user_is_active
@load_tables
def clear_tournament_queue(tables,tournament_id):
    return jsonify(clear_tournament_queue_route(current_app,tournament_id))

def remove_player_from_queue_route(request,app,tournament_machine_id,user):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Not enough info specified')

    player_id = set_player_id_based_on_type_of_login(user,input_data)    
    check_tournament_machine_and_player(app,tournament_machine_id,player_id)       

    with app.tables.db_handle.session.no_autoflush:                
        try:                                           
            
            queues = queue_helpers.get_queue_for_tounament_machine(app,tournament_machine_id)
            result = queue_helpers.remove_player_from_queue(app,player_id,queues=queues)
            app.tables.db_handle.session.commit()            
            if result:
                result_string='player removed'
            else:
                result_string='noop'
            queue_serializer = serializer.queue.generate_queue_to_dict_serializer(serializer.queue.ALL)
            return {'result':result_string,'updated_queue':[queue_serializer(queue) for queue in queues]}                            
            
        except Exception as e:            
            app.tables.db_handle.session.commit()
            return {'result':'internal error : %s' % e,'added_queue':{}}
    
@blueprints.event_blueprint.route('/queue/tournament_machine/<tournament_machine_id>',methods=['DELETE'])
@player_add_to_queue_permissions.require(403)
@check_current_user_is_active
@load_tables
def remove_player_from_queue(tables,tournament_machine_id):
    return jsonify(remove_player_from_queue_route(request,current_app,tournament_machine_id))

def bump_player_down_queue_route(request,app,tournament_machine_id):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Not enough info specified')

    if 'player_id' in input_data:
        player_id=input_data['player_id']
    else:
        raise BadRequest('no player id specified')
    
    check_tournament_machine_and_player(app,tournament_machine_id,player_id)    
    action=input_data['action']
    
    with app.tables.db_handle.session.no_autoflush:                
        try:                                           
            if action == 'bump':                                
                queues = queue_helpers.get_queue_for_tounament_machine(app,tournament_machine_id)
                if queues[0].player_id != int(player_id):
                    raise BadRequest('Tried to bump player that is not at head of queue')
                #FIXME : change logic to allow for more than one bump
                if queues[0].bumped is False and queues[1].player_id is not None:                    
                    queue_helpers.bump_player_down_queue(app,tournament_machine_id,queues)
                    app.tables.db_handle.session.commit()
                    
                elif queues[1].player_id is None or queues[0].bumped is True:                
                    queue_helpers.remove_player_from_queue(app,
                                                           queues[0].player_id,
                                                           queues=queues,
                                                           position_in_queue=1)
                    
                    app.tables.db_handle.session.commit()
                queue_serializer = serializer.queue.generate_queue_to_dict_serializer(serializer.queue.ALL)                
                return {'result':'player bumped','updated_queue':[queue_serializer(queue) for queue in queues if queue.player_id is not None]}                
        except Exception as e:            
            app.tables.db_handle.session.commit()            
            raise e
            #return {'result':'internal error : %s' % e,'added_queue':{}}
    
@blueprints.event_blueprint.route('/queue/tournament_machine/<tournament_machine_id>',methods=['PUT'])
@bump_down_queue_permissions.require(403)
@check_current_user_is_active
@load_tables
def bump_player_down_queue(tables,tournament_machine_id):
    return jsonify(bump_player_down_queue_route(request,app,tournament_machine_id))

#FIXME : raise exception, don't swallow it
def add_player_to_queue_route_validate(request,app,tournament_machine_id,user):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Not enough info specified')

    player_id = set_player_id_based_on_type_of_login(user,input_data)    
    
    action=input_data['action']
    tournament_machine,player=check_tournament_machine_and_player(app,tournament_machine_id,player_id)
    tournament = app.tables.Tournaments.query.filter_by(tournament_id=tournament_machine.tournament_id).first()
    
    if tournament.meta_tournament_id:        
        meta_tournament=app.tables.MetaTournaments.query.filter_by(meta_tournament_id=tournament.meta_tournament_id).first()
        token_count = token_helpers.get_number_of_unused_tickets_for_player(player,app,meta_tournament=meta_tournament)
    else:
        token_count = token_helpers.get_number_of_unused_tickets_for_player(player,app,tournament=tournament)
    
    if token_count<1:
        
        raise BadRequest('Player has no tokens')
    

def add_player_to_queue_route_remove_existing(request,app,tournament_machine_id,user):
    with app.tables.db_handle.session.no_autoflush:                
        try:
            input_data = json.loads(request.data)
            player_id = set_player_id_based_on_type_of_login(user,input_data)    
            
            existing_queue = queue_helpers.get_queue_player_is_already_in(player_id,app)            
            
            if existing_queue and existing_queue.tournament_machine_id == int(tournament_machine_id):                                                                
                raise BadRequest('Player can not be added to a queue when they are already on queue')

            queues = queue_helpers.get_queue_for_tounament_machine(app,tournament_machine_id)
            if queues[0].player_id is None:
                raise BadRequest('Can not add to empty queue.  Please see scorekeeper')
            if existing_queue:
                
                tournament_machine_id_to_remove_from = existing_queue.tournament_machine_id
                existing_position = existing_queue.position                                
                old_queues = queue_helpers.get_queue_for_tounament_machine(app,tournament_machine_id_to_remove_from)
                
                queue_helpers.remove_player_from_queue(app,
                                                       player_id,
                                                       queues=old_queues,
                                                       position_in_queue=existing_position)
                if app.event_config['ionic_api_key']:                    
                    notification_helpers.notify_list_of_players(queues[existing_position:],"test message")
                        
        except Exception as e:            
            app.tables.db_handle.session.commit()            
            raise e
            #return {'result':'internal error : %s' % e,'added_queue':{}}

def add_player_to_queue_route(request,app,tournament_machine_id,user):
    with app.tables.db_handle.session.no_autoflush:                
        try:
            input_data = json.loads(request.data)            
            player_id = set_player_id_based_on_type_of_login(user,input_data)    
            queues = queue_helpers.get_queue_for_tounament_machine(app,tournament_machine_id)                        
            updated_queue = queue_helpers.add_player_to_queue(player_id,queues,app,tournament_machine_id)
            
            app.tables.db_handle.session.commit()
            queue_serializer = serializer.queue.generate_queue_to_dict_serializer(serializer.queue.ALL)
            return {'result':'player added','added_queue':queue_serializer(updated_queue)}
            
        except Exception as e:            
            app.tables.db_handle.session.commit()                        
            raise e
            #return {'result':'internal error : %s' % e,'added_queue':{}}
            
@blueprints.event_blueprint.route('/queue/tournament_machine/<tournament_machine_id>',methods=['POST'])
@player_add_to_queue_permissions.require(403)
@check_current_user_is_active
@load_tables
def add_player_to_queue(tables,tournament_machine_id):
    add_player_to_queue_route_validate(request,current_app,tournament_machine_id,current_user)
    add_player_to_queue_route_remove_existing(request,current_app,tournament_machine_id,current_user)
    return jsonify(add_player_to_queue_route(request,current_app,tournament_machine_id,current_user))

def get_tournament_machine_queue_route(request,app,tournament_machine_id):

    queues = queue_helpers.get_queue_for_tounament_machine(app,tournament_machine_id)
    queue_serializer = serializer.queue.generate_queue_to_dict_serializer(serializer.queue.ALL)                
    return {'tournament_machine_queue':[queue_serializer(queue) for queue in queues]}                
    
@blueprints.event_blueprint.route('/queue/tournament_machine/<tournament_machine_id>',methods=['GET'])
@load_tables
def get_tournament_machine_queue(tables,tournament_machine_id):
    return jsonify(get_tournament_machine_queue_route(request,current_app,tournament_machine_id))    

def get_tournament_queue_route(app,tournament_id):
    queue_groups = queue_helpers.get_queue_for_tounament(app,tournament_id)
    
    queue_serializer = serializer.queue.generate_queue_to_dict_serializer(serializer.queue.ALL)                
    return jsonify({'tournament_queues':[{tournament_machine_id:[queue_serializer(queue) for queue in queue_group ]} for tournament_machine_id,queue_group in queue_groups]})
    
@blueprints.event_blueprint.route('/queue/tournament/<tournament_id>',methods=['GET'])
@load_tables
def get_tournament_queue(tables,tournament_id):
    return get_tournament_queue_route(current_app,tournament_id)
    
