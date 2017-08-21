from lib.flask_lib import blueprints
from flask import jsonify,current_app,request
from werkzeug.exceptions import BadRequest,Unauthorized
import json
from lib.serializer.generic import  generate_generic_serializer
from lib import serializer
from lib.route_decorators.db_decorators import load_tables
from sqlalchemy.orm import joinedload

def edit_division_machine_route(division_machine_id,request,tables):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Username or password not specified')
    existing_division_machine = tables.DivisionMachines.query.filter_by(division_machine_id=division_machine_id).first()    
    if existing_division_machine is None:
        raise BadRequest('Bad division machine submitted')        
    if 'active' in input_data and input_data['active'] is True:
        existing_division_machine.active=True
    else:
        existing_division_machine.active=False

    if 'removed' in input_data and input_data['removed'] is True:
         existing_division_machine.removed=True
         existing_division_machine.active=False
    else:
        existing_division_machine.removed=False
    return existing_division_machine

def create_division_machine_route(request,tables):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Username or password not specified')
    if 'division_id' not in input_data or 'machine_id' not in input_data:
        raise BadRequest('Missing information')        
    existing_division_machine = tables.DivisionMachines.query.filter_by(machine_id=input_data['machine_id']).first()
    if existing_division_machine:
        if existing_division_machine.removed is False:
            raise BadRequest('Trying to add an already added machine')
        else:
            existing_division_machine.removed = False
            existing_division_machine.active = True
            return existing_division_machine
            
    existing_division = tables.Divisions.query.filter_by(division_id=input_data['division_id']).first()
    existing_machine = tables.Machines.query.filter_by(machine_id=input_data['machine_id']).first()
    if existing_division is None or existing_machine is None:
        raise BadRequest('Trying to add to a bad division, or trying to add a bad machine')        

    new_division_machine = tables.DivisionMachines(machine_id=input_data['machine_id'],
                                                   division_machine_name=existing_machine.machine_name,
                                                   division_machine_abbreviation=existing_machine.abbreviation,
                                                   active=True)    
    existing_division.division_machines.append(new_division_machine)    
    tables.db_handle.session.add(new_division_machine)
    tables.db_handle.session.commit()
    return new_division_machine

@blueprints.event_blueprint.route('/division_machine',methods=['POST'])
@load_tables
def create_division_machine(tables):    
    new_division_machine = create_division_machine_route(request,tables)
    division_machine_serializer = generate_generic_serializer(serializer.generic.ALL)
    return jsonify({'new_division_machine':division_machine_serializer(new_division_machine)})

@blueprints.event_blueprint.route('/division_machine/<division_machine_id>',methods=['PUT'])
@load_tables
def edit_division_machine(tables,division_machine_id):    
    edited_division_machine = edit_division_machine_route(division_machine_id,request,tables)    
    tables.db_handle.session.commit()
    division_machine_serializer = generate_generic_serializer(serializer.generic.ALL)
    return jsonify({'edited_division_machine':division_machine_serializer(edited_division_machine)})
    
