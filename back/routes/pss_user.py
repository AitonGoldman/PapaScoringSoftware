from lib.flask_lib import blueprints
from lib.flask_lib.permissions import create_pss_event_user_permissions, create_pss_user_permissions
from flask import jsonify,current_app,request
from werkzeug.exceptions import BadRequest,Unauthorized,Conflict
from flask_login import login_user, logout_user, current_user
import json
from lib orm_factories
from lib.serializer.pss_user import generate_pss_user_serializer
from lib.route_decorators.db_decorators import load_tables

#FIXME : tables not needed
def create_pss_user_route(request, app):            
    tables = app.tables
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('No info in request')        
    if 'username' not in input_data or 'password' not in input_data or 'first_name' not in input_data or 'last_name' not in input_data:        
        raise BadRequest('Information missing')
    if 'event_role_id' not in input_data and 'role_id' not in input_data:
        raise BadRequest('Information missing')
    if 'event_role_id' in input_data and 'role_id' in input_data:
        raise BadRequest('Naughty Naughty')        
    
    existing_user=tables.PssUsers.query.filter_by(username=input_data['username']).first()
    #FIXME : needs to be more extensive of a check (i.e. check actual name, etc)
    if existing_user is not None:
        raise Conflict('User already exists.')
    if 'role_id' in input_data:
        pss_user_role = tables.AdminRoles.query.filter_by(admin_role_id=int(input_data['role_id'])).first()
        if pss_user_role is None:
            raise BadRequest('Role specified does not exist')
        new_user = orm_factories.create_user(app,input_data['username'],
                                             input_data['first_name'],input_data['last_name'],
                                             input_data['password'],admin_roles=[pss_user_role])        
    if 'event_role_id' in input_data:
        pss_event_user_role = tables.EventRoles.query.filter_by(event_role_id=int(input_data['event_role_id'])).first()
        if pss_event_user_role is None:
            raise BadRequest('Role specified does not exist')
        new_user = orm_factories.create_user(app,input_data['username'],
                                             input_data['first_name'],input_data['last_name'],
                                             input_data['password'],event_roles=[pss_event_user_role])
    
    tables.db_handle.session.add(new_user)
    tables.db_handle.session.commit()
    return new_user

def get_user_and_event_role_from_input_data(request,app):
    tables = app.tables
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('No information in request')

    if 'pss_user_id' not in input_data or 'username' not in input_data or 'password' not in input_data or 'event_role_id' not in input_data:
        raise BadRequest('Information missing')
    pss_user = app.tables.PssUsers.query.filter_by(pss_user_id=input_data['pss_user_id']).first()
    if pss_user is None:
        raise BadRequest('Bad pss user id')        
    event_role = app.tables.EventRoles.query.filter_by(event_role_id=input_data['event_role_id']).first()
    if event_role is None:
        raise BadRequest('Bad event role id')                
    return pss_user,event_role

def add_existing_user_to_event_route(password,pss_user,event_role,app):
    tables = app.tables
    orm_factories.populate_event_user(app,password,
                                      pss_user,[event_role])
    tables.db_handle.session.commit()
    return pss_user

def change_existing_user_in_event_route(pss_user, app, event_role, input_data):
    tables = app.tables
    if 'password' in input_data:
        password=input_data['password']        
    else:
        password=None
    orm_factories.modify_event_user(app,
                                    pss_user,
                                    event_role,
                                    password=password)
    tables.db_handle.session.commit()
    return pss_user

@blueprints.pss_admin_event_blueprint.route('/pss_user',methods=['POST'])
@load_tables
@create_pss_user_permissions.require(403)
def create_pss_user(tables):    
    new_user = create_pss_user_route(request,current_app)
    pss_user_serializer = generate_pss_user_serializer(current_app)    
    user_dict=pss_user_serializer().dump(new_user).data    
    return jsonify({'new_pss_user':user_dict})

@blueprints.event_blueprint.route('/pss_event_user',methods=['POST'])
@load_tables
@create_pss_event_user_permissions.require(403)
def create_pss_event_user(tables):                
    if 'role_id' in json.loads(request.data):
        raise BadRequest('Naughty Naughty')
    new_user = create_pss_user_route(request,current_app)
    pss_user_serializer = generate_pss_user_serializer(current_app)    
    user_dict=pss_user_serializer().dump(new_user).data    
    return jsonify({'new_pss_user':user_dict})
    

@blueprints.event_blueprint.route('/pss_event_user',methods=['PUT'])
@load_tables
@create_pss_event_user_permissions.require(403)
def add_existing_user_to_event(tables):                
    pss_user, event_role = get_user_and_event_role_from_input_data(request,current_app)
    input_data = json.loads(request.data)
    if 'role_id' in input_data:
        raise BadRequest('Naughty Naughty')
    event = tables.Events.query.filter_by(name=current_app.name).first()    
    if event not in pss_user.events:
        modified_pss_user = add_existing_user_to_event_route(input_data['password'],pss_user,event_role,current_app)        
    else:
        modified_pss_user = change_existing_user_in_event_route(pss_user, current_app, event_role, input_data)
    pss_user_serializer = generate_pss_user_serializer(current_app)    
    user_dict=pss_user_serializer().dump(modified_pss_user).data    
    return jsonify({'existing_pss_user_added_to_event':user_dict})
    

