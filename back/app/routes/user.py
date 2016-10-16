from app.blueprints import admin_login_blueprint,admin_manage_blueprint
from flask import jsonify,current_app,request
import json
from werkzeug.exceptions import BadRequest,Conflict
from app.util import db_util
from app.util.permissions import Admin_permission
from flask_login import login_required,current_user

@admin_manage_blueprint.route('/user/<user_id>',methods=['DELETE'])
@login_required
@Admin_permission.require(403)
def route_delete_user(user_id):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    user = tables.User.query.filter_by(user_id=user_id).first()
    if user is None:
        raise BadRequest("Tried to delete a user that does not exist")
    db.session.delete(user)
    db.session.commit()
    return jsonify({'data':'deleted'})
        
@admin_manage_blueprint.route('/user',methods=['POST'])
@login_required
@Admin_permission.require(403)
def route_add_user():
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)

    input_data = json.loads(request.data)
    for key in ['username','password']:
        if key not in input_data:
            raise BadRequest("You did not specify a username and/or a password")        
    user = tables.User.query.filter_by(username=input_data['username']).first()
    if user is not None:
        raise Conflict('Duplicate username')
    new_user = tables.User(
        username=input_data['username']        
    )
    
    new_user.crypt_password(input_data['password'])
    db.session.add(new_user)
    
    if 'roles' in input_data:        
        for role in input_data['roles']:                        
            existing_role = current_app.tables.Role.query.filter_by(role_id=role['role_id']).first()            
            if existing_role is None:                
                raise BadRequest('Role with id %s does not exist' % role['role_id'])
        for role in input_data['roles']:
            existing_role = current_app.tables.Role.query.filter_by(role_id=role['role_id']).first()            
            new_user.roles.append(existing_role)
    
    db.session.commit()                        
    return jsonify({'data':new_user.to_dict_simple()})
    
