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

        if flask_app.table_proxy.get_tournament_machine_player_is_playing(player, event_id):    
            current_ticket_amount=current_ticket_amount+1
    #if player.event_player.team_id and flask_app.tables.TournamentMachines.query.filter_by(team_id=player.event_player.team_id).first():
    #    current_ticket_amount=current_ticket_amount+1        
    cutoff_index=tournament.number_of_unused_tickets_allowed-current_ticket_count
    return [{'amount':0,'price':0}]+output_list[0:cutoff_index]


def calculate_cost_of_single_ticket_count(amount,player,app,event_id, meta_tournament=None,tournament=None):
    calculated_list = calculate_list_of_tickets_and_prices_for_player(0, player,                                                                      
                                                                      app, event_id, meta_tournament=meta_tournament,
                                                                      tournament=tournament)
    return [calculated_cost for calculated_cost in calculated_list if int(calculated_cost['amount'])==int(amount)][0]


def insert_tokens_into_db(list_of_tournament_tokens, tournaments_dict,
                          type, player,
                          app, new_token_purchase,
                          event_id,
                          player_initiated=False, comped=False):    
    purchase_summary = []
    if len(list_of_tournament_tokens) == 0:
        return []
    for token_count in list_of_tournament_tokens:
        tournament = tournaments_dict[token_count['%s_id' % type]]
        if tournament.team_tournament and player.event_player.team_id is None:
            continue
        normal_and_discount_amounts = get_normal_and_discount_amounts(tournament,int(token_count['token_count']))
        if int(token_count['token_count'])==0:
            continue        
        if type == "tournament":
            ticket_cost = calculate_cost_of_single_ticket_count(int(token_count['token_count']),player,app,event_id, tournament=tournament)
        else:
            ticket_cost = calculate_cost_of_single_ticket_count(int(token_count['token_count']),player,app,event_id, meta_tournament=tournament)

        #FIXME : this should be a dict, not a list
        if type == "tournament":
            tournament_name=tournament.tournament_name
        else:
            tournament_name=tournament.meta_tournament_name            
        purchase_summary.append([tournament_name,token_count['token_count'],ticket_cost])
        token_purchase_summary = app.table_proxy.create_token_purchase_summary()
        if type == "tournament":
            token_purchase_summary.tournament_id=tournament.tournament_id
        else:
            token_purchase_summary.meta_tournament_id=tournament.meta_tournament_id
        token_purchase_summary.token_count=token_count['token_count']
        #app.tables.db_handle.session.add(token_purchase_summary)
        new_token_purchase.token_purchase_summaries.append(token_purchase_summary)

        if player_initiated:
            new_token_purchase.stripe_purchase=True
        else:
            new_token_purchase.stripe_purchase=False
            
        for count in range(int(token_count['token_count'])):
            #new_token = app.tables.Tokens()
            new_token=app.table_proxy.create_token(event_id)
            if player_initiated:
                new_token.paid_for=False                
            else:
                new_token.paid_for=True                
            new_token.comped=comped
            new_token.player_id=player.player_id
            if tournament.team_tournament and player.event_roles[0].team_id:
                new_token.team_id=player.event_roles[0].team_id
            if type == "tournament":
                new_token.tournament_id=tournament.tournament_id
            else:
                new_token.meta_tournament_id=tournament.meta_tournament_id                            
            new_token_purchase.tokens.append(new_token)
    return purchase_summary


def get_number_of_unused_tickets_for_player(player,app,event_id, meta_tournament=None,tournament=None):
    #FIXME : explore if it makes sense to query al tokens (for all divisions) at once
    query = app.tables.Tokens.query.filter_by(used=False,voided=False,paid_for=True,deleted=False)
    if player.event_roles.team_id is None and tournament and tournament.team_tournament:
        return 0
    if tournament:
        if tournament.team_tournament is True:
            token_count = query.filter_by(tournament_id=tournament.tournament_id,team_id=player.event_player.team_id).count()
        else:            
            token_count = query.filter_by(player_id=player.player_id,tournament_id=tournament.tournament_id).count()
    if meta_tournament:
        token_count = query.filter_by(meta_tournament_id=meta_tournament.meta_tournament_id).count()    
    return token_count


