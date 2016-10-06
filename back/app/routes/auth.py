from flask import jsonify,current_app,request
from app.blueprints import admin_login_blueprint
import json
from werkzeug.exceptions import Unauthorized,Conflict
from flask_login import login_required, login_user, logout_user, current_user

@admin_login_blueprint.route('/auth/login',methods=['PUT'])
def route_login():
    input_data = json.loads(request.data)
    user = current_app.tables.User.query.filter_by(username=input_data['username']).first()
    if user and not user.verify_password(input_data['password']):
        user = None
    if user is None:
        raise Unauthorized('Bad username or password')
    login_user(user)
    #identity_changed.send(current_app._get_current_object(), identity=Identity(user.user_id))
    #user_dict = user.to_dict_simple()
    #user_dict['roles'] = [r.name for r in user.roles]        
    return jsonify(user.to_dict_simple())
    
