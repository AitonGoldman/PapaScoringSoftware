from werkzeug.exceptions import BadRequest, Unauthorized, NotFound
from lib_v2 import blueprints,permissions,pss_user_helpers
from flask import jsonify,current_app,request
from flask_login import current_user
from lib_v2.serializers import generic
import json
from time import sleep
from shutil import copyfile
from flask_restless.helpers import to_dict
from routes_v2.token import calculate_list_of_tickets_and_prices_for_player,prereg_event_user_purchase_tokens

def handle_img_upload(input_data):
    event_img_folders=current_app.config['IMG_HTTP_SRV_DIR']
    if input_data.get('img_file',None) and input_data.get('has_pic',None):
        copyfile(current_app.config['UPLOAD_FOLDER']+"/"+input_data['img_file'],event_img_folders+"/"+input_data['img_file'])
        input_data['img_url']='/assets/imgs/%s'%(input_data['img_file'])
        input_data['has_pic']=True
        
def edit_player_route(request,app,event_id):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Submitted information is missing required fields')
    #put tournament edit logic here
    handle_img_upload(input_data)
    player = app.table_proxy.edit_player(input_data,False)        
    return player

def create_player_route(request,tables_proxy,event_id,perform_existing_player_check=True):
    #FIXME : check if user is already added to event
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Submitted information is missing required fields')    
    event = tables_proxy.get_event_by_event_id(event_id)    
    print "%s event id " % event_id
    if event is None:
        raise BadRequest('No event with that ID')
    players_to_create=input_data['players']    
    players_added_to_event=[]        
    for player_to_create in players_to_create:        
        handle_img_upload(player_to_create)
        if 'player_id' in player_to_create and player_to_create.get('player_id'):            
            player = tables_proxy.get_player(event_id,player_id=player_to_create['player_id'])
            if player is None:
                raise BadRequest('Tried to submit a player with an invalid player_id')            
            if len([event_info for event_info in player.event_info if event_info.event_id==int(event_id)])>0 and perform_existing_player_check:
                raise BadRequest('Player already added to event')                
            email_address=player_to_create.get('email_address',None)
            print "adding player to event %s" %event_id    
            tables_proxy.update_player_roles(event_id, player,
                                             player_to_create.get('ifpa_ranking',None),
                                             player_to_create.get('selected_division_in_multi_division_tournament',None),
                                             email_address=email_address)
            if player_to_create.get('img_url',None):
                player.img_url=player_to_create['img_url']
                player.has_pic=True
                
            players_added_to_event.append(player)
            continue                        
        existing_players = tables_proxy.get_player(event_id,
                                                   first_name=player_to_create['first_name'],
                                                   last_name=player_to_create['last_name'],
                                                   extra_title=player_to_create.get('extra_title',None))
        if len(existing_players)>0 and perform_existing_player_check:            
            raise BadRequest('Oops - that player already exists')
        new_player = tables_proxy.create_player(player_to_create['first_name'],
                                               player_to_create['last_name'],
                                               extra_title=player_to_create.get('extra_title',None),
                                               img_url=player_to_create.get('img_url',None))
        if new_player.img_url:
            new_player.has_pic=True
        email_address=input_data['players'][0].get('email_address',None)
        tables_proxy.update_player_roles(event_id, new_player,
                                        player_to_create.get('ifpa_ranking',None),
                                         player_to_create.get('selected_division_in_multi_division_tournament',None),
                                         email_address=email_address)        
        players_added_to_event.append(new_player)    
    return players_added_to_event


def get_event_player_route(app,event_id,event_player_id):
    event_player = app.table_proxy.get_event_player(event_id,event_player_id)
    tournament_calculated_lists=[]
    if event_player:
        tournament_counts, meta_tournament_counts = app.table_proxy.get_available_token_count_for_tournaments(event_id,event_player)
        permission = permissions.CreatePlayerPermission(event_id)    
        if not permission.can():            
            player_dict=generic.serialize_player_public(event_player,generic.PLAYER_AND_EVENTS,event_id)
        else:
            player_dict=generic.serialize_player_private(event_player,generic.PLAYER_AND_EVENTS,event_id)
            
        for tournament in app.table_proxy.get_tournaments(event_id,exclude_metatournaments=True):
            if tournament_counts.get(tournament.tournament_id,None):
                max_amount_allowed_for_player=tournament.number_of_unused_tickets_allowed-tournament_counts[tournament.tournament_id]['count']
            else:
                max_amount_allowed_for_player=tournament.number_of_unused_tickets_allowed
            calculated_list = calculate_list_of_tickets_and_prices_for_player(0,event_player,app,event_id,tournament)
            if tournament_counts.get(tournament.tournament_id,None):                
               pruned_calculated_list = [price for price in calculated_list if price['amount'] <= max_amount_allowed_for_player]
            else:
               pruned_calculated_list = calculated_list            
            tournament_calculated_lists.append({'tournament_name':tournament.tournament_name,
                                               'tournament_id':tournament.tournament_id,
                                               'calculated_price_list':pruned_calculated_list})
        player_dict['tournament_counts']=tournament_counts
        current_queue = current_app.table_proxy.get_queue_player_is_already_in(event_player,event_id) 
        current_machine = current_app.table_proxy.get_tournament_machine_player_is_playing(event_player,event_id)
        if current_queue:
            player_dict['queue_player_is_in'] = generic.serialize_queue(current_queue,generic.QUEUE_AND_MACHINE)
        if current_machine:
            player_dict['machine_player_is_on'] = generic.serialize_tournament_machine_public(current_machine)

        tournament_calculated_lists = sorted(tournament_calculated_lists, key= lambda e: e['tournament_name'])

        return {'data':player_dict,
                'tournament_calculated_lists':to_dict(tournament_calculated_lists),
                'tournament_counts':tournament_counts}
    else:
        raise NotFound('That player number does not exist')
    
