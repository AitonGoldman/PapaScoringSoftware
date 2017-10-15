from lib.serializer import generic
from flask_restless.helpers import to_dict
from lib.flask_lib import blueprints
from lib.flask_lib.permissions import create_pss_event_user_permissions, create_pss_user_permissions
from flask import jsonify,current_app,request
from werkzeug.exceptions import BadRequest,Unauthorized,Conflict
from flask_login import login_user, logout_user, current_user
import json
from lib import orm_factories
from lib.serializer.pss_user import generate_pss_user_to_dict_serializer
from lib import serializer
from lib.route_decorators.db_decorators import load_tables
from lib.route_decorators.auth_decorators import check_current_user_is_active
from sqlalchemy.orm import joinedload
from lib.PssConfig import PssConfig

def check_user_input_valid(user_dict):
    if 'username' not in user_dict or 'password' not in user_dict or 'first_name' not in user_dict or 'last_name' not in user_dict:        
        raise BadRequest('Information missing')
    if 'event_role_id' not in user_dict and 'role_id' not in user_dict:
        raise BadRequest('Information missing')
    if 'event_role_id' in user_dict and 'role_id' in user_dict:
        raise BadRequest('Naughty Naughty')        
    
#FIXME : tables not needed
def create_pss_event_user_from_input_data(user_dict,app):
    pss_event_user_role = app.tables.EventRoles.query.filter_by(event_role_id=int(user_dict['event_role_id'])).first()
    if pss_event_user_role is None:
        raise BadRequest('Role specified does not exist')
    new_user = orm_factories.create_user(app,user_dict['username'],
                                         user_dict['first_name'],user_dict['last_name'],
                                         user_dict['password'],event_roles=[pss_event_user_role])
    if 'extra_title' in user_dict:
        new_user.extra_title = user_dict['extra_title']
    return new_user



def create_pss_user_route(user_dict, app):                    
    orm_factories.check_user_input_valid(user_dict)        
    orm_factories.check_user_exists(input_data,app)

    if 'role_id' in user_dict:
        pss_user_role = app.tables.AdminRoles.query.filter_by(admin_role_id=int(user_dict['role_id'])).first()
        if pss_user_role is None:
            raise BadRequest('Role specified does not exist')
        new_user = orm_factories.create_user(app,user_dict['username'],
                                             user_dict['first_name'],user_dict['last_name'],
                                             user_dict['password'],admin_roles=[pss_user_role])
        if 'extra_title' in user_dict:
            new_user.extra_title = user_dict['extra_title']        
    if 'event_role_id' in user_dict:
        new_user = create_pss_event_user_from_input_data(user_dict,app)
    tables.db_handle.session.add(new_user)
    tables.db_handle.session.commit()
    return new_user

def get_user_and_event_role_from_input_data(user_dict,app):
    tables = app.tables
    if 'pss_user_id' not in user_dict or 'username' not in user_dict or 'password' not in user_dict or 'event_role_id' not in user_dict:
        raise BadRequest('Information missing')
    if 'role_id' in user_dict:
        raise BadRequest('Naughty Naughty')
    pss_user = app.tables.PssUsers.query.filter_by(pss_user_id=user_dict['pss_user_id']).first()
    if pss_user is None:
        raise BadRequest('Bad pss user id')        
    event_role = app.tables.EventRoles.query.filter_by(event_role_id=user_dict['event_role_id']).first()
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
@check_current_user_is_active
@create_pss_user_permissions.require(403)
def create_pss_user(tables):    
    input_data = json.loads(request.data)
    new_user = create_pss_user_route(input_data,current_app)
    pss_user_serializer = generate_pss_user_to_dict_serializer(serializer.pss_user.ALL)
    user_dict=pss_user_serializer(new_user)
    return jsonify({'new_pss_user':user_dict})

@blueprints.pss_admin_event_blueprint.route('/pss_event_users',methods=['POST'])
@blueprints.event_blueprint.route('/pss_event_users',methods=['POST'])
@load_tables
@check_current_user_is_active
@create_pss_event_user_permissions.require(403)
def create_pss_event_users(tables):                
    input_data = json.loads(request.data)
    if 'event_id' in input_data:
        event_id = int(input_data['event_id'])
        matching_user_events = [event for event in current_user.events if event.event_id==event_id]
        if len(matching_user_events)!=1:
            raise BadRequest('Trying to create tournament for an event you do not own')
        event = tables.Events.query.filter_by(event_id=event_id).first()
        pss_config = PssConfig()
        app = pss_config.get_db_info().getImportedTablesForEvent(event.name)        
    else:
        app = current_app

    #if 'role_id' in json.loads(request.data):
    #    raise BadRequest('Naughty Naughty')
    new_users=[]
    parsed_user_names=[]
    for user in input_data['users_text_area'].split("\n"):
        user_name_tokens=user.split(' ')
        if len(user_name_tokens)<2:
            raise BadRequest('User %s does not have a last name specified' % user)
        parsed_user = {
            "username":user_name_tokens[0]+user_name_tokens[1],
            "password":"1234",
            "first_name":user_name_tokens[0],
            "last_name":user_name_tokens[1],
            "event_role_id":input_data['event_role_id']
        }                
        orm_factories.check_user_exists(parsed_user,app)                    
        parsed_user_names.append(parsed_user)
        
    for user in parsed_user_names:
        new_user = create_pss_event_user_from_input_data(user,app)        
        app.tables.db_handle.session.add(new_user)
        app.tables.db_handle.session.commit()
        pss_user_serializer = generate_pss_user_to_dict_serializer(serializer.pss_user.ALL)
        user_dict=pss_user_serializer(new_user)
        new_users.append(user_dict)
    return jsonify({'pss_users_added_to_event':new_users})


