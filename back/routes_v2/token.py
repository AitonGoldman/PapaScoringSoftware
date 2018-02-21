from flask_restless.helpers import to_dict
from werkzeug.exceptions import BadRequest, Unauthorized
from lib_v2 import blueprints,permissions
from flask import jsonify,current_app,request
from flask_login import current_user
from lib_v2.serializers import generic
import json

def get_discount_price(tournament):
    if tournament.use_stripe:
        return tournament.discount_stripe_price
    else:
        return tournament.discount_price

#FIXME : Better name for this
def get_price(tournament):
    if tournament.use_stripe:
        return tournament.stripe_price
    else:
        return tournament.manually_set_price

def get_normal_and_discount_amounts(tournament,amount):
    if tournament.number_of_tickets_for_discount:
        if amount < tournament.number_of_tickets_for_discount:
            return (amount,0)
        if amount == tournament.number_of_tickets_for_discount:
            return (0,1)        
        return (amount%tournament.number_of_tickets_for_discount,int(amount/tournament.number_of_tickets_for_discount))
    else:
        return (amount,0)
    pass


def calculate_list_of_tickets_and_prices_for_player(current_ticket_count, player,
                                                    flask_app, event_id,
                                                    meta_tournament=None,
                                                    tournament=None):
    if meta_tournament:
        tournament = meta_tournament
    last_discounted_cost=None
    last_discounted_amount=None
    discount_price=get_discount_price(tournament)
    normal_price=get_price(tournament)
    output_list=[]    
    for current_ticket_amount in range(tournament.minimum_number_of_tickets_allowed,
                                       tournament.number_of_unused_tickets_allowed+1,
                                       tournament.ticket_increment_for_each_purchase):
        if tournament.number_of_tickets_for_discount and current_ticket_amount < tournament.number_of_tickets_for_discount:
            output_list.append({'amount':current_ticket_amount,'price':current_ticket_amount*normal_price})
        elif tournament.number_of_tickets_for_discount and current_ticket_amount == tournament.number_of_tickets_for_discount:
            last_discounted_cost=discount_price
            last_discounted_amount=current_ticket_amount
            output_list.append({'amount':current_ticket_amount,'price':discount_price})
        elif tournament.number_of_tickets_for_discount and current_ticket_amount%tournament.number_of_tickets_for_discount==0:
            last_discounted_cost=discount_price*(current_ticket_amount/tournament.number_of_tickets_for_discount)
            last_discounted_amount=current_ticket_amount
            output_list.append({'amount':current_ticket_amount,'price':last_discounted_cost})            
        elif tournament.number_of_tickets_for_discount:
            delta_ticket_amount = current_ticket_amount-last_discounted_amount
            ticket_cost = last_discounted_cost+(delta_ticket_amount*normal_price)
            output_list.append({'amount':current_ticket_amount,'price':ticket_cost})
        elif tournament.number_of_tickets_for_discount is None:            
            output_list.append({'amount':current_ticket_amount,'price':current_ticket_amount*normal_price})

        # if flask_app.table_proxy.get_tournament_machine_player_is_playing(player, event_id):    
        #     current_ticket_amount=current_ticket_amount+1
        pass
    if flask_app.table_proxy.get_tournament_machine_player_is_playing(player, event_id):    
        current_ticket_amount=current_ticket_amount+1
    
    cutoff_index=tournament.number_of_unused_tickets_allowed-current_ticket_count
    return [{'amount':0,'price':0}]+output_list[0:cutoff_index]


def calculate_cost_of_single_ticket_count(amount,player,app,event_id, meta_tournament=None,tournament=None):
    calculated_list = calculate_list_of_tickets_and_prices_for_player(0, player,                                                                      
                                                                      app, event_id, meta_tournament=meta_tournament,
                                                                      tournament=tournament)
    return [calculated_cost for calculated_cost in calculated_list if int(calculated_cost['amount'])==int(amount)][0]


