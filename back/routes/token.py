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
from lib.flask_lib.permissions import player_buy_tickets_permissions

#FIXME : figure out a way to just pass type into functions that need to accept both tournaments and meta_tournaments (i.e. see insert_tokens_into_db)

def insert_tokens_into_db(list_of_tournament_tokens, tournaments_dict,
                          type, player,
                          app, new_token_purchase,
                          player_initiated=False, comped=False):    
    purchase_summary = []
    if len(list_of_tournament_tokens) == 0:
        return []
    for token_count in list_of_tournament_tokens:
        tournament = tournaments_dict[token_count['%s_id' % type]]
        normal_and_discount_amounts = token_helpers.get_normal_and_discount_amounts(tournament,int(token_count['token_count']))
        if int(token_count['token_count'])==0:
            continue        
        if type == "tournament":
            ticket_cost = calculate_cost_of_single_ticket_count(int(token_count['token_count']),player,app,tournament=tournament)
        else:
            ticket_cost = calculate_cost_of_single_ticket_count(int(token_count['token_count']),player,app,meta_tournament=meta_tournament)

        #FIXME : this should be a dict, not a list
        purchase_summary.append([tournament.tournament_name,token_count['token_count'],ticket_cost])
        token_purchase_summary = app.tables.TokenPurchaseSummaries()
        if type == "tournament":
            token_purchase_summary.tournament_id=tournament.tournament_id
        else:
            token_purchase_summary.meta_tournament_id=tournament.meta_tournament_id
        token_purchase_summary.token_count=token_count['token_count']
        app.tables.db_handle.session.add(token_purchase_summary)
        new_token_purchase.token_purchase_summaries.append(token_purchase_summary)
        for count in range(int(token_count['token_count'])):
            new_token = app.tables.Tokens()
            if player_initiated:
                new_token.paid_for=False
            else:
                new_token.paid_for=True
            new_token.comped=comped
            new_token.player_id=player.player_id
            if tournament.team_tournament and player.team_id:
                new_token.team_id=player.team_id
            if type == "tournament":
                new_token.tournament_id=tournament.tournament_id
            else:
                new_token.meta_tournament_id=tournament.meta_tournament_id
                
            app.tables.db_handle.session.add(new_token)            
            new_token_purchase.tokens.append(new_token)
    return purchase_summary
    
def verify_tournament_and_meta_tournament_request_counts_are_valid(input_data, player,
                                                                   type, tournaments_dict,
                                                                   app):
    list_of_tournament_tokens=[]
    list_of_meta_tournament_tokens=[]

    for token_count in input_data['%s_token_counts' % type]:        
        if int(token_count['token_count']) == 0:
            continue
        tournament = tournaments_dict[token_count['%s_id' % type]]
        if type == 'tournament':
            request_token_count = token_helpers.get_number_of_unused_tickets_for_player(player,app,tournament=tournament)
        else:
            request_token_count = token_helpers.get_number_of_unused_tickets_for_player(player,app,meta_tournament=tournament)            
        max_tokens_player_is_allowed_to_buy = tournament.number_of_unused_tickets_allowed - request_token_count
        if max_tokens_player_is_allowed_to_buy-int(token_count['token_count'])<0:
            raise BadRequest('Fuck off, Ass Wipe')
        if tournament.ifpa_rank_restriction and player.event_player.ifpa_ranking and player.event_player.ifpa_ranking < tournament.ifpa_rank_restriction:
            raise BadRequest('Ifpa restrictions have been violated')    
        
        list_of_tournament_tokens.append(token_count)
    return list_of_tournament_tokens
    

def purchase_tickets_route(request,player,app,player_initiated=False):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('No info in request')        

    list_of_tournament_tokens=[]
    list_of_meta_tournament_tokens=[]

    comped = input_data.get('comped',False)
    
    tournaments_dict = {tournament.tournament_id:tournament for tournament in app.tables.Tournaments.query.all()}
    meta_tournaments_dict = {meta_tournament.meta_tournament_id:meta_tournament for meta_tournament in app.tables.MetaTournaments.query.all()}
    
    list_of_tournament_tokens = verify_tournament_and_meta_tournament_request_counts_are_valid(input_data, player,
                                                                                               "tournament", tournaments_dict,
                                                                                               app)
    list_of_meta_tournament_tokens = verify_tournament_and_meta_tournament_request_counts_are_valid(input_data, player,
                                                                                                    "meta_tournament", meta_tournaments_dict,
                                                                                                    app)

    new_token_purchase=app.tables.TokenPurchases()
    app.tables.db_handle.session.add(new_token_purchase)    

    purchase_summary = insert_tokens_into_db(list_of_tournament_tokens, tournaments_dict,
                                             "tournament", player,
                                             app, new_token_purchase,
                                             player_initiated=player_initiated, comped=comped)
    meta_purchase_summary = insert_tokens_into_db(list_of_meta_tournament_tokens, meta_tournaments_dict,
                                                  "meta_tournament", player,
                                                  app, new_token_purchase,
                                                  player_initiated=player_initiated, comped=comped)    
    total_cost = sum(int(summary[2]['price']) for summary in purchase_summary+meta_purchase_summary)
    new_token_purchase.total_cost=total_cost
    if player_initiated is False:
        new_token_purchase.completed_purchase=True
    app.tables.db_handle.session.commit()
    return new_token_purchase,purchase_summary+meta_purchase_summary

