from lib.flask_lib import blueprints
from flask import jsonify,current_app,request
from sqlalchemy.orm import joinedload
from flask_restless.helpers import to_dict
from werkzeug.exceptions import BadRequest,Unauthorized
from flask_login import login_user, logout_user, current_user
import json
from flask_principal import identity_changed, Identity
from lib import roles
from lib.serializer.pss_user import generate_pss_user_serializer
from lib.route_decorators.db_decorators import load_tables

#FIXME : all routes under this need to be rechecked when players stuff is implemented

#FIXME : make sure all PssUser instances are called pss_user

def check_pss_user_has_admin_site_access(pss_user,tables):
    table_roles = tables.Roles.query.filter_by(admin_role=True).all()
    user_roles = [role.name for role in pss_user.roles]            
    allowed_roles = [role.name for role in table_roles]            
    if len(list(set(allowed_roles) & set(user_roles))) == 0:
        raise Unauthorized('User can not access this') 
    return True

def check_event_user_has_event_access(pss_event_user,tables):
    table_roles = tables.EventRoles.query.all()
    user_roles = [event_role.role.name for event_role in pss_event_user.event_roles]            
    allowed_roles = [role.name for role in table_roles]            
    if len(list(set(allowed_roles) & set(user_roles))) == 0:
        raise Unauthorized('User can not access this') 
    return True


def pss_admin_login_route(request,tables):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Username or password not specified')        
    pss_user = tables.PssUsers.query.options(joinedload("roles")).filter_by(username=input_data['username']).first()        
    if pss_user and not pss_user.event_user.verify_password(input_data['password']):
       pss_user = None
    if pss_user is None:
       raise Unauthorized('Bad username or password')    
    #FIXME : this should be in pss_admin_login(), not here
    check_pss_user_has_admin_site_access(pss_user,tables)
    return pss_user

def pss_event_user_login_route(request,tables):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Username or password not specified')        
    pss_event_user = tables.PssUsers.query.options(joinedload("roles")).filter_by(username=input_data['username']).first()        
    if pss_event_user and not pss_event_user.event_user.verify_password(input_data['password']):
       pss_event_user = None
    if pss_event_user is None:
       raise Unauthorized('Bad username or password')    
    #FIXME : this should be in pss_admin_login(), not here
    check_event_user_has_event_access(pss_event_user,tables)
    return pss_event_user

@blueprints.pss_admin_event_blueprint.route('/auth/pss_user/login',methods=['POST'])
@load_tables
def pss_admin_login(tables):    
    pss_user = pss_admin_login_route(request,tables)
    login_user(pss_user)    
    identity_changed.send(current_app._get_current_object(), identity=Identity(pss_user.pss_user_id))
    pss_user_serializer = generate_pss_user_serializer(current_app)    
    user_dict=pss_user_serializer().dump(pss_user).data
    return jsonify({'pss_user':user_dict})

@blueprints.pss_admin_event_blueprint.route('/auth/pss_user/logout',methods=['GET'])
@blueprints.event_blueprint.route('/auth/pss_user/logout',methods=['GET'])
@load_tables
def pss_logout(tables):
    if current_user.is_anonymous() is False:
        logged_out_username=current_user.username
        logout_user()
    else:
        logged_out_username='anonymous'        
    return jsonify({'status':'%s is logged out' % logged_out_username})

@blueprints.event_blueprint.route('/auth/pss_event_user/login',methods=['POST'])
@load_tables
def pss_event_user_login(tables):    
    pss_event_user = pss_event_user_login_route(request,tables)
    login_user(pss_event_user)    
    identity_changed.send(current_app._get_current_object(), identity=Identity(pss_event_user.pss_user_id))
    pss_user_serializer = generate_pss_user_serializer(current_app)    
    user_dict=pss_user_serializer().dump(pss_event_user).data
    return jsonify({'pss_user':user_dict})

@blueprints.pss_admin_event_blueprint.route('/auth/pss_user/current_user',methods=['GET'])
@blueprints.event_blueprint.route('/auth/pss_event_user/current_user',methods=['GET'])
def get_current_user():
    if current_user.is_anonymous():
        return jsonify({'current_user':None})
    pss_user_serializer = generate_pss_user_serializer(current_app)    
    user_dict=pss_user_serializer().dump(current_user).data    
    return jsonify({'current_user':user_dict})

#FIXME : need get_current_user for event user
