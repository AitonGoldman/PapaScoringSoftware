from lib.flask_lib import blueprints
from flask import jsonify,current_app,request
from werkzeug.exceptions import BadRequest,Unauthorized
import json
from lib.serializer.generic import  generate_generic_serializer
from lib import serializer,stripe_lib
from lib import serializer
from lib.route_decorators.db_decorators import load_tables
from sqlalchemy.orm import joinedload
from lib.flask_lib.permissions import create_tournament_permissions
from lib.serializer.deserialize import deserialize_json
from lib import orm_factories
from lib.route_decorators.auth_decorators import check_current_user_is_active
from routes.tournament import get_tournament_field_descriptions,edit_tournament_route
from lib.serializer.tournament import  generate_tournament_to_dict_serializer

            
def create_meta_tournament_route(request,app):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Information not specified')
    if 'meta_tournament_name' not in input_data:
        raise BadRequest('Missing meta tournament name')
    if input_data['meta_tournament_name'] == "":
        raise BadRequest('Missing meta tournament name')    
    existing_meta_tournament = app.tables.MetaTournaments.query.filter_by(meta_tournament_name=input_data['meta_tournament_name']).first()
    if existing_meta_tournament:
        raise BadRequest('Trying to use an already used name for a meta tournament')
    tournaments_to_include = []
    new_meta_tournament =   app.tables.MetaTournaments()
    new_meta_tournament.meta_tournament_name=input_data['meta_tournament_name']
    app.tables.db_handle.session.add(new_meta_tournament)
    for tournament_id in input_data['tournament_ids']:
        tournaments_to_include.append(app.tables.Tournaments.query.filter_by(tournament_id=tournament_id).first())        
    new_meta_tournament.tournaments = tournaments_to_include
    app.tables.db_handle.session.commit()
    return new_meta_tournament

@blueprints.event_blueprint.route('/meta_tournament',methods=['POST'])
@create_tournament_permissions.require(403)
@check_current_user_is_active
@load_tables
def create_meta_tournament(tables):    
    new_meta_tournament = create_meta_tournament_route(request,current_app)
    generic_serializer = generate_generic_serializer(serializer.generic.ALL)
    new_meta_tournament_dict=generic_serializer(new_meta_tournament)        
    return jsonify({'new_meta_tournament':new_meta_tournament_dict})

@blueprints.event_blueprint.route('/meta_tournament/<meta_tournament_id>',methods=['GET'])
@load_tables
def get_meta_tournament(tables,meta_tournament_id):    
    meta_tournament = tables.MetaTournaments.query.filter_by(meta_tournament_id=meta_tournament_id).first()
    if meta_tournament is None:
        raise BadRequest('Bad meta_tournament requested')    
    #meta_tournament_serializer = generate_tournament_to_dict_serializer(serializer.tournament.ALL)
    meta_tournament_serializer = generate_generic_serializer(serializer.generic.ALL)
    return jsonify({'item':meta_tournament_serializer(meta_tournament),'descriptions':get_tournament_field_descriptions()})


@blueprints.event_blueprint.route('/meta_tournament/<meta_tournament_id>',methods=['PUT'])
@create_tournament_permissions.require(403)
@check_current_user_is_active
@load_tables
def edit_meta_tournament(tables,meta_tournament_id):    
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Username or password not specified')
    meta_tournament = tables.MetaTournaments.query.filter_by(meta_tournament_id=meta_tournament_id).first()
    if meta_tournament is None:
        raise BadRequest('Bad meta_tournament submitted')
    edit_tournament_route(meta_tournament,input_data,current_app)
    
    tables.db_handle.session.commit()
    #meta_tournament_serializer = generate_tournament_to_dict_serializer(serializer.tournament.ALL)
    meta_tournament_serializer = generate_generic_serializer(serializer.generic.ALL)
    return jsonify({'item':meta_tournament_serializer(meta_tournament)})

