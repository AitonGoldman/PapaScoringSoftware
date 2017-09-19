from lib.flask_lib import blueprints
from flask import jsonify,current_app,request
from werkzeug.exceptions import BadRequest,Unauthorized
import json
from lib import serializer
from lib.serializer.generic import generate_generic_serializer
from lib.route_decorators.db_decorators import load_tables
from sqlalchemy.orm import joinedload
from lib.serializer.deserialize import deserialize_json
from lib.flask_lib.permissions import create_tournament_permissions
from lib.route_decorators.auth_decorators import check_current_user_is_active
from lib import orm_factories

@blueprints.event_blueprint.route('/machine',methods=['GET'])
@load_tables
def get_machines(tables):    
    machines = tables.Machines.query.all()
    machines_mapping_to_active_tournament_machines = tables.Machines.query.join(tables.TournamentMachines).filter(tables.TournamentMachines.active==True).all()
    machines_list = list(set(machines) - set(machines_mapping_to_active_tournament_machines))
    machine_serializer = generate_generic_serializer(serializer.generic.ALL)

    return jsonify({'machines':[machine_serializer(machine) for machine in machines_list]})
