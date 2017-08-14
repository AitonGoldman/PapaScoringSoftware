from lib.PssConfig import PssConfig
from werkzeug.exceptions import BadRequest,Unauthorized,Conflict
from base64 import b64encode
import os
from lib import roles_constants

#FIXME : move this back to route
def create_event_route(user_creating_event, tables, input_data, new_event_tables):
    secret_key=b64encode(os.urandom(24)).decode('utf-8')        
    new_event = tables.Events(name=input_data['name'],flask_secret_key=secret_key)    
    tables.db_handle.session.add(new_event)
    new_event_user = new_event_tables.EventUsers(pss_user_id=user_creating_event.pss_user_id,
                                                 password_crypt=user_creating_event.event_user.password_crypt)
    td_role = new_event_tables.EventRoles.query.filter_by(name=roles_constants.TOURNAMENT_DIRECTOR).first()
    
    existing_user_in_new_event = new_event_tables.PssUsers.query.filter_by(pss_user_id=user_creating_event.pss_user_id).first()
    existing_user_in_new_event.event_roles.append(td_role)
    new_event_tables.db_handle.session.add(new_event_user)
    user_creating_event.events.append(new_event)
    new_event_tables.db_handle.session.commit()
    tables.db_handle.session.commit()        
    return new_event

def create_event_tables(pss_config,new_event_app):
    new_event_tables = pss_config.get_db_info().getImportedTables(new_event_app,"pss_admin")    
    existing_event = new_event_tables.Events.query.filter_by(name=new_event_app.name).first()
    if existing_event is not None:
        raise Conflict('Event already exists')             
    metadata = new_event_tables.db_handle.metadata
    event_role_pss_user_table = metadata.tables['event_role_pss_user_'+new_event_app.name]
    event_role_pss_user_table.create(new_event_tables.db_handle.session.bind)
    new_event_tables.EventUsers.__table__.create(new_event_tables.db_handle.session.bind)    

    return new_event_tables

def create_user(flask_app,username,password,roles,commit=False):
    tables=flask_app.tables
    user = tables.PssUsers(username=username)
    event_user = tables.EventUsers()
    event_user.crypt_password(password)
    user.event_user = event_user
    tables.db_handle.session.add(user)
    for role in roles:
        user.admin_roles.append(role)        
    if commit:
        tables.db_handle.session.commit()

