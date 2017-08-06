from threading import Lock
from werkzeug.wsgi import pop_path_info, peek_path_info
from werkzeug.exceptions import BadRequest
import app_build
import pss_config
import os

class PathDispatcher(object):
    def __init__(self):
        self.lock = Lock()
        self.instances = {}

    def get_application(self, prefix):
        with self.lock:            
            app_instance = self.instances.get(prefix)
            if app_instance is None:
                app_instance = app_build.get_event_app(prefix)                
                if app_instance is not None:                    
                    self.instances[prefix] = app_instance                                                    
            return app_instance

    def __call__(self, environ, start_response):        
        #FIXME : need to get all env vars HERE (i.e. db info, name of pss_admin event) and pass them in to get_application         
        app = self.get_application(peek_path_info(environ))
        pop_path_info(environ)
        return app(environ, start_response)
