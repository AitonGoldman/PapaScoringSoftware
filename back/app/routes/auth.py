from flask import jsonify,current_app,request
from app.blueprints import admin_login_blueprint
import json
from werkzeug.exceptions import Unauthorized,Conflict,BadRequest
from flask_login import login_required, login_user, logout_user, current_user
from app.util import db_util
from flask_principal import identity_changed, Identity

@admin_login_blueprint.route('/auth/logout',methods=['GET'])
@login_required
def route_logout():
    logout_user()
    return jsonify({'data':'all done'})

@admin_login_blueprint.route('/auth/current_user',methods=['GET'])
@login_required
def route_get_current_user():
    if hasattr(current_user,'user_id'):
        return jsonify({'data':current_user.to_dict_simple()})
    else:
        return jsonify({'data': None})

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
    return jsonify({'data':user.to_dict_simple()})
    
