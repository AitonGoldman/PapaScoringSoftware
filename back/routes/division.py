from lib.flask_lib import blueprints
from flask import jsonify,current_app,request
from werkzeug.exceptions import BadRequest,Unauthorized
import json
from lib.serializer.division import  generate_division_to_dict_serializer
from lib import serializer
from lib.route_decorators.db_decorators import load_tables
from sqlalchemy.orm import joinedload

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