@blueprints.event_blueprint.route('/pss_event_user',methods=['POST'])
@load_tables
@check_current_user_is_active
@create_pss_event_user_permissions.require(403)
def create_pss_event_user(tables):                
    input_data = json.loads(request.data)
    if 'role_id' in json.loads(input_data):
        raise BadRequest('Naughty Naughty')
    new_user = create_pss_user_route(input_data,current_app)
    pss_user_serializer = generate_pss_user_to_dict_serializer(serializer.pss_user.ALL)
    user_dict=pss_user_serializer(new_user)
    return jsonify({'new_pss_user':user_dict})
    
@blueprints.pss_admin_event_blueprint.route('/pss_event_user',methods=['PUT'])
@blueprints.event_blueprint.route('/pss_event_user',methods=['PUT'])
@load_tables
@check_current_user_is_active
@create_pss_event_user_permissions.require(403)
def add_existing_user_to_event(tables):                
    input_data = json.loads(request.data)
    if 'event_id' in input_data:
        event_id = int(input_data['event_id'])
        matching_user_events = [event for event in current_user.events if event.event_id==event_id]
        if len(matching_user_events)!=1:
            raise BadRequest('Trying to create tournament for an event you do not own')
        event = tables.Events.query.filter_by(event_id=event_id).first()
        pss_config = PssConfig()
        app = pss_config.get_db_info().getImportedTablesForEvent(event.name)        
    else:
        app = current_app

    event = tables.Events.query.filter_by(name=app.name).first()    
    new_users=[]
    for user in input_data['users']:
        if 'password' not in user:
            user['password']="1234"
        user['event_role_id']=input_data['event_role_id']
        pss_user, event_role = get_user_and_event_role_from_input_data(user,app)    
        if event.name not in [event.name for event in pss_user.events]:            
            modified_pss_user = add_existing_user_to_event_route(user['password'],pss_user,event_role,app)        
        else:
            modified_pss_user = pss_user
        pss_user_serializer = generate_pss_user_to_dict_serializer(serializer.pss_user.ALL)
        user_dict=pss_user_serializer(modified_pss_user)
        new_users.append(user_dict)
    return jsonify({'pss_users_added_to_event':new_users})

@blueprints.event_blueprint.route('/pss_user',methods=['GET'])
@blueprints.pss_admin_event_blueprint.route('/pss_user',methods=['GET'])
@load_tables
def get_existing_users(tables):                
    existing_users = tables.PssUsers.query.options(joinedload("event_roles"),joinedload("admin_roles"),joinedload("events"),joinedload("event_user")).all()
    #existing_users = tables.PssUsers.query.all()
    pss_user_serializer = generate_pss_user_to_dict_serializer(serializer.pss_user.ALL)
    existing_users_list = []
    for existing_user in existing_users:        
        user_dict = pss_user_serializer(existing_user)                
        existing_users_list.append(user_dict)
    roles_list = []
    event_roles = tables.EventRoles.query.all()
    generic_serializer = generic.generate_generic_serializer(serializer.generic.ALL)
    for event_role in event_roles:        
                roles_list.append(generic_serializer(event_role))    
    
    return jsonify({'existing_pss_users':existing_users_list,'event_roles':roles_list})


@blueprints.event_blueprint.route('/pss_event_user',methods=['GET'])
@load_tables
def get_existing_event_users(tables):                
    existing_users = tables.PssUsers.query.options(joinedload("event_roles"),joinedload("admin_roles"),joinedload("events"),joinedload("event_user")).filter(tables.PssUsers.event_user!=None).all()
    pss_user_serializer = generate_pss_user_to_dict_serializer(serializer.pss_user.ALL)
    existing_users_list = []
    for existing_user in existing_users:        
        user_dict = pss_user_serializer(existing_user)                
        existing_users_list.append(user_dict)
    
    return jsonify({'existing_pss_event_users':existing_users_list})

@blueprints.event_blueprint.route('/pss_event_user/<pss_user_id>',methods=['GET'])
@load_tables
def get_existing_event_user(tables,pss_user_id):                
    existing_user = tables.PssUsers.query.options(joinedload("event_roles"),joinedload("admin_roles"),joinedload("events"),joinedload("event_user")).filter_by(pss_user_id=pss_user_id).first()
    if existing_user.event_user is None:
        raise BadRequest('User is not in this event')
    pss_user_serializer = generate_pss_user_to_dict_serializer(serializer.pss_user.ALL)
    user_dict = pss_user_serializer(existing_user)                            
    return jsonify({'existing_pss_user':user_dict})

@blueprints.pss_admin_event_blueprint.route('/pss_user/<pss_user_id>',methods=['GET'])
@load_tables
def get_existing_user(tables,pss_user_id):                
    existing_user = tables.PssUsers.query.options(joinedload("event_roles"),joinedload("admin_roles"),joinedload("events"),joinedload("event_user")).filter_by(pss_user_id=pss_user_id).first()
    pss_user_serializer = generate_pss_user_to_dict_serializer(serializer.pss_user.ALL)
    user_dict = pss_user_serializer(existing_user)                            
    return jsonify({'existing_pss_user':user_dict})
    

