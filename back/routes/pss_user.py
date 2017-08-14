from lib.flask_lib import blueprints
from lib.flask_lib.permissions import create_pss_event_user_permissions, create_pss_user_permissions
from flask import jsonify,current_app,request
from werkzeug.exceptions import BadRequest,Unauthorized,Conflict
from flask_login import login_user, logout_user, current_user
import json
from lib import roles
from lib.serializer.pss_user import generate_pss_user_serializer
from lib.route_decorators.db_decorators import load_tables

def create_pss_user_route(tables,request, app):            
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Username or password not specified')        
    if 'username' not in input_data or 'password' not in input_data:        
        raise BadRequest('Information missing')
    if 'event_role_id' not in input_data and 'role_id' not in input_data:
        raise BadRequest('Information missing')        
    existing_user=tables.PssUsers.query.filter_by(username=input_data['username']).first()
    #FIXME : needs to be more extensive of a check (i.e. check actual name, etc)
    if existing_user is not None:
        raise Conflict('User already exists.')
    new_user = tables.PssUsers(username=input_data['username'])
    event_user = tables.EventUsers()
    event_user.crypt_password(input_data['password'])
    new_user.event_user=event_user    
    if 'role_id' in input_data:
        pss_user_role = tables.AdminRoles.query.filter_by(admin_role_id=int(input_data['role_id'])).first()
        if pss_user_role is None:
            raise BadRequest('Role specified does not exist')        
        new_user.admin_roles.append(pss_user_role)
    if 'event_role_id' in input_data:
        event = tables.Events.query.filter_by(name=app.name).first()
        new_user.events.append(event)        
        pss_event_user_role = tables.EventRoles.query.filter_by(event_role_id=int(input_data['event_role_id'])).first()
        if pss_event_user_role is None:
            raise BadRequest('Role specified does not exist')        
        new_user.event_roles.append(pss_event_user_role)
    tables.db_handle.session.add(new_user)
    tables.db_handle.session.commit()
    return new_user

@blueprints.pss_admin_event_blueprint.route('/pss_user',methods=['POST'])
@load_tables
@create_pss_user_permissions.require(403)
def create_pss_user(tables):    
    new_user = create_pss_user_route(tables,request,current_app)
    pss_user_serializer = generate_pss_user_serializer(current_app)    
    user_dict=pss_user_serializer().dump(new_user).data    
    return jsonify({'new_pss_user':user_dict})

@blueprints.event_blueprint.route('/pss_user',methods=['POST'])
@load_tables
@create_pss_event_user_permissions.require(403)
def create_pss_event_user(tables):        
    #FIXME : protect against duplicate users
    if 'role_id' in json.loads(request.data):
        raise BadRequest('Naughty Naughty')
    new_user = create_pss_user_route(tables,request,current_app)
    pss_user_serializer = generate_pss_user_serializer(current_app)    
    user_dict=pss_user_serializer().dump(new_user).data    
    return jsonify({'new_pss_user':user_dict})
    
