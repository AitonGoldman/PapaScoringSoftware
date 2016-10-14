from flask import Flask
from sqlalchemy_utils import create_database, database_exists
from app import td_public, td_secret
from app.util import db_util,td_config, auth
from app.util.pg_info import build_PgInfo
from app.util.dispatch import PathDispatcher
import os
from app.types import ImportedTables
from werkzeug.exceptions import BadRequest
from flask_principal import Principal
from flask_cors import CORS
from flask_login import LoginManager

from app import routes

from app.blueprints import admin_login_blueprint,meta_admin_blueprint,admin_manage_blueprint

def get_generic_app(name):
    app = Flask(name)
    flask_config_file=os.getenv('flask_config_file','app/td_flask.py')
    td_public_config_file=os.getenv('td_public_config_file','app/td_public.py')
    td_secret_config_file=os.getenv('td_secret_config_file','app/td_secret.py')
    app.config.from_pyfile(flask_config_file)    
    td_config.assign_loaded_config(app,td_public_config_file,td_secret_config_file)
    pg_info = build_PgInfo(app)
    use_sqlite = app.td_config['sqlite']    
    db_url = db_util.generate_db_url(name,pg_info=pg_info,use_sqlite=use_sqlite)                 
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

def get_admin_app(name):
    if name == 'meta_admin':
        return None
    app = get_generic_app(name)            
    if app:
        pg_info = build_PgInfo(app)
        use_sqlite = app.td_config['sqlite']
        db_url = db_util.generate_db_url(name,pg_info=pg_info,use_sqlite=use_sqlite)            
        if not database_exists(db_url):
            return None            
        db_handle = db_util.create_db_handle(db_url, app)
        app.tables = ImportedTables(db_handle)
        app.register_blueprint(admin_login_blueprint)
        app.register_blueprint(admin_manage_blueprint)                        
        LoginManager().init_app(app)
        auth.generate_user_loader(app)
        auth.generate_identity_loaded(app)
    return app

def get_meta_admin_app():        
    app = get_generic_app('meta_admin')    
    app.register_blueprint(meta_admin_blueprint)
    return app
