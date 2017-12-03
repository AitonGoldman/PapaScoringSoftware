from werkzeug.exceptions import BadRequest, Unauthorized
from lib_v2 import blueprints
from flask import jsonify,current_app,request
from lib_v2 import permissions
from flask_login import current_user
from lib_v2.serializers import generic
import json

def pss_event_create_route(request,tables_proxy):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Submitted information is missing required fields')
    return tables_proxy.create_event(current_user,input_data,True)


@blueprints.test_blueprint.route('/event',methods=['POST'])
def event_create():
    permission = permissions.EventCreatorPermission()
    if not permission.can():
        raise Unauthorized('You are not authorized to create an event')    
    event = pss_event_create_route(request,current_app.table_proxy)        
    return jsonify({'data':generic.serialize_event_public(event)})
    

