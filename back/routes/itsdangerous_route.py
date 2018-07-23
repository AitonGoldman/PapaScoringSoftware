from itsdangerous import URLSafeSerializer
from flask import Flask
from lib.flask_lib import blueprints
from lib.flask_lib.permissions import create_pss_event_permissions
from flask import jsonify,current_app,request
from werkzeug.exceptions import BadRequest,Unauthorized,Conflict
from flask_login import login_user, logout_user, current_user
import json
from lib.PssConfig import PssConfig
from lib.serializer import generic
from lib import serializer,roles_constants
from lib.serializer.deserialize import deserialize_json
from lib.route_decorators.db_decorators import load_tables
from lib.route_decorators.auth_decorators import check_current_user_is_active
from flask_mail import Message
from pss_models.PssUsers import generate_pss_user_event_role_mapping
import os
from lib import orm_factories

@blueprints.pss_admin_event_blueprint.route('/itsdangerous/pss_user',methods=['POST'])
@load_tables
def request_pss_user_creations(tables):                    
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Details not specified')        

    flask_secret_key=tables.Events.query.filter_by(name=current_app.name).first().flask_secret_key
    
    s = URLSafeSerializer(flask_secret_key)

    #https://stackoverflow.com/questions/37058567/configure-flask-mail-to-use-gmail
    #
    #Important part from link : https://security.google.com/settings/security/apppasswords
    print input_data['email']
    msg = Message("PSS user account activation",
                  sender="papa.scoring.software@gmail.com",
                  recipients=[input_data['email']]
                  )
    info = {'username':input_data['username'],
            'first_name':input_data['first_name'],
            'last_name':input_data['last_name'],
            'email':input_data['email'],
            'password':input_data['password']}    
    msg.body = "here is a link : http://0.0.0.0:8100/admin.html#/app/register_new_pss_user_confirm?itsdangerous=%s" % s.dumps(info)    
    current_app.mail.send(msg)
    return jsonify({})

@blueprints.pss_admin_event_blueprint.route('/itsdangerous/pss_user_confirm/<itsdangerous_string>',methods=['GET'])
@load_tables
def confirm_pss_user_creations(tables,itsdangerous_string):                    
    flask_secret_key=tables.Events.query.filter_by(name=current_app.name).first().flask_secret_key    
    s = URLSafeSerializer(flask_secret_key)    
    new_user_info = s.loads(itsdangerous_string)
    print new_user_info
    admin_role = tables.AdminRoles.query.filter_by(name=roles_constants.PSS_USER).first()
    new_user_info['role_id']=admin_role.admin_role_id
    new_user = orm_factories.check_user_create_is_valid(new_user_info,current_app)
    tables.db_handle.session.add(new_user)
    tables.db_handle.session.commit()    
    return jsonify(new_user_info)
