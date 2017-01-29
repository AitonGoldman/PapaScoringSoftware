from flask import jsonify,current_app,request
from blueprints import admin_login_blueprint
import json
from werkzeug.exceptions import Unauthorized,Conflict,BadRequest
from flask_login import login_required, login_user, logout_user, current_user
from util import db_util
from flask_principal import identity_changed, Identity
from routes.utils import record_ioniccloud_push_token,send_push_notification

@admin_login_blueprint.route('/auth/logout',methods=['GET'])
def route_logout():
    if current_user.is_anonymous() is False:
        logout_user()
    return jsonify({'data':'all done'})

@admin_login_blueprint.route('/auth/current_user',methods=['GET'])
def route_get_current_user():
    if current_user.is_anonymous():
        return jsonify({'data':None})
    current_user_dict = current_user.to_dict_simple()
    #if current_user.is_player:
    #    current_user_dict['full_name']=current_user.player.get_full_name()
    return jsonify({'data':current_user_dict})

@admin_login_blueprint.route('/auth/login',methods=['PUT'])
def route_login():
    tables = db_util.app_db_tables(current_app)
    if request.data:
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Username or password not specified')        
    if 'username' not in input_data or 'password' not in input_data:
        raise BadRequest('Username or password not specified')    
    user = tables.User.query.filter_by(username=input_data['username']).first()    
    if user and not user.verify_password(input_data['password']):
        user = None
    if user is None:
        raise Unauthorized('Bad username or password')
    login_user(user)
    identity_changed.send(current_app._get_current_object(), identity=Identity(user.user_id))
    user_dict = user.to_dict_simple()
    user_dict['roles'] = [r.name for r in user.roles]    
    if "ioniccloud_push_token" in input_data:
        record_ioniccloud_push_token(input_data['ioniccloud_push_token'],user_id=user.user_id)
        send_push_notification('you are logged in - good job!',user_id=user.user_id)
        send_push_notification('okay - push notifications work!',user_id=user.user_id,postpone=120)
        
    return jsonify({'data':user.to_dict_simple()})

@admin_login_blueprint.route('/auth/player_login',methods=['PUT'])
def route_player_login():
    tables = db_util.app_db_tables(current_app)
    if request.data:
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Player pin # not specified')        
    if 'player_pin' not in input_data or 'player_id' not in input_data:
        raise BadRequest('Player pin # or Player Number not specified')    
    player = tables.Player.query.filter_by(pin=input_data['player_pin'],player_id=input_data['player_id']).first()
    if player is None:
        raise Unauthorized('Bad player pin # and player number')
    login_user(player.user)
    identity_changed.send(current_app._get_current_object(), identity=Identity(player.player_id))
    if "ioniccloud_push_token" in input_data:
        record_ioniccloud_push_token(input_data['ioniccloud_push_token'],user_id=player.user.user_id)
    player_dict = player.user.to_dict_simple()
    #player_dict['full_name']=player.get_full_name()
    return jsonify({'data':player_dict})

