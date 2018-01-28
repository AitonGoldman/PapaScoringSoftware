from flask_restless.helpers import to_dict
from werkzeug.exceptions import BadRequest, Unauthorized
from lib_v2 import blueprints,permissions
from flask import jsonify,current_app,request
from flask_login import current_user
from lib_v2.serializers import generic
from lib_v2.queue_helpers import remove_player_with_notification
import json

def bump_player_down_queue_route(request,app,event_id,current_user):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Not enough info specified')    
    player_id = input_data.get('player_id',None)
    tournament_machine_id=input_data.get('tournament_machine_id',None)
    player = app.table_proxy.get_player(event_id, player_id=player_id)
    tournament_machine = app.table_proxy.get_tournament_machine_by_id(tournament_machine_id)    
    audit_log_params={
        'action':'Player Bumped Down Queue',
        'player_id':player.player_id,
        'pss_user_id':current_user.pss_user_id,
        'player_initiated':False,        
        'description':'Player %s bumped down queue by %s' % (player,current_user),
        'tournament_machine_id':tournament_machine.tournament_machine_id,
        'event_id':event_id
    }

    with app.table_proxy.db_handle.session.no_autoflush:                
        try:                                    
            queues = app.table_proxy.get_sorted_queue_for_tournament_machine(tournament_machine)
            if queues[0].player_id!=player_id:
                raise BadRequest('Trying to bump player who is not at head of the queue')
            if queues[0].bumped or (queues[0].player_id==player.player_id and queues[1].player_id is None):                
                remove_player_with_notification(player,app,tournament_machine,event_id)
                audit_log_params['action']='Player Bumped Down Queue And Removed'
                app.table_proxy.create_audit_log(audit_log_params,event_id)    
                return
            app.table_proxy.bump_player_down_queue(player,
                                                   tournament_machine)            
        except Exception as e:            
            app.table_proxy.db_handle.session.commit()            
            raise e            
    app.table_proxy.create_audit_log(audit_log_params,event_id)    

def remove_player_route(request,app,event_id,current_user,player_initiated=False):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Not enough info specified')
    player_id = input_data.get('player_id',None)
    if player_initiated and player_id != current_user.player_id:
        raise BadRequest('Naughty Naughty')
    tournament_machine_id=input_data.get('tournament_machine_id',None)
    player = app.table_proxy.get_player(event_id, player_id=player_id)
    tournament_machine = app.table_proxy.get_tournament_machine_by_id(tournament_machine_id)
    print tournament_machine.tournament_machine_id
    with app.table_proxy.db_handle.session.no_autoflush:                
        try:
            remove_player_with_notification(player,app,tournament_machine,event_id)
        except Exception as e:            
            app.table_proxy.db_handle.session.commit()            
            raise e            
    audit_log_params={
        'action':'Player Removed From Queue',
        'player_id':player.player_id,        
        'player_initiated':player_initiated,        
        'description':'Player %s removed from queue by %s' % (player,current_user),
        'tournament_machine_id':tournament_machine.tournament_machine_id,
        'event_id':event_id
    }
    if player_initiated is not True:
        audit_log_params['pss_user_id']=current_user.pss_user_id
    app.table_proxy.create_audit_log(audit_log_params,event_id)    
    return player

# def remove_player_with_notification(player,app,tournament_machine, event_id):
#     with app.table_proxy.db_handle.session.no_autoflush:                
#         try:                                    
#             existing_queue = app.table_proxy.get_queue_player_is_already_in(player,event_id)                        
#             if existing_queue:                
#                 tournament_machine_to_remove_from = app.table_proxy.get_tournament_machine_by_id(existing_queue.tournament_machine_id)
#                 existing_position = existing_queue.position                                                                
#                 app.table_proxy.remove_player_from_queue(player,
#                                                          tournament_machine_to_remove_from,
#                                                          position_in_queue=existing_position)
#                 #if app.event_settings[event_id].ionic_api_key:                
#                 #    notification_helpers.notify_list_of_players(queues[existing_position:],"test message")
                    
#         except Exception as e:            
#             app.table_proxy.db_handle.session.commit()            
#             raise e            

