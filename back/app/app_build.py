from CustomJsonEncoder import CustomJSONEncoder
from pss_models import ImportedTables
from flask import Flask
from lib import db_util
import auth, pss_config
from lib.db_info import DbInfo
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

def get_event_app(name):
    instance_config = pss_config.get_pss_instance_config()                
    configured_app = get_base_app(name, instance_config)
    if name == instance_config['pss_admin_event_name']:
        configured_app.register_blueprint(blueprints.pss_admin_event_blueprint)
    else:
        configured_app.register_blueprint(blueprints.event_blueprint)
    return configured_app

def get_base_app(name, instance_config):    
    app = Flask(name)
    app.json_encoder = CustomJSONEncoder            
    principals = Principal(app)    
    app.my_principals = principals
    #app.register_error_handler(BadRequest, lambda e: 'bad request!')        
    CORS(
        app,
        headers=['Content-Type', 'Accept'],
        send_wildcard=False,
        supports_credentials=True,
    )
    db_config = instance_config
    db_info = DbInfo(db_config)    
    db_url = db_util.generate_db_url(name,db_info)        
    db_handle = db_util.create_db_handle(app,db_url)
    app.tables = ImportedTables(db_handle, name, instance_config['pss_admin_event_name'])    
    pss_config.set_event_config_from_db(app)    
    LoginManager().init_app(app)
    auth.generate_user_loader(app)
    auth.generate_identity_loaded(app)
    for code in default_exceptions.iterkeys():
        app.error_handler_spec[None][code] = make_json_error
    #app.register_blueprint(admin_login_blueprint)
    #app.register_blueprint(admin_manage_blueprint)                        
        
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

