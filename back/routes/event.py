from flask import Flask
from lib.flask_lib import blueprints
from lib.flask_lib.permissions import create_pss_event_permissions
from flask import jsonify,current_app,request
from werkzeug.exceptions import BadRequest,Unauthorized,Conflict
from flask_login import login_user, logout_user, current_user
import json
from lib.PssConfig import PssConfig
from lib.serializer import generic
from lib import serializer
from lib.serializer.deserialize import deserialize_json
from lib.route_decorators.db_decorators import load_tables
from lib.route_decorators.auth_decorators import check_current_user_is_active

from pss_models.PssUsers import generate_pss_user_event_role_mapping
import os
from lib import orm_factories

def edit_event_route(event,input_data,app):
    deserialize_json(event,input_data,app)
    #FIXME : should check that api keys are valid


@blueprints.pss_admin_event_blueprint.route('/event',methods=['GET'])
@load_tables
def get_events(tables):                    
    events = tables.Events.query.all()
    event_serializer = serializer.event.generate_event_to_dict_serializer(serializer.event.MINIMUM_EVENT)        
    #FIXME : pss_admin should not be hard coded here
    return jsonify({'events':[event_serializer(event) for event in events if event.name != 'pss_admin']})


@blueprints.pss_admin_event_blueprint.route('/event/<event_id>',methods=['GET'])
@load_tables
@create_pss_event_permissions.require(403)
@check_current_user_is_active
def get_event(tables,event_id):                    
    event = tables.Events.query.filter_by(event_id=event_id).first()
    if event.event_creator_pss_user_id != current_user.pss_user_id:
        raise BadRequest('Can not get event details if it is not your event')
    event_serializer = serializer.event.generate_event_to_dict_serializer(serializer.event.ALL)            
    return jsonify({'event':event_serializer(event)})


@blueprints.pss_admin_event_blueprint.route('/event',methods=['POST'])
@load_tables
@create_pss_event_permissions.require(403)
@check_current_user_is_active
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
    new_event = orm_factories.create_event(current_user, tables, input_data, new_event_tables,current_user.pss_user_id)        
    generic_serializer = generic.generate_generic_serializer(serializer.generic.ALL)
    event_dict=generic_serializer(new_event)    
    return jsonify({'new_event':event_dict})
 

@blueprints.pss_admin_event_blueprint.route('/event/<event_id>',methods=['PUT'])
@load_tables
@create_pss_event_permissions.require(403)
@check_current_user_is_active
def edit_event(tables,event_id):                        
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Event details not specified')        
    event = tables.Events.query.filter_by(event_id=event_id).first()
    if event is None:
        raise BadRequest('Bad event submitted')
    if event.event_creator_pss_user_id != current_user.pss_user_id:
        raise BadRequest('You can not edit this event')        
    edit_event_route(event,input_data,current_app)
    tables.db_handle.session.commit()
    generic_serializer = generic.generate_generic_serializer(serializer.generic.ALL)
    event_dict=generic_serializer(event)    
    return jsonify({'event':event_dict})