def insert_tokens_into_db(list_of_tournament_tokens, player,
                          app, new_token_purchase,
                          event_id,
                          player_initiated=False, comped=False):    
    purchase_summary = []
    for token_count in list_of_tournament_tokens:
        tournament = token_count.get('tournament',None)
        meta_tournament = token_count.get('meta_tournament',None)                
        if tournament and tournament.team_tournament and player.event_info[0].team_id is None:
            continue
        ticket_cost = calculate_cost_of_single_ticket_count(int(token_count['token_count']),player,app,event_id, tournament=tournament,meta_tournament=meta_tournament)          
        purchase_summary_dict = {                                 
                                 "token_count":token_count['token_count'],
                                 "ticket_cost":ticket_cost
        }
        if tournament:
            purchase_summary_dict["tournament_id"]=tournament.tournament_id
            purchase_summary_dict["tournament_name"]=tournament.tournament_name
        if meta_tournament:            
            purchase_summary_dict["meta_tournament_id"]=meta_tournament.meta_tournament_id
            purchase_summary_dict["meta_tournament_name"]=meta_tournament.meta_tournament_name
        purchase_summary.append(purchase_summary_dict)
            
        for count in range(int(token_count['token_count'])):            
            new_token=app.table_proxy.create_token(event_id,
                                                   player_initiated=player_initiated,
                                                   comped=comped,
                                                   player=player,
                                                   tournament=tournament,
                                                   meta_tournament=meta_tournament,
                                                   team_id=player.event_info[0].team_id)
            
            new_token_purchase.tokens.append(new_token)
    return purchase_summary


def verify_tournament_and_meta_tournament_request_counts_are_valid(list_of_tournament_tokens,
                                                                   list_of_meta_tournament_tokens,
                                                                   event_id,
                                                                   player,
                                                                   app):
    tournament_counts, meta_tournament_counts = app.table_proxy.get_available_token_count_for_tournaments(event_id,player)    
    for tournament_token in list_of_tournament_tokens+list_of_meta_tournament_tokens:
        #FIXME : just query for the tournament/meta_tournament here
        tournament=tournament_token.get('tournament',None)
        meta_tournament = tournament_token.get('meta_tournament',None)
        
        if tournament:
            max_tokens_player_is_allowed_to_buy = tournament.number_of_unused_tickets_allowed
            if tournament_counts.get(tournament.tournament_id,None):
                request_token_count = tournament_counts[tournament.tournament_id]['count']
                max_tokens_player_is_allowed_to_buy = max_tokens_player_is_allowed_to_buy - request_token_count
        if meta_tournament:
            max_tokens_player_is_allowed_to_buy = meta_tournament.number_of_unused_tickets_allowed
            if meta_tournament_counts.get(meta_tournament.meta_tournament_id,None):
                request_token_count = meta_tournament_counts[meta_tournament.meta_tournament_id]['count']
                max_tokens_player_is_allowed_to_buy = max_tokens_player_is_allowed_to_buy - request_token_count
    
        if app.table_proxy.get_tournament_machine_player_is_playing(player, event_id):
            max_tokens_player_is_allowed_to_buy=max_tokens_player_is_allowed_to_buy-1
        if max_tokens_player_is_allowed_to_buy-int(tournament_token['token_count'])<0:
            raise BadRequest('Fuck off, Ass Wipe')
        if tournament and tournament.ifpa_rank_restriction and player.event_info[0].ifpa_ranking and player.event_info[0].ifpa_ranking < tournament.ifpa_rank_restriction:
            raise BadRequest('Ifpa restrictions have been violated')    
                    

