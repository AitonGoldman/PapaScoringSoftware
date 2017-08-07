from flask import Flask
from pss_models import ImportedTables
from threading import Lock
from werkzeug.wsgi import pop_path_info, peek_path_info
from werkzeug.exceptions import BadRequest
import app_build
import os
from lib.PssConfig import PssConfig
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
                pss_config = PssConfig()
                unconfigured_app = Flask(prefix)
                db_handle = pss_config.get_db_info().create_db_handle(unconfigured_app)
                unconfigured_app.tables = ImportedTables(db_handle, prefix, pss_config.pss_admin_event_name)                                    
                configured_app_instance = app_build.get_event_app(unconfigured_app,pss_config)                
                if configured_app_instance is not None:                    
                    self.instances[prefix] = configured_app_instance                                                    
            return configured_app_instance

    def __call__(self, environ, start_response):
        
        app = self.get_application(peek_path_info(environ))
        pop_path_info(environ)
        return app(environ, start_response)
