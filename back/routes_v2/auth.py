from werkzeug.exceptions import BadRequest, Unauthorized
from lib_v2 import blueprints,TableProxy
from flask import jsonify,current_app,request
from flask_principal import identity_changed, Identity
from flask_login import login_user,logout_user
from lib_v2.serializers import generic
import json

def get_user_roles(pss_user):
    if pss_user.event_creator:
        return [{'event_id':event.event_id,'event_role_name':'tournamentdirector'} for event in pss_user.events_created]            
    else:
        return [{'event_id':event.event_id,'event_role_name':event.event_role_name} for event in pss_user.event_roles]
 

def pss_login_route(request,tables_proxy,event_creator=False,event_id=None):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Submitted information is missing required fields')
    if 'username' not in input_data or 'password' not in input_data:
        raise BadRequest('Missing username or password')
    pss_user = tables_proxy.get_user_by_username(input_data['username'])
    if pss_user is None:
        raise Unauthorized('Bad username')
    if event_creator is True:
        if pss_user.event_creator is False:
            raise Unauthorized('User is not an event creator')    
    if not pss_user.verify_password(input_data['password']):        
        raise Unauthorized('Bad password')
    if event_id:
        if pss_user.event_creator:
            if len([event for event in pss_user.events_created if event.event_id==int(event_id)]) == 0:
                raise Unauthorized('Not allowed to login to this event')
        else:
            if len([event for event in pss_user.event_roles if event.event_id==int(event_id)]) == 0:
                raise Unauthorized('Not allowed to login to this event')
                
    return pss_user

def player_login_route(request,tables_proxy,event_id):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Submitted information is missing required fields')
    if 'player_id_for_event' not in input_data or 'player_pin' not in input_data:
        raise BadRequest('Missing player number or pin')
    #player = tables_proxy.get_player_by_player_id_for_event(input_data['player_id_for_event'],event_id)
    player = tables_proxy.get_player(event_id,player_id_for_event=input_data['player_id_for_event'])    
    if player is None:
        raise Unauthorized('Bad player number')
    if not player.verify_pin(input_data['player_pin']):        
        raise Unauthorized('Bad pin')        
    return player


# getUserRoles(pss_user, creator=False)
# 
#
#

@blueprints.test_blueprint.route('/auth/pss_user/login',methods=['POST'])
def event_creator_login():
    pss_user = pss_login_route(request,current_app.table_proxy,True)
    if login_user(pss_user) is False:
        raise Unauthorized('User is not active')
    identity_changed.send(current_app._get_current_object(), identity=Identity(pss_user.pss_user_id))            
    return jsonify({'data':generic.serialize_pss_user_public(pss_user)})        

@blueprints.test_blueprint.route('/auth/pss_event_user/login',methods=['POST'])
def event_user_login():
    pss_user = pss_login_route(request,current_app.table_proxy,False)
    if login_user(pss_user) is False:
        raise Unauthorized('User is not active')
    identity_changed.send(current_app._get_current_object(), identity=Identity(pss_user.pss_user_id))            
    return jsonify({'data':generic.serialize_pss_user_public(pss_user)})        

@blueprints.test_blueprint.route('/auth/pss_event_user/login/<int:event_id>',methods=['POST'])
def event_user_login_with_event_id(event_id):
    pss_user = pss_login_route(request,current_app.table_proxy,event_creator=False,event_id=event_id)
    if login_user(pss_user) is False:
        raise Unauthorized('User is not active')
    identity_changed.send(current_app._get_current_object(), identity=Identity(pss_user.pss_user_id))
    pss_user_dict = generic.serialize_pss_user_public(pss_user)
    pss_user_dict['roles']=get_user_roles(pss_user)
    return jsonify({'data':pss_user_dict})        

@blueprints.test_blueprint.route('/auth/player/login/<int:event_id>',methods=['POST'])
def event_player_login(event_id):    
    current_app.table_proxy.initialize_event_specific_relationship(event_id)
    player = player_login_route(request,current_app.table_proxy,event_id)    
    if login_user(player) is False:
        raise Unauthorized('Player is not active')
    identity_changed.send(current_app._get_current_object(), identity=Identity("player_%s"%player.player_id))            
    return jsonify({'data':generic.serialize_player_public(player)})        