@blueprints.test_blueprint.route('/<int:event_id>/player',methods=['POST'])
def player_create(event_id):            
    #current_app.table_proxy.initialize_event_specific_relationship(event_id)
    permission = permissions.CreatePlayerPermission(event_id)    
    if not permission.can():
        raise Unauthorized('You are not authorized to register players for this new')            
    event_players=create_player_route(request,current_app.table_proxy,event_id)
    current_app.table_proxy.commit_changes()            
    new_players_serialized = [generic.serialize_player_private(new_player,event_id=event_id) for new_player in event_players]
    #new_players_serialized = [generic.serialize_player_private(new_player,generic.PLAYER_AND_EVENTS) for new_player in new_players]
    event = current_app.table_proxy.get_event_by_event_id(event_id)
    return_json = {'data':new_players_serialized}
    if event.require_pics:
        return_json['require_pic']=True
    return jsonify(return_json)
    #return jsonify({'data':[{'player_full_name':'poop'}]})

@blueprints.test_blueprint.route('/<int:event_id>/<int:tournament_id>/prereg_player',methods=['POST'])
def prereg_player_create(event_id,tournament_id):    
    input_data = json.loads(request.data)    
    player = input_data['players'][0]
    event = current_app.table_proxy.get_event_by_event_id(event_id)
    player_name = player['first_name']+" "+player['last_name']
    if player['extra_title']:
        player_name = player_name+" "+extra_title
    players_found_list = search_for_players(player_name,event_id)        
    if len(players_found_list) == 1:
        historical_tokens = current_app.table_proxy.get_historical_tokens_for_player(event_id,players_found_list[0]['player_id'])        
        if historical_tokens and len(historical_tokens)>0:                        
            return jsonify({'data':[],'status':'existing'})
        else:            
            ## make sure to insert email addess if not already present
            player = current_app.table_proxy.get_player(event_id,players_found_list[0]['player_id'])            
            token_purchase = prereg_event_user_purchase_tokens(event_id,player,request,tournament_id)
            new_player_serialized = generic.serialize_player_private(player,generic.PLAYER_AND_EVENTS)
            new_player_serialized['event_player_id']=new_player_serialized['events'][0]['player_id_for_event']
            return jsonify({'data':new_player_serialized,'status':'unpaid','token_purchase':to_dict(token_purchase),'stripe_key':event.stripe_public_key,})
        
    if len(players_found_list) > 1:
        return jsonify({'data':[],'status':'multiple'})
    global_players_found_list = search_for_players(player_name)        
    print global_players_found_list
    
    if len(global_players_found_list)==1:
        old_json = json.loads(request.data)        
        old_json['players'][0]['player_id']=global_players_found_list[0]['player_id']        

        request.data = json.dumps(old_json)
        print request.data
    event_players=create_player_route(request,current_app.table_proxy,event_id,perform_existing_player_check=False)    
    token_purchase = prereg_event_user_purchase_tokens(event_id,event_players[0],request,tournament_id)
    current_app.table_proxy.commit_changes()            
    new_player_serialized = generic.serialize_player_private(event_players[0],generic.PLAYER_AND_EVENTS)    
    new_player_serialized['event_player_id']=new_player_serialized['events'][0]['player_id_for_event']    
    
    return jsonify({'data':new_player_serialized,'token_purchase':to_dict(token_purchase),'stripe_key':event.stripe_public_key,'status':'created'})
    #return jsonify({'data':[{'player_full_name':'poop'}]})
    
