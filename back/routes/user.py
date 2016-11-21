from blueprints import admin_login_blueprint,admin_manage_blueprint
from flask import jsonify,current_app,request
import json
from werkzeug.exceptions import BadRequest,Conflict
from util import db_util
from util.permissions import Admin_permission
from flask_login import login_required,current_user
from routes.utils import fetch_entity, check_roles_exist
from orm_creation import create_user
import os

# def check_roles_exist(roles):
#     for role_id in roles:
#         existing_role = current_app.tables.Role.query.filter_by(role_id=role_id).first()
#         if existing_role is None:            
#             raise BadRequest('Role with id %s does not exist' % role_id)


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

@admin_manage_blueprint.route('/user',methods=['GET'])
def route_get_all_users():
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    users = tables.User.query.all()    
    users_dict = {user.user_id: user.to_dict_simple() for user in users}
    return jsonify({'data':users_dict})

@admin_manage_blueprint.route('/user/<user_id>',methods=['GET'])
def route_get_user(user_id):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    user = fetch_entity(tables.User,user_id)     
    user_dict = {user.user_id: user.to_dict_simple()}
    return jsonify({'data':user_dict})


@admin_manage_blueprint.route('/user/<user_id>',methods=['PUT'])
@login_required
@Admin_permission.require(403)
def route_update_user(user_id):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    user = fetch_entity(tables.User,user_id)     
    input_data = json.loads(request.data)
    if 'username' not in input_data:
        raise BadRequest("You did not specify a username")
    if input_data['username'] != user.username:
        user.username=input_data['username']
    if 'has_picture' in input_data:
        user.has_picture=True
    if 'password' in input_data:        
        user.crypt_password(input_data['password'])    
    if 'roles' in input_data:        
        check_roles_exist(tables, input_data['roles'])
        roles = current_app.tables.Role.query.all()
        user_roles = user.roles
        for role in roles:            
            if role in user_roles and str(role.role_id) not in input_data['roles']:
                user.roles.remove(role)                
            if role not in user_roles and str(role.role_id) in input_data['roles']:                                
                user.roles.append(role)                
    if 'pic_file' in input_data:
        os.system('mv %s/%s /var/www/html/pics/user_%s.jpg' % (current_app.config['UPLOAD_FOLDER'],input_data['pic_file'],user.user_id))
    db.session.commit()                        
    return jsonify({'data':user.to_dict_simple()})


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
    if 'roles' in input_data:
        roles = input_data['roles']
    else:
        roles = []
    new_user = create_user(current_app,input_data['username'],input_data['password'],roles)
    
    return jsonify({'data':new_user.to_dict_simple()})
    
