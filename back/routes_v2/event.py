from werkzeug.exceptions import BadRequest, Unauthorized
from lib_v2 import blueprints
from flask import jsonify,current_app,request
from lib_v2 import permissions
from flask_login import current_user
from lib_v2.serializers import generic
import json

def pss_event_create_route(request,tables_proxy,user):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Submitted information is missing required fields')    
    # don't allow duplicate names
    if tables_proxy.get_event_by_eventname(input_data['name']) is not None:
        raise BadRequest('Event already exists')
    new_event = tables_proxy.create_event(user,input_data,True)
    #tables_proxy.create_event_tables(new_event.event_id)
    return new_event

def pss_event_edit_route(request,tables_proxy):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Submitted information is missing required fields')    
    # don't allow duplicate names
    event = tables_proxy.get_event_by_eventname(input_data['name'])
    if event and event.event_id != int(input_data['event_id']):
        if tables_proxy.get_event_by_eventname(input_data['name']) is not None:
            raise BadRequest('Event name already exists')    
    return tables_proxy.edit_event(input_data,True)            
        
@blueprints.test_blueprint.route('/event',methods=['POST'])
def event_create():
    permission = permissions.EventCreatorPermission()    
    if not permission.can():
        raise Unauthorized('You are not authorized to create an event')
    event = pss_event_create_route(request,current_app.table_proxy,current_user)
    return jsonify({'data':generic.serialize_event_public(event)})
    

@blueprints.test_blueprint.route('/event',methods=['PUT'])
def event_edit():
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Submitted information is missing required fields')
    permission = permissions.EventEditPermission(input_data['event_id'])    
    if not permission.can():
        raise Unauthorized('You are not authorized to edit this event')        
    event = pss_event_edit_route(request,current_app.table_proxy)        
    return jsonify({'data':generic.serialize_event_public(event)})
    

