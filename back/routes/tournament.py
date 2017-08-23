from lib.flask_lib import blueprints
from flask import jsonify,current_app,request
from werkzeug.exceptions import BadRequest,Unauthorized
import json
from lib.serializer.generic import  generate_generic_serializer
from lib.serializer.tournament import  generate_tournament_to_dict_serializer
from lib import serializer,stripe_lib
from lib import serializer
from lib.route_decorators.db_decorators import load_tables
from sqlalchemy.orm import joinedload
from lib.flask_lib.permissions import create_tournament_permissions
from lib.serializer.deserialize import deserialize_json
from lib import orm_factories

def edit_tournament_route(tournament,input_data,app):
    deserialize_json(tournament,input_data,app)
    if tournament.use_stripe:
        if app.event_config['stripe_api_key'] is None:
            raise BadRequest('oops - you forgot to set your stripe API key for the event')

        tournament.manually_set_price=None
        tournament.discount_price=None
        stripe_price = stripe_lib.get_sku_price(input_data['stripe_sku'],app.event_config['stripe_api_key'])
        tournament.stripe_price=stripe_price        
    if tournament.use_stripe and 'discount_stripe_sku' in input_data:
        discount_stripe_price = stripe_lib.get_sku_price(input_data['discount_stripe_sku'],app.event_config['stripe_api_key'])
        tournament.discount_stripe_price=discount_stripe_price        
    if tournament.use_stripe is not True:
        tournament.stripe_price = None
        tournament.stripe_sku = None
        tournament.discount_stripe_price = None
        tournament.discount_stripe_sku = None
            
def create_tournament_route(request,app):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Username or password not specified')
    if 'tournament_name' not in input_data:
        raise BadRequest('Missing information')        
    existing_tournament = app.tables.Tournaments.query.filter_by(tournament_name=input_data['tournament_name']).first()
    if existing_tournament:
        raise BadRequest('Trying to use an already used name for tournament')
    multi_division_tournament_name = input_data.get('multi_division_tournament_name',None)
    multi_division_tournament_id = input_data.get('multi_division_tournament_id',None)
    
    new_tournament = orm_factories.create_tournament(app,
                                                     input_data['tournament_name'],
                                                     multi_division_tournament_name,
                                                     multi_division_tournament_id)    
    app.tables.db_handle.session.commit()
    return new_tournament

@blueprints.event_blueprint.route('/tournament',methods=['POST'])
@load_tables
def create_tournament(tables):    
    new_tournament = create_tournament_route(request,current_app)
    tournament_serializer = generate_tournament_to_dict_serializer(serializer.tournament.ALL)
    return jsonify({'new_tournament':tournament_serializer(new_tournament)})

@blueprints.event_blueprint.route('/tournament/<tournament_id>',methods=['PUT'])
@load_tables
def edit_tournament(tables,tournament_id):    
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Username or password not specified')
    tournament = tables.Tournaments.query.filter_by(tournament_id=tournament_id).first()
    if tournament is None:
        raise BadRequest('Bad tournament submitted')
    edit_tournament_route(tournament,input_data,current_app)
    tables.db_handle.session.commit()
    tournament_serializer = generate_tournament_to_dict_serializer(serializer.tournament.ALL)
    return jsonify({'edited_tournament':tournament_serializer(tournament)})


# def create_tournament_route(request,tables):
#     if request.data:        
#         input_data = json.loads(request.data)
#     else:
#         raise BadRequest('Username or password not specified')
#     if 'tournament_name' not in input_data:
#         raise BadRequest('Missing information')
#     existing_tournament = tables.Tournaments.query.filter_by(tournament_name=input_data['tournament_name']).first()
#     if existing_tournament:
#         raise BadRequest('Trying to use an already used name for tournament')        
#     new_tournament = tables.Tournaments(tournament_name=input_data['tournament_name'])
#     tables.db_handle.session.add(new_tournament)
#     tables.db_handle.session.commit()
#     return new_tournament

# @blueprints.event_blueprint.route('/tournament',methods=['POST'])
# @create_tournament_permissions.require(403)
# @load_tables
# def create_tournament(tables):    
#     new_tournament = create_tournament_route(request,tables)
#     generic_serializer = generate_generic_serializer(serializer.generic.ALL)
#     return jsonify({'new_tournament':generic_serializer(new_tournament)})
