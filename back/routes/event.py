
from flask import Flask
from lib.flask_lib import blueprints
from lib.flask_lib.permissions import create_pss_event_permissions
from flask import jsonify,current_app,request
from werkzeug.exceptions import BadRequest,Unauthorized,Conflict
from flask_login import login_user, logout_user, current_user
import json
from lib import roles
from lib.PssConfig import PssConfig
from lib.serializer.event import generate_events_serializer
from lib.route_decorators.db_decorators import load_tables
from pss_models.PssUsers import generate_pss_user_event_role_mapping
import os
from lib import orm_factories

@blueprints.pss_admin_event_blueprint.route('/event',methods=['POST'])
@load_tables
@create_pss_event_permissions.require(403)
def create_event(tables):                    
    
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Event details not specified')        
    if 'name' not in input_data:
        raise BadRequest('Information missing')
    if not input_data['name'].isalpha():
        raise BadRequest('Name specified has non alpha characters')
    pss_config=PssConfig()
    new_event_app = Flask(input_data['name'])
    new_event_tables = orm_factories.create_event_tables(pss_config,new_event_app)    

    new_event = orm_factories.create_event_route(current_user, tables, input_data, new_event_tables)    
    
    event_serializer = generate_events_serializer(current_app)    
    event_dict=event_serializer().dump(new_event).data    
    return jsonify({'new_event':event_dict})
 

