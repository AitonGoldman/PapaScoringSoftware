from werkzeug.exceptions import BadRequest, Unauthorized
from lib_v2 import blueprints,permissions,pss_user_helpers
from flask import jsonify,current_app,request
from flask_login import current_user
from lib_v2.serializers import generic
import json
from time import sleep
from shutil import copyfile
from flask_restless.helpers import to_dict
from routes_v2.token import calculate_list_of_tickets_and_prices_for_player

def handle_img_upload(input_data):
    event_img_folders='/Users/agoldma/git/github/TD/front_v2/www/assets/imgs/'
    if input_data.get('img_file',None) and input_data.get('has_pic',None):
        copyfile(current_app.config['UPLOAD_FOLDER']+"/"+input_data['img_file'],event_img_folders+"/"+input_data['img_file'])
        input_data['img_url']='/assets/imgs/%s'%(input_data['img_file'])


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
        handle_img_upload(player_to_create)
        if 'player_id' in player_to_create:            
            player = tables_proxy.get_player(event_id,player_id=player_to_create['player_id'])
            if player is None:
                raise BadRequest('Tried to submit a player with an invalid player_id')            
            if len([event_info for event_info in player.event_info if event_info.event_id==int(event_id)])>0:
                raise BadRequest('Player already added to event')                
            
            tables_proxy.update_player_roles(event_id, player,
                                             player_to_create.get('ifpa_ranking',None),
                                             player_to_create.get('selected_division_in_multi_division_tournament',None))
            players_added_to_event.append(player)
            continue                        
        existing_players = tables_proxy.get_player(event_id,
                                                   first_name=player_to_create['first_name'],
                                                   last_name=player_to_create['last_name'],
                                                   extra_title=player_to_create.get('extra_title',None))
        if len(existing_players)>0:            
            raise BadRequest('Oops - that player already exists')
        new_player = tables_proxy.create_player(player_to_create['first_name'],
                                               player_to_create['last_name'],
                                               extra_title=player_to_create.get('extra_title',None),
                                               img_url=player_to_create.get('img_url',None))
        tables_proxy.update_player_roles(event_id, new_player,
                                        player_to_create.get('ifpa_ranking',None),
                                        player_to_create.get('selected_division_in_multi_division_tournament',None))        
        players_added_to_event.append(new_player)    
    return players_added_to_event


@blueprints.test_blueprint.route('/<int:event_id>/player',methods=['POST'])
def player_create(event_id):            
    #current_app.table_proxy.initialize_event_specific_relationship(event_id)
    permission = permissions.CreatePlayerPermission(event_id)    
    if not permission.can():
        raise Unauthorized('You are not authorized to register players for this event')            
    new_players=create_player_route(request,current_app.table_proxy,event_id)
    current_app.table_proxy.commit_changes()            
    new_players_serialized = [generic.serialize_player_private(new_player,generic.PLAYER_AND_EVENTS) for new_player in new_players]    
    return jsonify({'data':new_players_serialized})
    #return jsonify({'data':[{'player_full_name':'poop'}]})

@blueprints.test_blueprint.route('/<int:event_id>/event_player/<int:event_player_id>',methods=['GET'])
def get_event_player(event_id,event_player_id):                
    event_player = current_app.table_proxy.get_event_player(event_id,event_player_id)
    tournament_calculated_lists=[]
    if event_player:
        tournament_counts, meta_tournament_counts = current_app.table_proxy.get_available_token_count_for_tournaments(event_id,event_player)                
        player_dict=generic.serialize_player_public(event_player)
        for tournament in current_app.table_proxy.get_tournaments(event_id,exclude_metatournaments=True):
            if tournament_counts.get(tournament.tournament_id,None):
                max_amount_allowed_for_player=tournament.number_of_unused_tickets_allowed-tournament_counts[tournament.tournament_id]['count']
            else:
                max_amount_allowed_for_player=tournament.number_of_unused_tickets_allowed
            calculated_list = calculate_list_of_tickets_and_prices_for_player(0,event_player,current_app,event_id,tournament)
            if tournament_counts.get(tournament.tournament_id,None):                
                pruned_calculated_list = [price for price in calculated_list if price['amount'] <= max_amount_allowed_for_player]
            else:
                pruned_calculated_list = calculated_list            
            tournament_calculated_lists.append({'tournament_name':tournament.tournament_name,
                                                'tournament_id':tournament.tournament_id,
                                                'calculated_price_list':pruned_calculated_list})
        return jsonify({'data':player_dict,
                        'tournament_calculated_lists':to_dict(tournament_calculated_lists),
                        'tournament_counts':tournament_counts})
    else:
        raise BadRequest('That player number does not exist')

@blueprints.test_blueprint.route('/players/<string:query_string>',methods=['GET'])
def search_all_players(query_string):                
    
    players = current_app.table_proxy.search_player(query_string)
    if len(players)>25:
        player_max_index=2
    else:
        player_max_index=len(players)
    players_found_list=[generic.serialize_player_public(player,generic.PLAYER_AND_EVENTS) for player in players[0:player_max_index]]    
    #current_app.table_proxy.commit_changes()
    return jsonify({'data':players_found_list})
    #return jsonify(players_found_list)

@blueprints.test_blueprint.route('/players',methods=['GET'])
def get_all_players():            
    
    players = current_app.table_proxy.get_all_players()
    players_found_list=[generic.serialize_player_public(player,generic.PLAYER_AND_EVENTS) for player in players]
    #current_app.table_proxy.commit_changes()
    return jsonify({'data':players_found_list})

