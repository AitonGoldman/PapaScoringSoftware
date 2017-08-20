from lib.flask_lib import blueprints
from flask import jsonify,current_app,request
from werkzeug.exceptions import BadRequest,Unauthorized
import json
from lib.serializer.generic import  generate_generic_serializer
from lib import serializer
from lib.route_decorators.db_decorators import load_tables
from sqlalchemy.orm import joinedload
from lib.flask_lib.permissions import create_tournament_permissions

def create_tournament_route(request,tables):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Username or password not specified')
    if 'tournament_name' not in input_data:
        raise BadRequest('Missing information')
    existing_tournament = tables.Tournaments.query.filter_by(tournament_name=input_data['tournament_name']).first()
    if existing_tournament:
        raise BadRequest('Trying to use an already used name for tournament')        
    new_tournament = tables.Tournaments(tournament_name=input_data['tournament_name'])
    tables.db_handle.session.add(new_tournament)
    tables.db_handle.session.commit()
    return new_tournament

@blueprints.event_blueprint.route('/tournament',methods=['POST'])
@create_tournament_permissions.require(403)
@load_tables
def create_tournament(tables):    
    new_tournament = create_tournament_route(request,tables)
    generic_serializer = generate_generic_serializer(serializer.generic.ALL)
    return jsonify({'new_tournament':generic_serializer(new_tournament)})
