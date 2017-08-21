from lib.flask_lib import blueprints
from flask import jsonify,current_app,request
from werkzeug.exceptions import BadRequest,Unauthorized
import json
from lib.serializer.division import  generate_division_to_dict_serializer
from lib import serializer,stripe_lib
from lib.route_decorators.db_decorators import load_tables
from sqlalchemy.orm import joinedload

def edit_division_queuing(division,input_data):
    if 'queueing' in input_data and input_data['queuing'] is True:
        division.queuing=True
    else:
        division.queuing=False
    if 'num_spaces_to_bump_player_down_queue' in input_data:
        division.num_spaces_to_bump_player_down_queue=input_data['num_spaces_to_bump_player_down_queue']

def edit_division_ticket_info(division,input_data,app):
    if 'use_stripe' in input_data and input_data['use_stripe'] is True:
        division.use_stripe=True        
    else:
        division.use_stripe=False
    if division.use_stripe and 'stripe_sku' not in input_data:
        raise BadRequest('No stripe sku submitted')
    if division.use_stripe:
        division.manually_set_price=None
        division.discount_price=None        
        stripe_price = stripe_lib.get_sku_price(input_data['stripe_sku'],app.event_config['stripe_api_key'])
        division.stripe_sku=input_data['stripe_sku']
        division.stripe_price=stripe_price
    if division.use_stripe and 'discount_stripe_sku' in input_data:
        discount_stripe_price = stripe_lib.get_sku_price(input_data['discount_stripe_sku'],app.event_config['stripe_api_key'])
        division.discount_stripe_sku=input_data['discount_stripe_sku']
        division.discount_stripe_price=discount_stripe_price        
    if division.use_stripe is not True:
        division.stripe_price = None
        division.stripe_sku = None
        division.discount_stripe_price = None
        division.discount_stripe_sku = None
        
        if 'manually_set_price' in input_data:
            division.manually_set_price=input_data['manually_set_price']
        if 'discount_price' in input_data:
            division.discount_price=input_data['discount_price']
    if 'number_of_tickets_for_discount' in input_data:
        division.number_of_tickets_for_discount=input_data['number_of_tickets_for_discount']
    else:
        division.number_of_tickets_for_discount=None
        
    if 'number_of_unused_tickets_allowed' in input_data:
            division.number_of_unused_tickets_allowed=input_data['number_of_unused_tickets_allowed']        

def edit_division_scoring(division,input_data):
    if 'active' in input_data and input_data['active'] is True:
        division.active=True
    else:
        division.active=False

    if 'scoring_style' in input_data:
        division.scoring_style=input_data['scoring_style']

    if division.scoring_style=="HERB":
        if 'limited_herb' in input_data:
            division.limited_herb=True
        else:
            division.limited_herb=False
    if 'number_of_signifigant_scores' in input_data:
        division.number_of_signifigant_scores=input_data['number_of_signifigant_scores']
        
    if 'ifpa_rank_restriction' in input_data:
        division.ifpa_rank_restriction=input_data['ifpa_rank_restriction']

    if 'team_tournament' in input_data and input_data['team_tournament'] is True:
        division.team_tournament=True
    else:
        division.team_tournament=False

def edit_division_finals(division,input_data):
    if 'finals_style' in input_data:
        division.finals_style=input_data['finals_style']
    if 'number_of_qualifiers' in input_data:
        division.number_of_qualifiers=input_data['number_of_qualifiers']
    if 'number_of_qualifiers_for_a_when_finals_style_is_ppo' in input_data:
        division.number_of_qualifiers_for_a_when_finals_style_is_ppo=input_data['number_of_qualifiers_for_a_when_finals_style_is_ppo']
    if 'number_of_qualifiers_for_b_when_finals_style_is_ppo' in input_data:
        division.number_of_qualifiers_for_b_when_finals_style_is_ppo=input_data['number_of_qualifiers_for_b_when_finals_style_is_ppo']
    if 'number_of_games_played_in_each_finals_match' in input_data:
        division.number_of_games_played_in_each_finals_match=input_data['number_of_games_played_in_each_finals_match']
    if 'style_of_points_assigned_during_finals' in input_data:
        division.style_of_points_assigned_during_finals=input_data['style_of_points_assigned_during_finals']
        
    pass
            
def create_division_route(request,tables):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Username or password not specified')
    if 'division_name' not in input_data:
        raise BadRequest('Missing information')        
    existing_division = tables.Divisions.query.filter_by(division_name=input_data['division_name']).first()
    if existing_division:
        raise BadRequest('Trying to use an already used name for division')        
    new_division = tables.Divisions(division_name=input_data['division_name'])
    tables.db_handle.session.add(new_division)
    if 'tournament_id' in input_data:
        existing_tournament = tables.Tournaments.query.filter_by(tournament_id=input_data['tournament_id']).first()
        if existing_tournament:
            new_division.tournament=existing_tournament
            new_division.tournament_name=existing_tournament.tournament_name+" "+new_division.division_name
        else:
            raise BadRequest('Bad tournament id')            
    tables.db_handle.session.commit()
    return new_division

@blueprints.event_blueprint.route('/division',methods=['POST'])
@load_tables
def create_division(tables):    
    new_division = create_division_route(request,tables)
    division_serializer = generate_division_to_dict_serializer(serializer.division.ALL)
    return jsonify({'new_division':division_serializer(new_division)})

@blueprints.event_blueprint.route('/division/<division_id>',methods=['PUT'])
@load_tables
def edit_division(tables,division_id):    
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Username or password not specified')
    division = tables.Divisions.query.filter_by(division_id=division_id).first()
    if division is None:
        raise BadRequest('Bad division submitted')
    edit_division_queuing(division,input_data)
    edit_division_ticket_info(division,input_data,current_app)    
    edit_division_scoring(division,input_data)
    edit_division_finals(division,input_data)    
    tables.db_handle.session.commit()
    division_serializer = generate_division_to_dict_serializer(serializer.division.ALL)
    return jsonify({'edited_division':division_serializer(division)})
