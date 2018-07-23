from celery import Celery
from flask_mail import Mail
from json import loads, dumps
from flask_principal import Principal, Permission
from flask_login import LoginManager
import os
from lib_v2.CustomJsonEncoder import CustomJSONEncoder
from flask_cors import CORS
from flask import jsonify
from werkzeug.exceptions import default_exceptions, HTTPException
from flask import request
from traceback import format_exception_only
from lib_v2 import blueprints, needs, permissions,principal_identity_funcs
from lib_v2.PssConfig import PssConfig
from lib_v2.TableProxy import TableProxy
from werkzeug.wsgi import pop_path_info, peek_path_info
from StripeProxy import StripeProxy
from werkzeug.exceptions import BadRequest
import json

def make_celery(app):

    celery = Celery('celery_app', backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

#def generate_celery_method(app):
#    @app.celery.task()
#    def add_together(a, b):
#        return a + b
#    return add_together

 
def configure_base_app(app):    
    app.config['DEBUG']=True
    app.config['UPLOAD_FOLDER']='/tmp'
    app.config['IMG_HTTP_SRV_DIR']=os.getenv('IMG_HTTP_SRV_DIR')
    #app.config['SESSION_COOKIE_PATH']='/%s'%app.name
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    #FIXME : need a null check for mail info
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')    
    app.config['CELERY_BROKER_URL']=os.getenv('CELERY_BROKER_URL')
    app.config['CELERY_RESULT_BACKEND']=os.getenv('CELERY_RESULT_BACKEND')    
    mail = Mail(app)
    app.mail=mail
    app.json_encoder = CustomJSONEncoder            
    principals = Principal(app)    
    app.my_principals = principals    
    CORS(
        app,
        headers=['Content-Type', 'Accept'],
        vary_header=False,
        #send_wildcard=False,        
        supports_credentials=True
    )    
    LoginManager().init_app(app)
    for code in default_exceptions.iterkeys():
        app.error_handler_spec[None][code] = make_json_error
    #FIXME : THIS SHOULD COME FROM THE DB
    app.secret_key = os.getenv("FLASK_SECRET_KEY")
    #app.celery = make_celery(app)
    #app.test_celery = generate_celery_method(app)
    
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

def get_event_name_from_request():        
    pop_path_info(request.environ)
    #print request.environ    

def generate_event_settings_hash_setter(app):
    def event_settings_hash_setter():        
        app.event_settings={}
        events = app.table_proxy.Events.query.all()
        for event in events:
            app.event_settings[event.event_id]=event
    return event_settings_hash_setter

def generate_check_for_correct_client_version(app):
    def check_for_correct_client_version():
        if 'version' in request.args and request.args['version']=='3':
            return
        raise BadRequest('The version of the Papa Scoring Software you are using is no longer supported.  You must upgrade to the newest version.')
    return check_for_correct_client_version            
def build_app(app):    
    pss_config = PssConfig()
    pss_config.get_db_info().check_database_exists()
    app.db_handle = pss_config.get_db_info().create_db_handle(app)
    app.register_blueprint(blueprints.test_blueprint,url_prefix='/api')
    app.table_proxy=TableProxy()
    app.table_proxy.initialize_tables(app.db_handle)    
    app.before_request(generate_event_settings_hash_setter(app))
    app.before_request(generate_check_for_correct_client_version(app))    
    
    configure_base_app(app)
    principal_identity_funcs.generate_pss_user_loader(app)
    principal_identity_funcs.generate_pss_user_identity_loaded(app)
    app.stripe_proxy=StripeProxy(app.table_proxy)
    return app