def purchase_tickets_route(request, app, event_id, player_initiated=False, logged_in_player=None, current_user=None):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('No info in request')        
    if player_initiated:
        player = app.table_proxy.get_player(event_id, player_id=logged_in_player.player_id,initialize_event_specific_relationship=True)
    else:
        player = app.table_proxy.get_player(event_id, player_id=input_data['player_id'],initialize_event_specific_relationship=True)
    list_of_tournament_tokens=[]
    list_of_meta_tournament_tokens=[]
    # input format
    # {"tournament_counts":[{"tournament_id":1,"count":1}],"meta_tournament_counts":[]}    
    for tournament in app.table_proxy.get_tournaments(event_id,exclude_metatournaments=True):        
        for tournament_count in input_data.get('tournament_token_counts',[]):            
            if int(tournament_count['tournament_id'])==tournament.tournament_id:
                if int(tournament_count.get('token_count',0)) > 0:
                    if tournament.allow_phone_purchases is False and player_initiated:
                        raise BadRequest('Ticket purchases by players have been disabled for this tournament.  Sorry.')
                    if tournament.active is not True:
                        raise BadRequest('Ticket purchases have been disabled for this tournament.  Sorry.')
                    
                    tournament_count['tournament']=tournament
                    list_of_tournament_tokens.append(tournament_count)    
    for meta_tournament in app.table_proxy.get_meta_tournaments(event_id):        
        for meta_tournament_count in input_data.get('meta_tournament_token_counts',[]):            
            if int(meta_tournament_count['meta_tournament_id'])==meta_tournament.meta_tournament_id:                
                if int(meta_tournament_count.get('token_count',0)) > 0:
                    if meta_tournament.allow_phone_purchases is False:
                        raise BadRequest('Ticket purchases by players have been disabled.  Sorry.')

                    meta_tournament_count['meta_tournament']=meta_tournament
                    list_of_meta_tournament_tokens.append(meta_tournament_count)
    if len(list_of_tournament_tokens)==0 and len(list_of_meta_tournament_tokens)==0:
        raise BadRequest('0 tickets were requested')
    verify_tournament_and_meta_tournament_request_counts_are_valid(list_of_tournament_tokens,list_of_meta_tournament_tokens, event_id, player, app)

    new_token_purchase = app.table_proxy.create_token_purchase(player_initiated=player_initiated)
    purchase_summaries = insert_tokens_into_db(list_of_tournament_tokens+list_of_meta_tournament_tokens,
                                               player,
                                               app, new_token_purchase,
                                               event_id,
                                               player_initiated=player_initiated, comped=input_data.get('comped',False))
    for purchase_summary in purchase_summaries:        
        token_purchase_summary = app.table_proxy.create_token_purchase_summary(new_token_purchase)                
        if purchase_summary.get('tournament_id',None):
            token_purchase_summary.tournament_id=purchase_summary['tournament_id']
        else:
            token_purchase_summary.meta_tournament_id=purchase_summary['meta_tournament_id']
        token_purchase_summary.token_count=purchase_summary['token_count']            
                
    new_token_purchase.total_cost=sum(int(summary['ticket_cost']['price']) for summary in purchase_summaries)
    purchase_summary_string = ", ".join([" : ".join([str(summary.get('tournament_name',summary.get('meta_tournament_name'))),
                                                     str(summary['token_count'])]) for summary in purchase_summaries])    
    audit_log_params={'player_id':player.player_id,                      
                      'player_initiated':player_initiated,
                      'event_id':event_id}
    if player_initiated is not True:
        new_token_purchase.completed_purchase=True
        audit_log_params['pss_user_id']=current_user.pss_user_id
        audit_log_params['action']='Ticket Purchase'
        audit_log_description_string='tickets purchased - %s ' % (purchase_summary_string)        
    else:
        audit_log_params['action']='Player Ticket Purchase started'            
        audit_log_description_string='started purchase (token_purchase_id : %s) - %s' % (new_token_purchase.token_purchase_id,purchase_summary_string)        
        
    audit_log_params['description']=audit_log_description_string
    app.table_proxy.create_audit_log(audit_log_params,event_id)    
    return new_token_purchase,purchase_summaries

