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
from lib.route_decorators.auth_decorators import check_current_user_is_active


@blueprints.event_blueprint.route('/multi_tournament',methods=['POST'])
@create_tournament_permissions.require(403)
@check_current_user_is_active
@load_tables
def create_mutli_tournament(tables):    
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Missing information')
    if 'number_of_divisions' not in request.data or 'multi_division_tournament_name' not in request.data:
        raise BadRequest('Missing information')
    existing_multi_division_tournament = tables.MultiDivisionTournaments.query.filter_by(multi_division_tournament_name=input_data['multi_division_tournament_name']).first()
    if existing_multi_division_tournament:
        raise BadRequest('Multi division tournament already created')        
    new_multi_division_tournament = orm_factories.create_multi_tournament(current_app,input_data['multi_division_tournament_name'],int(input_data['number_of_divisions']))
    tables.db_handle.session.commit()    
    multi_division_tournament_serializer = generate_generic_serializer(serializer.tournament.ALL)
    return jsonify({'multi_division_tournament':multi_division_tournament_serializer(new_multi_division_tournament)})



@blueprints.event_blueprint.route('/multi_tournament',methods=['GET'])
@load_tables
def get_multi_tournaments(tables):    
    multi_division_tournament = tables.MultiDivisionTournaments.query.first()
    if multi_division_tournament is None:
        tournaments = []
    else:
        tournaments = tables.Tournaments.query.filter_by(multi_division_tournament_id=multi_division_tournament.multi_division_tournament_id).all()
    event = tables.Events.query.filter_by(name=current_app.name).first()
    event_serializer = serializer.event.generate_event_to_dict_serializer(serializer.event.MINIMUM_EVENT)        
    #multi_division_tournament_serializer = generate_generic_serializer(serializer.generic.ALL)
    tournament_serializer = generate_tournament_to_dict_serializer(serializer.tournament.ALL)
    return_message = {'multi_division_tournaments':[tournament_serializer(tournament) for tournament in tournaments],
                      'event': event_serializer(event)}    
    return jsonify(return_message)

