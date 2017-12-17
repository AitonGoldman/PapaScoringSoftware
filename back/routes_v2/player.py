from werkzeug.exceptions import BadRequest, Unauthorized
from lib_v2 import blueprints,permissions,pss_user_helpers
from flask import jsonify,current_app,request
from flask_login import current_user
from lib_v2.serializers import generic
import json
    
def create_player_route(request,tables_proxy,event_id):
    #FIXME : check if user is already added to event
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Submitted information is missing required fields')    
    event = tables_proxy.get_event_by_event_id(event_id)    
    if event is None:
        raise BadRequest('No event with that ID')
    players_to_create=input_data['players']    
    players_added_to_event=[]        
    for player_to_create in players_to_create:        
        if 'player_id' in player_to_create:            
            player = tables_proxy.get_player_by_id(player_to_create['player_id'])
            if player is None:
                raise BadRequest('Tried to submit a player with an invalid player_id')            
            tables_proxy.update_player_roles(event_id, player,
                                             player_to_create.get('ifpa_ranking',None),
                                             player_to_create.get('selected_division_in_multi_division_tournament',None))
            players_added_to_event.append(player)
            continue                        
        existing_players = tables_proxy.get_players_by_name(player_to_create['first_name'],
                                                            player_to_create['last_name'],
                                                            player_to_create.get('extra_title',None))
        if len(existing_players)>0:            
            raise BadRequest('Oops - that player already exists')
        new_player = tables_proxy.create_player(player_to_create['first_name'],
                                                player_to_create['last_name'],
                                                extra_title=player_to_create.get('extra_title',None))
        tables_proxy.update_player_roles(event_id, new_player,
                                         player_to_create.get('ifpa_ranking',None),
                                         player_to_create.get('selected_division_in_multi_division_tournament',None))        
        players_added_to_event.append(new_player)    
    return players_added_to_event


@blueprints.test_blueprint.route('/<int:event_id>/player',methods=['POST'])
def player_create(event_id):            
    current_app.table_proxy.initialize_event_specific_relationship(event_id)
    permission = permissions.CreatePlayerPermission(event_id)    
    if not permission.can():
        raise Unauthorized('You are not authorized to register players for this event')        
    new_players=[generic.serialize_player_private(player) for player in create_player_route(request,current_app.table_proxy,event_id)]
    current_app.table_proxy.commit_changes()
    return jsonify({'data':new_players})

