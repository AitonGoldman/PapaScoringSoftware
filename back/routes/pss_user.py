from lib.flask_lib import blueprints
from lib.flask_lib.permissions import create_pss_event_user_permissions, create_pss_user_permissions
from flask import jsonify,current_app,request
from sqlalchemy.orm import joinedload
from flask_restless.helpers import to_dict
from functools import wraps
from werkzeug.exceptions import BadRequest,Unauthorized
from flask_login import login_user, logout_user, current_user
import json
from flask_principal import identity_changed, Identity
from lib import roles
from lib.serializer.pss_user import generate_pss_user_serializer
from lib.route_decorators.db_decorators import load_tables

@blueprints.pss_admin_event_blueprint.route('/pss_user',methods=['POST'])
@load_tables
@create_pss_user_permissions.require(403)
def create_pss_user(tables):    
    #FIXME : need to add PssUserEventRoles many to many table
    
    return jsonify({'pss_user':None})


@blueprints.event_blueprint.route('/pss_user',methods=['POST'])
@load_tables
@create_pss_event_user_permissions.require(403)
def create_pss_event_user(tables):        
    return jsonify({'pss_user':None})
