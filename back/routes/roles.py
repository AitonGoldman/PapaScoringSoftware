from lib.flask_lib import blueprints
from lib.flask_lib.permissions import create_pss_event_user_permissions, create_pss_user_permissions
from flask import jsonify,current_app,request
from werkzeug.exceptions import BadRequest,Unauthorized
from flask_login import login_user, logout_user, current_user
import json
from lib import roles
from lib.serializer.roles import generate_admin_roles_serializer, generate_event_roles_serializer
from lib.route_decorators.db_decorators import load_tables

@blueprints.pss_admin_event_blueprint.route('/roles',methods=['GET'])
@load_tables
def get_roles(tables):    
    roles_list = []
    pss_admin_roles_serializer = generate_admin_roles_serializer(current_app)
    for role in tables.AdminRoles.query.all():                
        roles_list.append(pss_admin_roles_serializer().dump(role).data)    
    #FIXME : should be admin_roles
    return jsonify({'roles':roles_list})

@blueprints.event_blueprint.route('/roles',methods=['GET'])
@load_tables
def get_event_roles(tables):    
    roles_list = []
    event_roles = tables.EventRoles.query.all()
    pss_event_roles_serializer = generate_event_roles_serializer(current_app)
    for event_role in event_roles:        
        roles_list.append(pss_event_roles_serializer().dump(event_role).data)    
    return jsonify({'event_roles':roles_list})

