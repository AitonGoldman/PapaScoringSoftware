from lib.flask_lib import blueprints
from lib.flask_lib.permissions import create_pss_event_user_permissions, create_pss_user_permissions
from flask import jsonify,current_app,request
from werkzeug.exceptions import BadRequest,Unauthorized
from flask_login import login_user, logout_user, current_user
import json
from lib.route_decorators.db_decorators import load_tables
from lib.serializer import generic
from lib import serializer

@blueprints.pss_admin_event_blueprint.route('/roles',methods=['GET'])
@load_tables
def get_roles(tables):    
    roles_list = []
    generic_serializer = generic.generate_generic_serializer(serializer.generic.ALL)
    for role in tables.AdminRoles.query.all():                
        roles_list.append(generic_serializer(role))    
    #FIXME : should be admin_roles
    return jsonify({'roles':roles_list})

@blueprints.event_blueprint.route('/roles',methods=['GET'])
@load_tables
def get_event_roles(tables):    
    roles_list = []
    event_roles = tables.EventRoles.query.all()
    generic_serializer = generic.generate_generic_serializer(serializer.generic.ALL)
    for event_role in event_roles:        
                roles_list.append(generic_serializer(event_role))    
    return jsonify({'event_roles':roles_list})

