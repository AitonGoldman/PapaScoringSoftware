from flask import Flask
from pss_models import ImportedTables
from threading import Lock
from werkzeug.wsgi import pop_path_info, peek_path_info
from werkzeug.exceptions import BadRequest
import app_build
import os
import pss_config
from lib.db_info import DbInfo
from lib import db_util
from sqlalchemy_utils import database_exists
from flask_sqlalchemy import SQLAlchemy

class PathDispatcher(object):
    def __init__(self):
        self.lock = Lock()
        self.instances = {}

    def get_application(self, prefix):
        with self.lock:            
            app_instance = self.instances.get(prefix)
            if app_instance is None:
                instance_config = pss_config.get_pss_instance_config()                                
                db_info = DbInfo(instance_config)    
                db_url = db_util.generate_db_url(instance_config['pss_admin_event_name'],db_info)
                app = Flask(prefix)
                db_handle = db_util.create_db_handle(app,db_url)
                app.tables = ImportedTables(db_handle, prefix, instance_config['pss_admin_event_name'])                    
                app_instance = app_build.get_event_app(prefix,app,instance_config)                
                if app_instance is not None:                    
                    self.instances[prefix] = app_instance                                                    
            return app_instance

    def __call__(self, environ, start_response):
        
        app = self.get_application(peek_path_info(environ))
        pop_path_info(environ)
        return app(environ, start_response)
