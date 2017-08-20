from lib.flask_lib import blueprints
from flask import jsonify,current_app,request
from sqlalchemy.orm import joinedload
from flask_restless.helpers import to_dict
from werkzeug.exceptions import BadRequest,Unauthorized
from flask_login import login_user, logout_user, current_user
import json
from flask_principal import identity_changed, Identity
from lib.serializer.pss_user import  generate_pss_user_to_dict_serializer
from lib.serializer.player import  generate_player_to_dict_serializer

from lib import serializer
from lib.route_decorators.db_decorators import load_tables

#FIXME : all routes under this need to be rechecked when players stuff is implemented

#FIXME : make sure all PssUser instances are called pss_user


def do_user_roles_intersect_with_defined_roles(user_roles,table_roles):
    user_roles_names = [role.name for role in user_roles]            
    allowed_roles = [role.name for role in table_roles]            
    if len(list(set(allowed_roles) & set(user_roles_names))) == 0:
        #FIXME : should not throw exepction, should return False
        raise Unauthorized('User can not access this') 
    return True
    
def check_pss_user_has_admin_site_access(pss_user,tables):
    table_roles = tables.AdminRoles.query.filter_by(admin_role=True).all()
    return do_user_roles_intersect_with_defined_roles(pss_user.admin_roles,table_roles)

def check_event_user_has_event_access(pss_event_user,tables):
    table_roles = tables.EventRoles.query.all()
    return do_user_roles_intersect_with_defined_roles(pss_event_user.event_roles,table_roles)
    
def pss_login_route(request,tables,is_pss_admin_event=True):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Username or password not specified')
    if 'username' not in input_data or 'password' not in input_data:
        raise BadRequest('Missing information')        
    pss_user = tables.PssUsers.query.options(joinedload("admin_roles")).filter_by(username=input_data['username']).first()
    if pss_user is None:
        raise Unauthorized('Bad username or password')
    if pss_user.event_user is None:
        raise BadRequest('User does not have access to this event')                        
    if not pss_user.event_user.verify_password(input_data['password']):
        raise Unauthorized('Bad username or password')
    #FIXME : is this needed anymore?  if they have a event_user field on the event, then they are okay to go, right?
    if is_pss_admin_event:
        check_pss_user_has_admin_site_access(pss_user,tables)
    else:
        check_event_user_has_event_access(pss_user,tables)    
    return pss_user

def player_login_route(request,tables):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Username or password not specified')
    if 'event_player_number' not in input_data or 'event_player_pin' not in input_data:
        raise BadRequest('Missing information')        
    player = tables.Players.query.options(joinedload("player_roles"),
                                          joinedload("event_player"),
                                          joinedload("events")).filter(tables.Players.event_player.has(tables.EventPlayers.event_player_id==input_data['event_player_number'])).first()
    if player is None:
        raise Unauthorized('Bad player id')
    if player.event_player.event_player_pin != input_data['event_player_pin']:
        raise Unauthorized('Bad player pin number')        
    return player

@blueprints.pss_admin_event_blueprint.route('/auth/pss_user/login',methods=['POST'])
@load_tables
def pss_admin_login(tables):    
    pss_user = pss_login_route(request,tables,is_pss_admin_event=True)
    login_user(pss_user)    
    identity_changed.send(current_app._get_current_object(), identity=Identity(pss_user.pss_user_id))
    pss_user_serializer = generate_pss_user_to_dict_serializer(serializer.pss_user.ALL)
    user_dict=pss_user_serializer(pss_user)
    return jsonify({'pss_user':user_dict})

@blueprints.pss_admin_event_blueprint.route('/auth/pss_user/logout',methods=['GET'])
@blueprints.event_blueprint.route('/auth/pss_user/logout',methods=['GET'])
@load_tables
def pss_logout(tables):
    if current_user.is_anonymous() is False:
        logged_out_username=current_user.username
        logout_user()
    else:
        logged_out_username='anonymous'        
    return jsonify({'status':'%s is logged out' % logged_out_username})

@blueprints.event_blueprint.route('/auth/pss_event_user/login',methods=['POST'])
@load_tables
def pss_event_user_login(tables):    
    pss_event_user = pss_login_route(request,tables,is_pss_admin_event=False)
    login_user(pss_event_user)    
    identity_changed.send(current_app._get_current_object(), identity=Identity(pss_event_user.pss_user_id))
    pss_user_serializer = generate_pss_user_to_dict_serializer(serializer.pss_user.ALL)
    user_dict=pss_user_serializer(pss_event_user)
    return jsonify({'pss_user':user_dict})

@blueprints.event_blueprint.route('/auth/player/login',methods=['POST'])
@load_tables
def player_login(tables):    
    player = player_login_route(request,tables)
    login_user(player)    
    identity_changed.send(current_app._get_current_object(), identity=Identity(player.player_id))
    player_serializer = generate_player_to_dict_serializer(serializer.player.ALL)
    user_dict=player_serializer(player)
    return jsonify({'player':user_dict})


@blueprints.pss_admin_event_blueprint.route('/auth/pss_user/current_user',methods=['GET'])
@blueprints.event_blueprint.route('/auth/pss_event_user/current_user',methods=['GET'])
@load_tables
def get_current_user(tables):    
    if current_user.is_anonymous():
        return jsonify({'current_user':None})
    pss_user_serializer = generate_pss_user_to_dict_serializer(serializer.pss_user.ALL)
    #GUYH - need to reget the current user, otherwise the serializer chokes on the proxy current_user gives back
    user = tables.PssUsers.query.filter_by(pss_user_id=current_user.pss_user_id).first()
    user_dict=pss_user_serializer(user)
    return jsonify({'current_user':user_dict})

#FIXME : need get_current_user for event user
