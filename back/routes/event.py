
from flask import Flask
from lib.flask_lib import blueprints
from lib.flask_lib.permissions import create_pss_event_permissions
from flask import jsonify,current_app,request
from werkzeug.exceptions import BadRequest,Unauthorized
from flask_login import login_user, logout_user, current_user
import json
from lib import roles
from lib.PssConfig import PssConfig
from lib.serializer.pss_user import generate_pss_user_serializer
from lib.route_decorators.db_decorators import load_tables

@blueprints.pss_admin_event_blueprint.route('/event',methods=['POST'])
@load_tables
@create_pss_event_permissions.require(403)
def create_event(tables):                    
    #FIXME : need to prevent duplicate events
    #FIXME : need utility functions to find and drop orphaned tables
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Event details not specified')        
    if 'name' not in input_data:
        raise BadRequest('Information missing')
    if not input_data['name'].isalpha():
        raise BadRequest('Name specified has non alpha characters')
    new_event = tables.Events(name=input_data['name'])    
    tables.db_handle.session.add(new_event)
    new_event_app = Flask(input_data['name'])
    pss_config = PssConfig()    
    new_event_tables = pss_config.get_db_info().getImportedTables(new_event_app,"pss_admin")    
    new_event_tables.PssEventUsers.__table__.create(new_event_tables.db_handle.session.bind)        
    # # - create entry in user table for event creator
    # # - write login for event users
    # # - maybe let the admin app have a app specific user table
    tables.db_handle.session.commit()
    return jsonify({})

