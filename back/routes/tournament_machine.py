from lib.flask_lib import blueprints
from flask import jsonify,current_app,request
from werkzeug.exceptions import BadRequest,Unauthorized
import json
from lib.serializer.tournament_machine import generate_tournament_machine_to_dict_serializer
from lib import serializer
from lib.serializer.generic import generate_generic_serializer
from lib.route_decorators.db_decorators import load_tables
from sqlalchemy.orm import joinedload
from lib.serializer.deserialize import deserialize_json
from lib.flask_lib.permissions import create_tournament_permissions
from lib.route_decorators.auth_decorators import check_current_user_is_active
from lib import orm_factories

def edit_tournament_machine_route(tournament_machine_id,request,app):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Username or password not specified')
    existing_tournament_machine = app.tables.TournamentMachines.query.filter_by(tournament_machine_id=tournament_machine_id).first()    
    if existing_tournament_machine is None:
        raise BadRequest('Bad tournament machine submitted')
    print input_data
    deserialize_json(existing_tournament_machine,input_data,app)    
    if existing_tournament_machine.removed:
         existing_tournament_machine.removed=True
         existing_tournament_machine.active=False
         
    return existing_tournament_machine

#def create_tournament_machine_route(request,app):
def create_tournament_machine_route(machine_id,tournament_id,app):
    existing_tournament_machine = app.tables.TournamentMachines.query.filter_by(machine_id=machine_id).first()
    if existing_tournament_machine:
        if existing_tournament_machine.removed is False:
            raise BadRequest('Trying to add an already added machine')
        else:
            existing_tournament_machine.removed = False
            existing_tournament_machine.active = True
            return existing_tournament_machine
            
    existing_tournament = app.tables.Tournaments.query.filter_by(tournament_id=tournament_id).first()
    existing_machine = app.tables.Machines.query.filter_by(machine_id=machine_id).first()
    if existing_tournament is None or existing_machine is None:
        raise BadRequest('Trying to add to a bad tournament, or trying to add a bad machine')        

    new_tournament_machine = app.tables.TournamentMachines(machine_id=machine_id,
                                                   tournament_machine_name=existing_machine.machine_name,
                                                   tournament_machine_abbreviation=existing_machine.abbreviation,
                                                   active=True)    
    app.tables.db_handle.session.add(new_tournament_machine)
    existing_tournament.tournament_machines.append(new_tournament_machine)    
    if existing_tournament_machine is None:        
        orm_factories.create_queue_for_tournament_machine(app,new_tournament_machine,existing_tournament.queue_size)
    existing_event = app.tables.Events.query.filter_by(event_id=existing_tournament.event_id).first()
    existing_event.wizard_configured = True
    #app.tables.db_handle.session.commit()
    

    return new_tournament_machine

@blueprints.event_blueprint.route('/tournament_machine',methods=['POST'])
@create_tournament_permissions.require(403)
@check_current_user_is_active
@load_tables
def create_tournament_machine(tables):    
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('info not specified')
    
    tournament_id = input_data['tournament_id']
    print "tournament id is %s" % tournament_id
    new_tournament_machines = []
    serialized_new_tournament_machines = []
    tournament_machine_serializer = generate_generic_serializer(serializer.generic.ALL)
    for tournament_machine in input_data['tournament_machines']:            
        new_tournament_machine = create_tournament_machine_route(tournament_machine['machine_id'],tournament_id,current_app)            
        new_tournament_machines.append(new_tournament_machine)
    tables.db_handle.session.commit()
    for tournament_machine in new_tournament_machines:
        serialized_new_tournament_machines.append(tournament_machine_serializer(tournament_machine))    
    return jsonify({'new_tournament_machines':serialized_new_tournament_machines})

@blueprints.event_blueprint.route('/tournament_machine/<tournament_machine_id>',methods=['PUT'])
@create_tournament_permissions.require(403)
@check_current_user_is_active
@load_tables
def edit_tournament_machine(tables,tournament_machine_id):    
    edited_tournament_machine = edit_tournament_machine_route(tournament_machine_id,request,current_app)    
    tables.db_handle.session.commit()
    #tournament_machine_serializer = generate_generic_serializer(serializer.generic.ALL)
    tournament_machine_serializer = generate_tournament_machine_to_dict_serializer(serializer.generic.ALL)

    return jsonify({'item':tournament_machine_serializer(edited_tournament_machine)})
    

