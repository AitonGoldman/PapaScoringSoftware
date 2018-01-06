from werkzeug.exceptions import BadRequest, Unauthorized
from lib_v2 import blueprints,permissions,pss_user_helpers
from flask import jsonify,current_app,request
from flask_login import current_user
from lib_v2.serializers import generic
import json
from flask_restless.helpers import to_dict

def get_username_that_does_not_already_exist(new_username,new_pss_users,tables_proxy):
    for i in range(2,10):
        new_username_with_digit=new_username+"%d"%i
        if not tables_proxy.get_user_by_username(new_username_with_digit) and new_username_with_digit not in new_pss_users:
            return new_username_with_digit

def get_password_for_new_user(password):
    if password:
        return password
    return '1234'
    
def update_event_user_roles_route(request,tables_proxy,event_id):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Submitted information is missing required fields')    
    event = tables_proxy.get_event_by_event_id(event_id)    
    if event is None:
        raise BadRequest('No event with that ID')
    event_role_ids=input_data['event_role_ids']
    event_user_to_edit=input_data['event_user']
    pss_user = tables_proxy.get_user_by_id(event_user_to_edit['pss_user_id'])
    if pss_user is None:
        raise BadRequest('Tried to submit a user with an invalid pss_user_id')    
    tables_proxy.update_event_user_roles(event_role_ids,event_id, pss_user)
    return pss_user

def create_event_user_route(request,tables_proxy,event_id):
    #FIXME : check if user is already added to event
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Submitted information is missing required fields')    
    event = tables_proxy.get_event_by_event_id(event_id)    
    if event is None:
        raise BadRequest('No event with that ID')
    event_users_to_create=input_data['event_users']
    new_pss_users={}
    pss_users_added_to_event=[]
    event_role_ids=input_data['event_role_ids']
    for event_user_to_create in event_users_to_create:        
        if 'pss_user_id' in event_user_to_create:            
            pss_user = tables_proxy.get_user_by_id(event_user_to_create['pss_user_id'])
            if pss_user is None:
                raise BadRequest('Tried to submit a user with an invalid pss_user_id')                
            if len([event_info for event_info in pss_user.events if event_info.event_id==int(event_id)])>0:
                raise BadRequest('User already added to event')                
            #FIXME : need to silently fail when user is already registered
            tables_proxy.update_event_user_roles(event_role_ids,event_id, pss_user)
            pss_users_added_to_event.append(pss_user)
            continue                
        new_username=pss_user_helpers.generate_username(event_user_to_create)        
        if tables_proxy.get_user_by_username(new_username) or new_username in new_pss_users:            
            new_username=get_username_that_does_not_already_exist(new_username,new_pss_users,tables_proxy)        
        new_pss_user = tables_proxy.create_user(new_username,event_user_to_create['first_name'],
                                                event_user_to_create['last_name'],get_password_for_new_user(event_user_to_create.get('password',None)),
                                                extra_title=event_user_to_create.get('extra_title',None))
        tables_proxy.update_event_user_roles(event_role_ids,event_id, new_pss_user)        
        pss_users_added_to_event.append(new_pss_user)    
    return pss_users_added_to_event


@blueprints.test_blueprint.route('/<int:event_id>/event_user',methods=['POST'])
def event_user_create(event_id):            

    permission = permissions.CreateEventUserPermission(event_id)    
    if not permission.can():
        raise Unauthorized('You are not authorized to register users for this event')        
    #event = pss_event_edit_route(request,current_app.table_proxy)        
    #return jsonify({'data':generic.serialize_event_public(event)})
    new_event_users=[generic.serialize_pss_user_public(pss_user) for pss_user in create_event_user_route(request,current_app.table_proxy,event_id)]
    current_app.table_proxy.commit_changes()
    return jsonify({'data':new_event_users})

@blueprints.test_blueprint.route('/<int:event_id>/event_role_mapping',methods=['PUT'])
def event_role_mapping_update(event_id):            
    permission = permissions.CreateEventUserPermission(event_id)    
    if not permission.can():
        raise Unauthorized('You are not authorized to edit users for this event')        
    update_event_user_roles_route(request,current_app.table_proxy,event_id)
    current_app.table_proxy.commit_changes()
    return jsonify({'data':True})

@blueprints.test_blueprint.route('/pss_users',methods=['GET'])
def get_all_pss_users():            
    all_users = current_app.table_proxy.get_all_users()
    all_users_list=[]
    for user in all_users:
        all_users_list.append(generic.serialize_pss_user_public(user))
    roles = current_app.table_proxy.get_all_event_roles()
    roles_list = [to_dict(role) for role in roles]
    return jsonify({'data':all_users_list,'roles':roles_list})
