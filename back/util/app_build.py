from flask import Flask
from sqlalchemy_utils import create_database, database_exists
from util import db_util, auth, td_config
from util.db_info import DbInfo
from util.dispatch import PathDispatcher
import os
from td_types import ImportedTables
from werkzeug.exceptions import BadRequest
from flask_principal import Principal
from flask_cors import CORS
from flask_login import LoginManager
from flask import jsonify
from json import loads, dumps
from werkzeug.exceptions import default_exceptions, HTTPException
from traceback import format_exception_only
from flask_principal import Permission
import routes
from blueprints import admin_login_blueprint,meta_admin_blueprint,admin_manage_blueprint
import calendar
import datetime
from flask.json import JSONEncoder

class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                if obj.utcoffset() is not None:
                    obj = obj - obj.utcoffset()
                millis = int(
                    calendar.timegm(obj.timetuple()) * 1000 +
                    obj.microsecond / 1000
                )
                return millis
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


def get_generic_app(name):    
    app = Flask(name)
    app.json_encoder = CustomJSONEncoder
    #app.config['UPLOAD_FOLDER']='/var/www/html/pics'
    app.config['UPLOAD_FOLDER']=os.getenv('UPLOAD_FOLDER',None)
    app.config['DEBUG']=True
    td_config.assign_loaded_configs_to_app(app)    
    principals = Principal(app)    
    app.my_principals = principals
    app.register_error_handler(BadRequest, lambda e: 'bad request!')        
    CORS(
        app,
        headers=['Content-Type', 'Accept'],
        send_wildcard=False,
        supports_credentials=True,
    )
    
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

def get_admin_app(name):
    #FIXME : this actually gets ALL config values, not just db values
    db_config = td_config.get_db_config()
    #secret_config,public_config = td_config.get_configs()    
    db_info = DbInfo(db_config)    
    db_url = db_util.generate_db_url(name,db_info)    
    if not database_exists(db_url):
        return None                
    app = get_generic_app(name)                            
    db_handle = db_util.create_db_handle(db_url, app)
    app.tables = ImportedTables(db_handle)
    app.register_blueprint(admin_login_blueprint)
    app.register_blueprint(admin_manage_blueprint)                        
    LoginManager().init_app(app)
    auth.generate_user_loader(app)
    auth.generate_identity_loaded(app)
    for code in default_exceptions.iterkeys():
        app.error_handler_spec[None][code] = make_json_error    
    return app

def get_meta_admin_app():        
    app = get_generic_app('meta_admin')    
    app.register_blueprint(meta_admin_blueprint)
    return app