@blueprints.test_blueprint.route('/<int:event_id>/event_player/<int:event_player_id>',methods=['GET'])
def get_event_player(event_id,event_player_id):                
    event_player_info = get_event_player_route(current_app,event_id,event_player_id)
    event_player_info['data']['tournament_calculated_lists']=event_player_info['tournament_calculated_lists']
    event_player_info['data']['tournament_counts']=event_player_info['tournament_counts']
    event = current_app.table_proxy.get_event_by_event_id(event_id)
    event_player_info['stripe_public_key']=event.stripe_public_key
    return jsonify(event_player_info)
    # event_player = current_app.table_proxy.get_event_player(event_id,event_player_id)
    # tournament_calculated_lists=[]
    # if event_player:
    #     tournament_counts, meta_tournament_counts = current_app.table_proxy.get_available_token_count_for_tournaments(event_id,event_player)                
    #     player_dict=generic.serialize_player_public(event_player)
    #     for tournament in current_app.table_proxy.get_tournaments(event_id,exclude_metatournaments=True):
    #         if tournament_counts.get(tournament.tournament_id,None):
    #             max_amount_allowed_for_player=tournament.number_of_unused_tickets_allowed-tournament_counts[tournament.tournament_id]['count']
    #         else:
    #             max_amount_allowed_for_player=tournament.number_of_unused_tickets_allowed
    #         calculated_list = calculate_list_of_tickets_and_prices_for_player(0,event_player,current_app,event_id,tournament)
    #         if tournament_counts.get(tournament.tournament_id,None):                
    #             pruned_calculated_list = [price for price in calculated_list if price['amount'] <= max_amount_allowed_for_player]
    #         else:
    #             pruned_calculated_list = calculated_list            
    #         tournament_calculated_lists.append({'tournament_name':tournament.tournament_name,
    #                                             'tournament_id':tournament.tournament_id,
    #                                             'calculated_price_list':pruned_calculated_list})
    #     return jsonify({'data':player_dict,
    #                     'tournament_calculated_lists':to_dict(tournament_calculated_lists),
    #                     'tournament_counts':tournament_counts})
    # else:
    #     raise BadRequest('That player number does not exist')

@blueprints.test_blueprint.route('/<int:event_id>/event_players/no_pics',methods=['GET'])
def get_all_event_players_with_no_pics(event_id):                
    all_event_players=current_app.table_proxy.get_all_event_players(event_id)
    players_with_no_pics=[generic.serialize_player_public(player) for player in all_event_players if player.has_pic is False]    
    return jsonify({"data":players_with_no_pics})

def search_for_players(query_string, event_id=None):
    query_string=query_string.lower()
    players = current_app.table_proxy.search_player(query_string,event_id)
    if len(players)>25:
        player_max_index=2
    else:
        player_max_index=len(players)    
    return [generic.serialize_player_public(player,generic.PLAYER_AND_EVENTS,event_id=event_id) for player in players[0:player_max_index]]    
    #current_app.table_proxy.commit_changes()
    

@blueprints.test_blueprint.route('/players/<string:query_string>',methods=['GET'])
def search_all_players(query_string):                
    
    # players = current_app.table_proxy.search_player(query_string)
    # if len(players)>25:
    #     player_max_index=2
    # else:
    #     player_max_index=len(players)
    # players_found_list=[generic.serialize_player_public(player,generic.PLAYER_AND_EVENTS) for player in players[0:player_max_index]]    
    # #current_app.table_proxy.commit_changes()
    players_found_list = search_for_players(query_string)
    return jsonify({'data':players_found_list})
    #return jsonify(players_found_list)


@blueprints.test_blueprint.route('/<int:event_id>/event_players/<string:query_string>',methods=['GET'])
def search_all_event_players(event_id,query_string):                    
    # players = current_app.table_proxy.search_player(query_string,event_id)
    # if len(players)>25:
    #     player_max_index=2
    # else:
    #     player_max_index=len(players)
    # players_found_list=[generic.serialize_player_public(player,generic.PLAYER_AND_EVENTS) for player in players[0:player_max_index]]    
    # #current_app.table_proxy.commit_changes()
    event=current_app.table_proxy.get_event_by_event_id(event_id)    

    players_found_list = search_for_players(query_string,event_id)
    return jsonify({'data':players_found_list,'event':generic.serialize_event_public(event)})
    #return jsonify(players_found_list)
    
@blueprints.test_blueprint.route('/players',methods=['GET'])
def get_all_players():            
    
    players = current_app.table_proxy.get_all_players()
    players_found_list=[generic.serialize_player_public(player,generic.PLAYER_AND_EVENTS) for player in players]
    #current_app.table_proxy.commit_changes()
    return jsonify({'data':players_found_list})

@blueprints.test_blueprint.route('/<int:event_id>/player',methods=['PUT'])
def edit_player(event_id):            
    permission = permissions.EditPlayerPermission(event_id)    
    if not permission.can():
        raise Unauthorized('You are not authorized to edit players for this event')        
    player = edit_player_route(request,current_app,event_id)
    current_app.table_proxy.commit_changes()
    player_dict=generic.serialize_player_public(player)
    return jsonify({'data':player_dict})
