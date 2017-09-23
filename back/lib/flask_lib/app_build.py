from lib.CustomJsonEncoder import CustomJSONEncoder
from lib.flask_lib import auth
import os
from werkzeug.exceptions import BadRequest,default_exceptions, HTTPException
from flask_principal import Principal,Permission
from flask_cors import CORS
from flask_login import LoginManager
from flask import jsonify
from json import loads, dumps
from traceback import format_exception_only
import calendar
import datetime
import blueprints
import routes
#from flask_marshmallow import Marshmallow
from flask_mail import Mail

def generate_check_event_config(pss_config):
    def check_event_config():
        from flask import current_app
        pss_config.set_event_config_from_db(current_app)        
    return check_event_config

def get_event_app(app, pss_config):
    configured_app = get_base_app(app,pss_config)    
    if app.name == pss_config.pss_admin_event_name:        
        auth.generate_pss_user_loader(configured_app)
        auth.generate_pss_user_identity_loaded(configured_app)

        configured_app.register_blueprint(blueprints.pss_admin_event_blueprint)
    else:        
        #FIXME : will need new methods to handle users and players
        auth.generate_pss_user_loader(configured_app)
        auth.generate_pss_user_identity_loaded(configured_app)
        configured_app.register_blueprint(blueprints.event_blueprint)
    return configured_app

def get_base_app(app, pss_config):    
    app.config['DEBUG']=True
    app.config['SESSION_COOKIE_PATH']='/%s'%app.name
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    #FIXME : need a null check for mail info
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')    
    mail = Mail(app)
    app.mail=mail
    app.json_encoder = CustomJSONEncoder            
    principals = Principal(app)    
    app.my_principals = principals    
    CORS(
        app,
        headers=['Content-Type', 'Accept'],
        send_wildcard=False,
        supports_credentials=True,
    )
    
    pss_config.set_event_config_from_db(app)    
    LoginManager().init_app(app)
    for code in default_exceptions.iterkeys():
        app.error_handler_spec[None][code] = make_json_error

    #app.ma = Marshmallow(app)
    app.before_request(generate_check_event_config(pss_config))
    return app

def make_json_error(ex):
    """Turn an exception into a chunk of JSON"""
    response = jsonify({})
    response_dict = loads(response.get_data())
    if hasattr(ex, 'state_go'):
        response_dict['state_go'] = ex.state_go
    if isinstance(ex, HTTPException):
        response.status_code = ex.code
        if isinstance(ex.description, Permission):
            response_dict['message'] = "Permission denied"
        else:
            response_dict['message'] = str(ex.description)
    else:
        response.status_code = 500
        response_dict['message'] = str(ex)
    if response.status_code == 500:
        response_dict['stack'] = str(format_exception_only(type(ex), ex))
    response.set_data(dumps(response_dict))
    return response