def complete_player_token_purchase_route(request,app, event_id, token_purchase_id):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('No info in request')        
    token_purchase = app.table_proxy.get_token_purchase_by_id(token_purchase_id)
    if len(token_purchase.tokens)==0:
        raise BadRequest('0 tickets were specified')
    player_id = token_purchase.tokens[0].player_id
    if token_purchase.completed_purchase:
        raise BadRequest('You are trying to pay for something that is already paid for')                
    stripe_items=[]
    for token_purchase_summary in token_purchase.token_purchase_summaries:
        token_count=token_purchase_summary.token_count
        if token_purchase_summary.tournament_id:
            tournament=app.table_proxy.get_tournament_by_tournament_id(token_purchase_summary.tournament_id)
        else:
            tournament=app.table_proxy.get_meta_tournament_by_id(token_purchase_summary.meta_tournament_id) 
        normal_and_discount_amounts = get_normal_and_discount_amounts(tournament,token_count)
        discount_sku = tournament.discount_stripe_sku
        normal_sku = tournament.stripe_sku
        discount_count = normal_and_discount_amounts[1]
        normal_count = normal_and_discount_amounts[0]                
        if discount_count > 0:
            stripe_items.append({"quantity":discount_count,"type":"sku","parent":discount_sku})
        if normal_count > 0:
            stripe_items.append({"quantity":normal_count,"type":"sku","parent":normal_sku})           
    api_key = app.event_settings[event_id].stripe_api_key    
    result = app.stripe_proxy.purchase_tickets(stripe_items,api_key,input_data['stripe_token'],input_data['email'],token_purchase)    
    token_purchase.stripe_transaction_id=result.get('order_id_string',None)    
    audit_log_params={
        'action':'Player Ticket Purchase Complete',
        'player_id':player_id,                      
        'player_initiated':True,        
        'description':token_purchase.stripe_transaction_id,
        'event_id':event_id
    }
    app.table_proxy.create_audit_log(audit_log_params,event_id)    
    return result,token_purchase

@blueprints.test_blueprint.route('/<int:event_id>/token',methods=['POST'])
def event_user_purchase_tokens(event_id):
    input_data = json.loads(request.data)
    desk_permission = permissions.DeskTokenPurchasePermission(event_id)
    if desk_permission.can():                
        new_token_purchase,purchase_summary = purchase_tickets_route(request,current_app,event_id,player_initiated=False,current_user=current_user)            
    player_permission = permissions.PlayerTokenPurchasePermission(event_id)
    if player_permission.can():
        if input_data.get('comped',False) is True:
            raise BadRequest('Naughty Naughty')
        new_token_purchase,purchase_summary = purchase_tickets_route(request,current_app,event_id,player_initiated=True,logged_in_player=current_user)            

    current_app.table_proxy.commit_changes()    
    #total_cost = sum(int(summary['ticket_cost']['price']) for summary in purchase_summary)    
    return jsonify({'new_token_purchase':to_dict(new_token_purchase),
                    'purchase_summary':purchase_summary,
                    'total_cost':new_token_purchase.total_cost})
    

@blueprints.test_blueprint.route('/<int:event_id>/token/<token_purchase_id>',methods=['PUT'])
def player_complete_purchase_tokens(event_id,token_purchase_id):
    player_permission = permissions.PlayerTokenPurchasePermission(event_id)
    if player_permission.can():                
        result,token_purchase = complete_player_token_purchase_route(request,current_app, event_id, token_purchase_id)
        if result.get('error_text',None):
            raise BadRequest(result['error_text'])
        else:            
            current_app.table_proxy.commit_changes()
    #total_cost = sum(int(summary[2]['price']) for summary in purchase_summary)
    #generic_serializer = generate_generic_serializer(serializer.generic.ALL)
    #return jsonify({'new_token_purchase':generic_serializer(new_token_purchase),
    #                'purchase_summary':purchase_summary,
    #                'total_cost':new_token_purchase.total_cost})

    return jsonify({})
