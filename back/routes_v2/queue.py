from flask_restless.helpers import to_dict
from werkzeug.exceptions import BadRequest, Unauthorized
from lib_v2 import blueprints,permissions
from flask import jsonify,current_app,request
from flask_login import current_user
from lib_v2.serializers import generic
import json

def bump_player_down_queue_route(request,app,event_id):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Not enough info specified')
    player_id = input_data.get('player_id',None)
    tournament_machine_id=input_data.get('tournament_machine_id',None)
    player = app.table_proxy.get_player(event_id, player_id=player_id)
    tournament_machine = app.table_proxy.get_tournament_machine_by_id(tournament_machine_id)
    with app.table_proxy.db_handle.session.no_autoflush:                
        try:                                    
            queues = app.table_proxy.get_sorted_queue_for_tournament_machine(tournament_machine)
            if len(queues)<2:
                raise BadRequest('Trying to bump player on queue with only 1 player')            
            if queues[0].player_id!=player_id:
                raise BadRequest('Trying to bump player who is not at head of the queue')
            if queues[0].bumped:                
                remove_player_with_notification(player,app,tournament_machine,event_id)
                return
            app.table_proxy.bump_player_down_queue(player,
                                                   tournament_machine)                    
        except Exception as e:            
            app.table_proxy.db_handle.session.commit()            
            raise e            

def remove_player_route(request,app,event_id):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Not enough info specified')
    player_id = input_data.get('player_id',None)
    tournament_machine_id=input_data.get('tournament_machine_id',None)
    player = app.table_proxy.get_player(event_id, player_id=player_id)
    tournament_machine = app.table_proxy.get_tournament_machine_by_id(tournament_machine_id)
    with app.table_proxy.db_handle.session.no_autoflush:                
        try:
            remove_player_with_notification(player,app,tournament_machine,event_id)
        except Exception as e:            
            app.table_proxy.db_handle.session.commit()            
            raise e            
        

def remove_player_with_notification(player,app,tournament_machine, event_id):
    with app.table_proxy.db_handle.session.no_autoflush:                
        try:                                    
            existing_queue = app.table_proxy.get_queue_player_is_already_in(player,event_id)                        
            if existing_queue:                
                tournament_machine_to_remove_from = app.table_proxy.get_tournament_machine_by_id(existing_queue.tournament_machine_id)
                existing_position = existing_queue.position                                                                
                app.table_proxy.remove_player_from_queue(player,
                                                         tournament_machine_to_remove_from,
                                                         position_in_queue=existing_position)
                #if app.event_settings[event_id].ionic_api_key:                
                #    notification_helpers.notify_list_of_players(queues[existing_position:],"test message")
                    
        except Exception as e:            
            app.table_proxy.db_handle.session.commit()            
            raise e            

def add_player_to_tournament_machine_queue_route(request,app,event_id,current_user):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Not enough info specified')
    player_id = input_data.get('player_id',None)
    tournament_machine_id=input_data.get('tournament_machine_id',None)
    if player_id is None:
        player = current_user.player_id        
    player = app.table_proxy.get_player(event_id, player_id=player_id)
    tournament_machine = app.table_proxy.get_tournament_machine_by_id(tournament_machine_id)
    if tournament_machine.player_id == player.player_id or app.table_proxy.get_tournament_machine_player_is_playing(player,event_id):
        raise BadRequest('Player is already playing a game')
    
    tournament=app.table_proxy.get_tournament_by_tournament_id(tournament_machine.tournament_id)
    if tournament.meta_tournament_id:
        meta_tournament=app.table_proxy.get_meta_tournament_by_id(tournament.meta_tournament_id)
        token_count = app.table_proxy.get_available_token_count_for_tournament(event_id,player,meta_tournament=meta_tournament)
    else:
        token_count = app.table_proxy.get_available_token_count_for_tournament(event_id,player,tournament=tournament)            
    if token_count<1:        
        raise BadRequest('Player has no tokens')
    
    queues = app.table_proxy.get_queue_for_tounament_machine(tournament_machine)
    if tournament_machine.player_id is None:
        raise BadRequest('Can not add to empty queue.  Please see scorekeeper')

    remove_player_with_notification(player,app,tournament_machine, event_id)
    with app.table_proxy.db_handle.session.no_autoflush:                
        try:            
            updated_queue = app.table_proxy.add_player_to_queue(player,app,tournament_machine)                        
            #queue_serializer = serializer.queue.generate_queue_to_dict_serializer(serializer.queue.ALL)
            #return {'result':'player added','added_queue':queue_serializer(updated_queue)}
            
        except Exception as e:            
            app.table_proxy.db_handle.session.commit()                        
            raise e
            #return {'result':'internal error : %s' % e,'added_queue':{}}
    
    pass

@blueprints.test_blueprint.route('/<int:event_id>/queue',methods=['POST'])
def add_player_to_queue(event_id):
    add_player_to_tournament_machine_queue_route(request,current_app,event_id,current_user)
    current_app.table_proxy.commit_changes()
    return jsonify({})
    pass

@blueprints.test_blueprint.route('/<int:event_id>/queue',methods=['DELETE'])
def remove_player_to_queue(event_id):
    remove_player_route(request,current_app,event_id)
    current_app.table_proxy.commit_changes()
    return jsonify({})
    pass

@blueprints.test_blueprint.route('/<int:event_id>/queue',methods=['PUT'])
def modify_player_position_in_queue(event_id):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Not enough info specified')
    if input_data['action']=="bump":
        bump_player_down_queue_route(request,current_app,event_id)
    current_app.table_proxy.commit_changes()
    return jsonify({})
    pass