def add_player_to_tournament_machine_queue_route(request,app,event_id,current_user,player_initiated=False):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Not enough info specified')
    player_id = input_data.get('player_id',None)
    if player_initiated and player_id != current_user.player_id:
        raise BadRequest('Naughty Naughty')
    tournament_machine_id=input_data.get('tournament_machine_id',None)
    if player_id is None:
        player = current_user.player_id        
    player = app.table_proxy.get_player(event_id, player_id=player_id)
    tournament_machine = app.table_proxy.get_tournament_machine_by_id(tournament_machine_id)
    if tournament_machine.player_id == player.player_id or app.table_proxy.get_tournament_machine_player_is_playing(player,event_id):
        raise BadRequest('Player is already playing a game')
    
    tournament=app.table_proxy.get_tournament_by_tournament_id(tournament_machine.tournament_id)
    if tournament.active is False:
        raise BadRequest('Can not queue because tournament is no longer active')

    #if tournament.meta_tournament_id:
    #    meta_tournament=app.table_proxy.get_meta_tournament_by_id(tournament.meta_tournament_id)
    # tournament_counts,meta_tournament_counts = app.table_proxy.get_available_token_count_for_tournaments(event_id,player)
    # if tournament.meta_tournament_id:
    #     token_count=meta_tournament_counts[tournament.meta_tournament_id]['count']
    # else:
    #     token_count=tournament_counts[tournament.tournament_id]['count']
    token_count = app.table_proxy.get_available_token_count_for_tournament(event_id,player,tournament)   
    if token_count<1:        
        raise BadRequest('Player has no tokens')
    
    queues = app.table_proxy.get_queue_for_tounament_machine(tournament_machine)
    if tournament_machine.player_id is None and queues[0].player_id is None:
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
    audit_log_params={
        'action':'Player Added To Queue',
        'player_id':player.player_id,        
        'player_initiated':player_initiated,        
        'description':'Player %s added to queue by %s' % (player,current_user),
        'tournament_machine_id':tournament_machine.tournament_machine_id,
        'event_id':event_id
    }
    if player_initiated is not True:
        audit_log_params['pss_user_id']=current_user.pss_user_id
    app.table_proxy.create_audit_log(audit_log_params,event_id)    
    return updated_queue
    

@blueprints.test_blueprint.route('/<int:event_id>/queue',methods=['POST'])
def add_player_to_queue(event_id):
    queue_permission = permissions.QueuePermission(event_id)
    if queue_permission.can():
        updated_queue = add_player_to_tournament_machine_queue_route(request,current_app,event_id,current_user)
    player_permission = permissions.PlayerTokenPurchasePermission(event_id)
    if player_permission.can():        
        updated_queue = add_player_to_tournament_machine_queue_route(request,current_app,event_id,current_user,player_initiated=True)
    current_app.table_proxy.commit_changes()
    return jsonify({'data':to_dict(updated_queue)})
    pass

@blueprints.test_blueprint.route('/<int:event_id>/queue',methods=['DELETE'])
def remove_player_to_queue(event_id):
    queue_permission = permissions.QueuePermission(event_id)    
    if queue_permission.can():        
        player = remove_player_route(request,current_app,event_id,current_user)
    player_permission = permissions.PlayerTokenPurchasePermission(event_id)
    if player_permission.can():        
        player = remove_player_route(request,current_app,event_id,current_user,player_initiated=True)
    current_app.table_proxy.commit_changes()
    return jsonify({'data':generic.serialize_player_public(player)})
    pass

@blueprints.test_blueprint.route('/<int:event_id>/queue',methods=['PUT'])
def modify_player_position_in_queue(event_id):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Not enough info specified')
    if input_data['action']=="bump":
        queue_permission = permissions.QueuePermission(event_id)
        if queue_permission.can():
            bump_player_down_queue_route(request,current_app,event_id,current_user)
        else:
            raise BadRequest('You do not have permission to bump players')
    current_app.table_proxy.commit_changes()
    tournament_machine = current_app.table_proxy.get_tournament_machine_by_id(input_data['tournament_machine_id'])
    tournament_machine_dict=generic.serialize_tournament_machine_public(tournament_machine,generic.TOURNAMENT_MACHINE_AND_QUEUES)            
    return jsonify({'data':tournament_machine_dict})
    pass
