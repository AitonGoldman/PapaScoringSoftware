from flask import Flask
from sqlalchemy_utils import create_database, database_exists
from app import td_public, td_secret
from app.util import db_util,td_config, auth
from app.util.dispatch import PathDispatcher
import os
from app.types import ImportedTables
from werkzeug.exceptions import BadRequest

from app import routes

from blueprints import admin_login_blueprint,meta_admin_blueprint

def get_admin_app(name):
    app = Flask(name)
    app.register_error_handler(BadRequest, lambda e: 'bad request!')    
    app.config.from_pyfile('app/td_flask.py')
    app.register_blueprint(admin_login_blueprint)
    # FIXME : need to generate db_url by comparing "name" to good list of dbs
    db_url="postgresql://tom:tomPassword@localhost/%s" % name
    if not database_exists(db_url):
        return None        
    db_handle = db_util.create_db_handle(db_url,name,app)        
    app.tables = ImportedTables(db_handle)
    #FIXME : when we properly implement meta_admin,
    #        create_TD_tables() moves from here.
    if db_util.check_table_exists(db_handle) is False:
        db_util.create_TD_tables(app.tables.db_handle)        
    td_config.assign_loaded_config(app,'app/td_public.py','app/td_secret.py')
    auth.init_login_manager(app)
    return app

def get_meta_admin_app():    
    app = Flask("metaadmin")
    app.register_error_handler(BadRequest, lambda e: 'bad request!')        
    app.register_blueprint(meta_admin_blueprint)
    return app

App = PathDispatcher(get_meta_admin_app(), get_admin_app)

