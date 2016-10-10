from flask import Flask
from sqlalchemy_utils import create_database, database_exists
from app import td_public, td_secret
from app.util import db_util,td_config, auth
from app.util.dispatch import PathDispatcher
import os
from app.types import ImportedTables
from werkzeug.exceptions import BadRequest
from flask_principal import Principal
from flask_cors import CORS

from app import routes

from blueprints import admin_login_blueprint,meta_admin_blueprint,admin_manage_blueprint

def get_generic_app(name):
    db_url = db_util.generate_db_url(name)
    if not database_exists(db_url):        
        return None        
    app = Flask(name)
    principals = Principal(app)
    auth.generate_identity_loaded(app)    
    app.register_error_handler(BadRequest, lambda e: 'bad request!')        
    app.config.from_pyfile('app/td_flask.py')    
    td_config.assign_loaded_config(app,'app/td_public.py','app/td_secret.py')
    CORS(
        app,
        headers=['Content-Type', 'Accept'],
        send_wildcard=False,
        supports_credentials=True,
    )
    
    return app

def get_admin_app(name):
    if name == 'meta_admin':
        return None
    app = get_generic_app(name)
    if app:
        db_url = db_util.generate_db_url(name)
        db_handle = db_util.create_db_handle(db_url,app)
        app.tables = ImportedTables(db_handle)
        app.register_blueprint(admin_login_blueprint)
        app.register_blueprint(admin_manage_blueprint)                
        auth.init_login_manager(app)        
    
    return app

def get_meta_admin_app():    
    app = get_generic_app('meta_admin')
    app.register_blueprint(meta_admin_blueprint)
    return app

App = PathDispatcher(get_meta_admin_app(), get_admin_app)

