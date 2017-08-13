
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
from base64 import b64encode
import os

def create_event_tables(pss_config,new_event_app):
    #pss_config = PssConfig()
    new_event_tables = pss_config.get_db_info().getImportedTables(new_event_app,"pss_admin")    
    existing_event = new_event_tables.Events.query.filter_by(name=new_event_app.name).first()
    if existing_event is not None:
        raise Conflict('Event already exists')             
    new_event_tables.EventUsers.__table__.create(new_event_tables.db_handle.session.bind)
    new_event_tables.PssEventUsersRoles.__table__.create(new_event_tables.db_handle.session.bind)                
    return new_event_tables

def create_event_route(user_creating_event, tables, input_data, new_event_tables):
    secret_key=b64encode(os.urandom(24)).decode('utf-8')        
    new_event = tables.Events(name=input_data['name'],flask_secret_key=secret_key)    
    tables.db_handle.session.add(new_event)
    new_event_user = new_event_tables.EventUsers(pss_user_id=user_creating_event.pss_user_id,
                                                 password_crypt=user_creating_event.event_user.password_crypt)
    td_role = tables.EventRoles.query.filter_by(name=roles.TOURNAMENT_DIRECTOR).first()
    
    new_event_user_td_role = new_event_tables.PssEventUsersRoles(pss_user_id=user_creating_event.pss_user_id,
                                                                 event_role_id=td_role.event_role_id)
    
    new_event_tables.db_handle.session.add(new_event_user)
    new_event_tables.db_handle.session.add(new_event_user_td_role)    

    user_creating_event.events.append(new_event)
    new_event_tables.db_handle.session.commit()
    tables.db_handle.session.commit()        
    return new_event

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
    new_event_tables = create_event_tables(pss_config,new_event_app)    

    new_event = create_event_route(current_user, tables, input_data, new_event_tables)    
    
    
    event_serializer = generate_events_serializer(current_app)    
    event_dict=event_serializer().dump(new_event).data    
    return jsonify({'new_event':event_dict})
 

