from lib.flask_lib import blueprints
from lib.flask_lib.permissions import create_pss_event_user_permissions, create_pss_user_permissions
from flask import jsonify,current_app,request
from werkzeug.exceptions import BadRequest,Unauthorized
from flask_login import login_user, logout_user, current_user
import json
from lib import roles
from lib.serializer.roles import generate_roles_serializer
from lib.route_decorators.db_decorators import load_tables

@blueprints.pss_admin_event_blueprint.route('/roles',methods=['GET'])
@load_tables
def get_roles(tables):    
    roles_list = []
    pss_roles_serializer = generate_roles_serializer(current_app)
    for role in tables.Roles.query.all():                
        roles_list.append(pss_roles_serializer().dump(role).data)    
    return jsonify({'roles':roles_list})

@blueprints.event_blueprint.route('/roles',methods=['GET'])
@load_tables
def get_roles(tables):    
    roles_list = []
    #FIXME : this list should be a constant/not hidden here
    #filtered_roles=[roles.PSS_ADMIN,roles.PSS_USER]
    filtered_roles = tables.EventRoles.query.all()
    pss_roles_serializer = generate_roles_serializer(current_app)
    for role in tables.Roles.query.filter(~tables.Roles.name.in_(filtered_roles)).all():
        roles_list.append(pss_roles_serializer().dump(role).data)    
    return jsonify({'roles':roles_list})

