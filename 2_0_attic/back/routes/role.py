from blueprints import admin_login_blueprint,admin_manage_blueprint
from flask import jsonify,current_app,request
import json
from werkzeug.exceptions import BadRequest,Conflict
from util import db_util
from util.permissions import Admin_permission
from flask_login import login_required,current_user

@admin_manage_blueprint.route('/role',methods=['GET'])
def route_get_roles():
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)    
    roles = tables.Role.query.all()            
    if roles is None:
        return jsonify({'data':None})    
    roles_dict = {role.role_id: role.to_dict_simple() for role in roles}
    return jsonify({'data':roles_dict})
        
