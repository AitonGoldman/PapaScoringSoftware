
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

@blueprints.pss_admin_event_blueprint.route('/event',methods=['POST'])
@load_tables
@create_pss_event_permissions.require(403)
def create_event(tables):                    
    #FIXME : need utility functions to find and drop orphaned tables
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Event details not specified')        
    if 'name' not in input_data:
        raise BadRequest('Information missing')
    if not input_data['name'].isalpha():
        raise BadRequest('Name specified has non alpha characters')
    existing_event = tables.Events.query.filter_by(name=input_data['name']).first()
    if existing_event is not None:
        raise Conflict('Event already exists')        
    new_event = tables.Events(name=input_data['name'])    
    tables.db_handle.session.add(new_event)
    new_event_app = Flask(input_data['name'])
    pss_config = PssConfig()
    #FIXME : configure admin name passed to importedtables
    new_event_tables = pss_config.get_db_info().getImportedTables(new_event_app,"pss_admin")    
    new_event_tables.EventUsers.__table__.create(new_event_tables.db_handle.session.bind)        
    tables.db_handle.session.commit()
    event_serializer = generate_events_serializer(current_app)    
    event_dict=event_serializer().dump(new_event).data    
    return jsonify({'new_event':event_dict})
 

