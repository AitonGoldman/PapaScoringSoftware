from flask_restless.helpers import to_dict
from lib.flask_lib import blueprints
from flask import jsonify,current_app,request
from werkzeug.exceptions import BadRequest,Unauthorized,Conflict
from flask_login import login_user, logout_user, current_user
import json
from lib import orm_factories
from lib.serializer.generic import generate_generic_serializer
from lib import serializer
from lib.route_decorators.db_decorators import load_tables
from sqlalchemy.orm import joinedload

def get_discount_price(tournament):
    if tournament.use_stripe:
        return tournament.discount_stripe_price
    else:
        return tournament.discount_price

def get_price(tournament):
    if tournament.use_stripe:
        return tournament.stripe_price
    else:
        return tournament.manually_set_price
    
def calculate_list_of_tickets_and_prices_for_player(current_ticket_count,
                                                    player,
                                                    flask_app,
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

    if flask_app.tables.TournamentMachines.query.filter_by(player_id=player.player_id).first():
        current_ticket_amount=current_ticket_amount+1
    if player.team_id and flask_app.tables.TournamentMachines.query.filter_by(team_id=player.team_id).first():
        current_ticket_amount=current_ticket_amount+1        
    cutoff_index=tournament.number_of_unused_tickets_allowed-current_ticket_count
    return [{'amount':0,'price':0}]+output_list[0:cutoff_index]
    
        
    
def get_number_of_unused_tickets_for_player(player,flask_app,meta_tournament=None,tournament=None):
    #FIXME : explore if it makes sense to query al tokens (for all divisions) at once
    query = flask_app.tables.Tokens.query.filter_by(used=False,voided=False,paid_for=True,deleted=False)
    if player.team_id is None and tournament and tournament.team_tournament:
        return 0
    if tournament:
        if tournament.team_tournament is True:
            token_count = query.filter_by(tournament_id=tournament.tournament_id,team_id=player.team_id).count()            
        else:            
            token_count = query.filter_by(player_id=player.player_id,tournament_id=tournament.tournament_id).count()
    if meta_tournament:
        token_count = query.filter_by(meta_tournament_id=meta_tournament.meta_tournament_id).count()    
    return token_count
        
@blueprints.event_blueprint.route('/token/<player_id>',methods=['GET'])
@load_tables
def get_player_tokens_count(tables,player_id):                
    player = tables.Players.query.filter_by(player_id=player_id).first()
    token_count_per_tournament=[]
    token_count_per_meta_tournament=[]
    tournament_ticket_prices=[]
    meta_tournament_ticket_prices=[]
    
    for tournament in tables.Tournaments.query.filter_by(meta_tournament_id=None).all():
        count = get_number_of_unused_tickets_for_player(player,current_app,tournament=tournament)
        token_count_per_tournament.append({tournament.tournament_id:count})
        tournament_ticket_prices.append(calculate_list_of_tickets_and_prices_for_player(count,
                                                                                        player,
                                                                                        current_app,
                                                                                        tournament=tournament))        
    for meta_tournament in tables.MetaTournaments.query.all():
        count = get_number_of_unused_tickets_for_player(player,current_app,meta_tournament=meta_tournament)
        token_count_per_meta_tournament.append({meta_tournament.meta_tournament_id:count})
        meta_tournament_ticket_prices.append(calculate_list_of_tickets_and_prices_for_player(count,
                                                                                        player,
                                                                                        current_app,
                                                                                        meta_tournament=meta_tournament))        
        
    return jsonify({'tournament_token_count':token_count_per_tournament,
                    'meta_tournament_token_count':token_count_per_meta_tournament,
                    'tournament_ticket_prices':tournament_ticket_prices,
                    'meta_tournament_ticket_prices':meta_tournament_ticket_prices})


