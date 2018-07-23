from lib_v2 import blueprints
from flask import jsonify,current_app,request
from itsdangerous import URLSafeSerializer
from werkzeug.exceptions import BadRequest,Unauthorized,Conflict
from flask_mail import Message
import json

@blueprints.test_blueprint.route('/pss_user_request',methods=['POST'])
def request_pss_user_creations():                    
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Details not specified')        

    flask_secret_key=current_app.secret_key
    
    s = URLSafeSerializer(flask_secret_key)

    #https://stackoverflow.com/questions/37058567/configure-flask-mail-to-use-gmail
    #
    #Important part from link : https://security.google.com/settings/security/apppasswords    
    msg = Message("PSS user account activation",
                  sender="papa.scoring.software@gmail.com",
                  recipients=[input_data['email']]
                  )
    info = {'username':input_data['username'],
            'first_name':input_data['first_name'],
            'last_name':input_data['last_name'],
            'email':input_data['email'],
            'password':input_data['password']}    
    msg.body = "here is a link : http://0.0.0.0:8100/#/EventOwnerConfirm/%s" % s.dumps(info)
    current_app.mail.send(msg)
    return jsonify({})

@blueprints.test_blueprint.route('/pss_user_request_confirm/<itsdangerous_string>',methods=['POST'])
def confirm_pss_user_creations(itsdangerous_string):                    
    flask_secret_key=current_app.secret_key
    s = URLSafeSerializer(flask_secret_key)    
    new_user_info = s.loads(itsdangerous_string)
    new_user = current_app.table_proxy.create_user(new_user_info['username'],
                                                   new_user_info['first_name'],
                                                   new_user_info['last_name'],
                                                   new_user_info['password'],
                                                   True)
    if 'extra_title' in new_user_info:
        new_user.extra_title = new_user_info['extra_title']
    current_app.table_proxy.db_handle.session.add(new_user)
    current_app.table_proxy.commit_changes()
    #admin_role = tables.AdminRoles.query.filter_by(name=roles_constants.PSS_USER).first()
    #new_user_info['role_id']=admin_role.admin_role_id
    #new_user = orm_factories.check_user_create_is_valid(new_user_info,current_app)
    #tables.db_handle.session.add(new_user)
    #tables.db_handle.session.commit()    
    new_user_info['password']=None
    return jsonify({'data':new_user_info})
