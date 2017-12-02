from werkzeug.exceptions import BadRequest, Unauthorized
from lib_v2 import blueprints
from flask import jsonify,current_app,request
from flask_principal import identity_changed, Identity
from flask_login import login_user,logout_user
from lib_v2.serializers import pss_user_serializer
import json

def pss_login_route(request,tables_proxy,event_creator=False):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Submitted information is missing required fields')
    if 'username' not in input_data or 'password' not in input_data:
        raise BadRequest('Missing username or password')
    if event_creator is True:        
        pss_user = tables_proxy.get_user_by_username(input_data['username'])
        if pss_user and pss_user.event_creator is False:
            raise BadRequest('User is not an event creator')            
    else:
        pss_user = None
    if pss_user is None:
        raise Unauthorized('Bad username')
    if not pss_user.verify_password(input_data['password']):        
        raise Unauthorized('Bad password')    
    return pss_user


@blueprints.test_blueprint.route('/auth/pss_user/login',methods=['POST'])
def event_creator_login():
    pss_user = pss_login_route(request,current_app.table_proxy,True)
    if login_user(pss_user) is False:
        raise Unauthorized('User is not active')
    identity_changed.send(current_app._get_current_object(), identity=Identity(pss_user.pss_user_id))    
    serializer = pss_user_serializer.generate_pss_user_to_dict_serializer(pss_user_serializer.ALL)
    user_dict=serializer(pss_user)
    return jsonify({'pss_user':user_dict})
    