def verify_tournament_and_meta_tournament_request_counts_are_valid(input_data, event_id,
                                                                   player,type,
                                                                   tournaments_dict, app):
    list_of_tournament_tokens=[]
    list_of_meta_tournament_tokens=[]

    for token_count in input_data['%s_token_counts' % type]:        
        if int(token_count['token_count']) == 0:
            continue
        tournament = tournaments_dict[token_count['%s_id' % type]]
        if type == 'tournament':
            #request_token_count = get_number_of_unused_tickets_for_player(player,app,event_id, tournament=tournament)
            request_token_count = app.table_proxy.get_available_token_count_for_tournament(event_id,player,tournament=tournament)
        else:
            #request_token_count = get_number_of_unused_tickets_for_player(player,app,event_id, meta_tournament=tournament)
            request_token_count = app.table_proxy.get_available_token_count_for_tournament(event_id,player,meta_tournament=tournament)
        max_tokens_player_is_allowed_to_buy = tournament.number_of_unused_tickets_allowed - request_token_count
        #if app.tables.TournamentMachines.query.filter_by(player_id=player.player_id).first():
        if app.table_proxy.get_tournament_machine_player_is_playing(player, event_id):
            max_tokens_player_is_allowed_to_buy=max_tokens_player_is_allowed_to_buy-1
        if max_tokens_player_is_allowed_to_buy-int(token_count['token_count'])<0:
            raise BadRequest('Fuck off, Ass Wipe')
        if tournament.ifpa_rank_restriction and player.event_roles[0].ifpa_ranking and player.event_roles[0].ifpa_ranking < tournament.ifpa_rank_restriction:
            raise BadRequest('Ifpa restrictions have been violated')    
        
        list_of_tournament_tokens.append(token_count)
    return list_of_tournament_tokens

def purchase_tickets_route(request, app, event_id, player_initiated=False):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('No info in request')        
    player = app.table_proxy.get_player_by_id(input_data['player_id'])
    list_of_tournament_tokens=[]
    list_of_meta_tournament_tokens=[]

    comped = input_data.get('comped',False)
    
    #tournaments_dict = {tournament.tournament_id:tournament for tournament in app.tables.Tournaments.query.filter_by(meta_tournament_id=None).all()}
    #meta_tournaments_dict = {meta_tournament.meta_tournament_id:meta_tournament for meta_tournament in app.tables.MetaTournaments.query.all()}

    tournaments_dict = {tournament.tournament_id:tournament for tournament in app.table_proxy.get_tournaments(event_id,exclude_metatournaments=True)}
    meta_tournaments_dict = {meta_tournament.meta_tournament_id:meta_tournament for meta_tournament in app.table_proxy.get_meta_tournaments(event_id)}
    
    list_of_tournament_tokens = verify_tournament_and_meta_tournament_request_counts_are_valid(input_data, event_id, player,
                                                                                               "tournament", tournaments_dict,
                                                                                               app)
    list_of_meta_tournament_tokens = verify_tournament_and_meta_tournament_request_counts_are_valid(input_data, event_id, player,
                                                                                                    "meta_tournament", meta_tournaments_dict,
                                                                                                    app)

    #new_token_purchase=app.table_proxy.TokenPurchases()
    #app.tables.db_handle.session.add(new_token_purchase)    
    new_token_purchase = app.table_proxy.create_token_purchase()
    purchase_summary = insert_tokens_into_db(list_of_tournament_tokens, tournaments_dict,
                                             "tournament", player,
                                             app, new_token_purchase,
                                             event_id,
                                             player_initiated=player_initiated, comped=comped)
    meta_purchase_summary = insert_tokens_into_db(list_of_meta_tournament_tokens, meta_tournaments_dict,
                                                  "meta_tournament", player,
                                                  app, new_token_purchase,
                                                  event_id,
                                                  player_initiated=player_initiated, comped=comped)    
    total_cost = sum(int(summary[2]['price']) for summary in purchase_summary+meta_purchase_summary)
    new_token_purchase.total_cost=total_cost
    if player_initiated is False:
        new_token_purchase.completed_purchase=True
    else:
        new_token_purchase.completed_purchase=False    
    audit_log={'player_id':player.player_id,
               'action':'Ticket Purchase',
               'player_initiated':player_initiated}
    purchase_summary_string = ", ".join([" : ".join([str(summary[0]),str(summary[1])]) for summary in purchase_summary+meta_purchase_summary])    

    if player_initiated is False:
        audit_log_description_string='tickets purchased - %s ' % (purchase_summary_string)
    else:
        audit_log_description_string='started purchase (token_purchase_id : %s) - %s' % (new_token_purchase.token_purchase_id,purchase_summary_string)
        
    audit_log['description']=audit_log_description_string
    #orm_factories.create_audit_log(app,audit_log)    
    #app.tables.db_handle.session.commit()
    return new_token_purchase,purchase_summary+meta_purchase_summary


@blueprints.test_blueprint.route('/<int:event_id>/token',methods=['PUT'])
def event_user_purchase_tokens(event_id):
    new_token_purchase,purchase_summary = purchase_tickets_route(request,current_app,event_id,player_initiated=False)
    current_app.table_proxy.commit_changes()
    #total_cost = sum(int(summary[2]['price']) for summary in purchase_summary)
    #generic_serializer = generate_generic_serializer(serializer.generic.ALL)
    #return jsonify({'new_token_purchase':generic_serializer(new_token_purchase),
    #                'purchase_summary':purchase_summary,
    #                'total_cost':new_token_purchase.total_cost})
    return jsonify({})
