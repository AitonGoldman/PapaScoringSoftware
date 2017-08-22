import random
from flask import Flask
from lib import bootstrap
from lib.PssConfig import PssConfig
import os
from lib.flask_lib.dispatch import PathDispatcher
from mock import MagicMock
from gunicorn.http.wsgi import Response,WSGIErrorsWrapper, FileWrapper

test_db_name_for_run='test_db_%s' % random.randrange(9999999)
PSS_ADMIN_EVENT = "pss_admin_test"
pss_config = None
app=None

def static_setup():    
    global app,test_db_name_for_run,PSS_ADMIN_EVENT,pss_config    
    if app is None:
        create_test_db(test_db_name_for_run)
        pss_config = PssConfig()
        app = PathDispatcher()            
        initialize_pss_admin_app_in_db(db_name=test_db_name_for_run)
        response,results = dispatch_request('/%s/this_does_not_exist' % PSS_ADMIN_EVENT)
                
def create_test_db(db_name=None):    
    global PSS_ADMIN_EVENT,pss_config    
    dummy_app = Flask(PSS_ADMIN_EVENT)            
    pss_config.get_db_info(db_name=db_name).create_db_and_tables(dummy_app,False)        
    del dummy_app
    
def initialize_pss_admin_app_in_db(db_name=None):        
    global PSS_ADMIN_EVENT,pss_config
    pss_admin_app = Flask(PSS_ADMIN_EVENT)        
    tables = pss_config.get_db_info(db_name=db_name).getImportedTables(pss_admin_app,"unimportant")
    bootstrap.bootstrap_pss_admin_event(tables,PSS_ADMIN_EVENT)
    del pss_admin_app

def dispatch_request(url):        
    global app
    mocked_socket = MagicMock()                
    mocked_request = MagicMock()                
    response = Response(mocked_request, mocked_socket, None)
    req_env = create_full_env(url)        
    return response,app(req_env,response.start_response)

def create_full_env(url):
    socket = MagicMock()
    error = MagicMock()
    fw = MagicMock()
    body = MagicMock()
    return {'HTTP_REFERER': 'http://localhost/dist_2/',
            'SERVER_SOFTWARE': 'gunicorn/19.3.0',
            'SCRIPT_NAME': '',
            'REQUEST_METHOD': 'GET',
            'PATH_INFO': url,
            'HTTP_ORIGIN': 'http://localhost',
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'QUERY_STRING': '',
            'HTTP_USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:49.0) Gecko/20100101 Firefox/49.0',
            'HTTP_CONNECTION': 'keep-alive',
            'HTTP_COOKIE': 'session=.eJyrVorPTFGyqlZSSFKyUvIN8cqKCg819quKNPXLyq6KNPLK8ctyNfatysjwC3fL9A8PNPDLysnwDUm3VarVUcpMSc0rySyp1EssLcmIL6ksSFWyyivNyUGSAZluUgsAzZoixw.CuJ5xA.agefXt7Vfjcyp7ql3Phgp8aBdAU',
            'SERVER_NAME': '0.0.0.0',
            'REMOTE_ADDR': '192.168.1.178',
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '8000',
            'REMOTE_PORT': '52458',
            'wsgi.input': body,                
            'HTTP_HOST': '192.168.1.178:8000',
            'wsgi.multithread': False,
            'HTTP_CACHE_CONTROL': 'max-age=0',
            'HTTP_ACCEPT': 'application/json, text/plain, */*',
            'wsgi.version': (1, 0),
            'RAW_URI': url,
            'wsgi.run_once': False,
            'wsgi.errors': error,                
            'wsgi.multiprocess': False,
            'HTTP_ACCEPT_LANGUAGE': 'en-US,en;q=0.5',
            'gunicorn.socket': socket,
            'wsgi.file_wrapper': fw,                
            'HTTP_ACCEPT_ENCODING': 'gzip, deflate'}

        
        
