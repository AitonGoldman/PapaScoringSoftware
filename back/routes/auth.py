from lib.flask_lib import blueprints
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

def load_tables(f):
    @wraps(f)
    def new_f(*args,**kwargs):
        return f(current_app.tables,*args,**kwargs)
    return new_f

#FIXME : make sure all PssUser instances are called pss_user
def check_pss_user_has_admin_site_access(pss_user):
    user_roles = [role.name for role in pss_user.roles]        
    allowed_roles = [roles.PSS_ADMIN,roles.PSS_USER]        
    if len(list(set(allowed_roles) & set(user_roles))) == 0:
        raise Unauthorized('User can not access this') 
    return True


def pss_admin_login_route(request,tables):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Username or password not specified')        
    pss_user = tables.PssUsers.query.options(joinedload("roles")).filter_by(username=input_data['username']).first()        
    if pss_user and not pss_user.verify_password(input_data['password']):
       pss_user = None
    if pss_user is None:
       raise Unauthorized('Bad username or password')    
    check_pss_user_has_admin_site_access(pss_user)
    return pss_user

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
@load_tables
def pss_admin_logout(tables):
    if current_user.is_anonymous() is False and check_pss_user_has_admin_site_access(current_user):
        logged_out_username=current_user.username
        logout_user()
    else:
        logged_out_username='anonymous'        
    return jsonify({'status':'%s is logged out' % logged_out_username})

#FIXME : need get_current_user
