from lib.flask_lib import blueprints
from lib.flask_lib.permissions import create_pss_event_user_permissions, create_pss_user_permissions
from flask import jsonify,current_app,request
from werkzeug.exceptions import BadRequest,Unauthorized
from flask_login import login_user, logout_user, current_user
import json
from lib import roles
from lib.serializer.pss_user import generate_pss_user_serializer
from lib.route_decorators.db_decorators import load_tables

def create_pss_user_route(tables,request):        
    # FIXME : need to make sure onidentityload pulls event permissions from both tables

    # FIXME : need to make sure intergration test is using bootstraping functions
    
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Username or password not specified')        
    if 'username' not in input_data or 'password' not in input_data or 'role_id' not in input_data:
        raise BadRequest('Information missing')
    new_user = tables.PssUsers(username=input_data['username'])    
    pss_user_role = tables.Roles.query.filter_by(role_id=int(input_data['role_id'])).first()
    if pss_user_role is None:
        raise BadRequest('Role specified does not exist')        
    new_user.roles.append(pss_user_role)
    tables.db_handle.session.add(new_user)
    tables.db_handle.session.commit()
    return new_user

@blueprints.pss_admin_event_blueprint.route('/pss_user',methods=['POST'])
@load_tables
@create_pss_user_permissions.require(403)
def create_pss_user(tables):    
    #FIXME : protect against duplicate users
    new_user = create_pss_user_route(tables,request)
    pss_user_serializer = generate_pss_user_serializer(current_app)    
    user_dict=pss_user_serializer().dump(new_user).data    
    return jsonify({'new_pss_user':user_dict})

@blueprints.event_blueprint.route('/pss_user',methods=['POST'])
@load_tables
@create_pss_event_user_permissions.require(403)
def create_pss_event_user(tables):        
    #FIXME : protect against duplicate users
    return jsonify({'pss_user':None})
