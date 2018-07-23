from lib.flask_lib import blueprints
from flask import jsonify,current_app,request
from werkzeug.exceptions import BadRequest,Unauthorized
import json
from lib.serializer.division import  generate_division_to_dict_serializer
from lib import serializer,stripe_lib
from lib.serializer.deserialize import deserialize_json
from lib.route_decorators.db_decorators import load_tables
from sqlalchemy.orm import joinedload


def edit_division_route(division,input_data,app):
    deserialize_json(division,input_data,app)
    if division.use_stripe:
        division.manually_set_price=None
        division.discount_price=None
        stripe_price = stripe_lib.get_sku_price(input_data['stripe_sku'],app.event_config['stripe_api_key'])
        division.stripe_price=stripe_price        
    if division.use_stripe and 'discount_stripe_sku' in input_data:        
        discount_stripe_price = stripe_lib.get_sku_price(input_data['discount_stripe_sku'],app.event_config['stripe_api_key'])
        division.discount_stripe_price=discount_stripe_price        
    if division.use_stripe is not True:
        division.stripe_price = None
        division.stripe_sku = None
        division.discount_stripe_price = None
        division.discount_stripe_sku = None
            
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
    edit_division_route(division,input_data,current_app)
    tables.db_handle.session.commit()
    division_serializer = generate_division_to_dict_serializer(serializer.division.ALL)
    return jsonify({'edited_division':division_serializer(division)})