#FIXME : Better name for this
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

def calculate_cost_of_single_ticket_count(amount,player,flask_app,meta_tournament=None,tournament=None):
    calculated_list = calculate_list_of_tickets_and_prices_for_player(0, player,
                                                                      flask_app, meta_tournament=meta_tournament,
                                                                      tournament=tournament)
    return [calculated_cost for calculated_cost in calculated_list if int(calculated_cost['amount'])==int(amount)][0]
    
def calculate_list_of_tickets_and_prices_for_player(current_ticket_count, player,
                                                    flask_app, meta_tournament=None,
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

    if flask_app.tables.TournamentMachines.query.filter_by(player_id=player.player_id).first():
        current_ticket_amount=current_ticket_amount+1
    if player.team_id and flask_app.tables.TournamentMachines.query.filter_by(team_id=player.team_id).first():
        current_ticket_amount=current_ticket_amount+1        
    cutoff_index=tournament.number_of_unused_tickets_allowed-current_ticket_count
    return [{'amount':0,'price':0}]+output_list[0:cutoff_index]

#FIXME : should this info come as part of the GET /player instead of as a seperate get?
@blueprints.event_blueprint.route('/token/player_id/<player_id>',methods=['GET'])
@load_tables
def get_player_tokens_count(tables,player_id):                
    player = tables.Players.query.filter_by(player_id=player_id).first()
    token_count_per_tournament=[]
    token_count_per_meta_tournament=[]
    tournament_ticket_prices=[]
    meta_tournament_ticket_prices=[]
    
    for tournament in tables.Tournaments.query.filter_by(meta_tournament_id=None).all():
        count = token_helpers.get_number_of_unused_tickets_for_player(player,current_app,tournament=tournament)
        token_count_per_tournament.append({'tournament_name':tournament.tournament_name,
                                           'tournament_id':tournament.tournament_id,
                                           'count':count})
        tournament_ticket_prices.append(calculate_list_of_tickets_and_prices_for_player(count,
                                                                                        player,
                                                                                        current_app,
                                                                                        tournament=tournament))        
    for meta_tournament in tables.MetaTournaments.query.all():
        count = token_helpers.get_number_of_unused_tickets_for_player(player,current_app,meta_tournament=meta_tournament)
        token_count_per_meta_tournament.append({'meta_tournament_name':meta_tournament.meta_tournament_name,
                                                'meta_tournament_id':meta_tournament.meta_tournament_id,
                                                'count':count})
        meta_tournament_ticket_prices.append(calculate_list_of_tickets_and_prices_for_player(count,
                                                                                             player,
                                                                                             current_app,
                                                                                             meta_tournament=meta_tournament))
        
    return jsonify({'tournament_token_count':token_count_per_tournament,
                    'meta_tournament_token_count':token_count_per_meta_tournament,
                    'tournament_ticket_prices':tournament_ticket_prices,
                    'meta_tournament_ticket_prices':meta_tournament_ticket_prices})


@blueprints.event_blueprint.route('/token',methods=['POST'])
@player_buy_tickets_permissions.require(403)
@check_current_user_is_active
@load_tables
def player_purchase_tokens(tables):
    player = current_app.tables.Players.query.filter_by(player_id=current_user.player_id).first()
    if player is None:
        raise BadRequest('player does not exist')
    new_token_purchase,purchase_summary = purchase_tickets_route(request,player,current_app,player_initiated=True)
    generic_serializer = generate_generic_serializer(serializer.generic.ALL)
    return jsonify({'new_token_purchase':generic_serializer(new_token_purchase),
                    'purchase_summary':purchase_summary,
                    'total_cost':new_token_purchase.total_cost})


@blueprints.event_blueprint.route('/token/player_id/<player_id>',methods=['POST'])
@event_user_buy_tickets_permissions.require(403)
@check_current_user_is_active
@load_tables
def event_user_purchase_tokens(tables,player_id):
    player = current_app.tables.Players.query.filter_by(player_id=player_id).first()
    if player is None:
        raise BadRequest('player does not exist')
    new_token_purchase,purchase_summary = purchase_tickets_route(request,player,current_app,player_initiated=False)
    #total_cost = sum(int(summary[2]['price']) for summary in purchase_summary)
    generic_serializer = generate_generic_serializer(serializer.generic.ALL)
    return jsonify({'new_token_purchase':generic_serializer(new_token_purchase),
                    'purchase_summary':purchase_summary,
                    'total_cost':new_token_purchase.total_cost})
