import unittest
from lib import roles_constants,orm_factories,bootstrap
from gunicorn.http.wsgi import Response,WSGIErrorsWrapper, FileWrapper
from gunicorn.http.body import Body
from mock import MagicMock
from flask import Flask
from time import sleep
from sqlalchemy_utils import drop_database
import time
import json
import random
from lib.PssConfig import PssConfig
from lib.flask_lib.dispatch import PathDispatcher
import os

PSS_ADMIN_EVENT = "pss_admin_test"
class PssIntegrationTestBase(unittest.TestCase):        
    def create_test_db(self):
        dummy_app = Flask(PSS_ADMIN_EVENT)
        self.pss_config.get_db_info().create_db_and_tables(dummy_app,True)        
        del dummy_app
    
    def initialize_pss_admin_app_in_db(self):        
        pss_admin_app = Flask(PSS_ADMIN_EVENT)        
        tables = self.pss_config.get_db_info().getImportedTables(pss_admin_app,"unimportant")
        bootstrap.bootstrap_pss_admin_event(tables,PSS_ADMIN_EVENT)
        del pss_admin_app

    def get_event_app_in_db(self,app_name):        
        response,results = self.dispatch_request('/%s/this_does_not_exist' % app_name)
        return self.app.instances[app_name]                 
        
    def setUp(self):
        #pss_config.check_db_connection_env_vars_set()
        self.test_db_name='test_db_%s' % random.randrange(9999999)
        os.environ['pss_db_name']=self.test_db_name
        os.environ['pss_admin_event_name']=PSS_ADMIN_EVENT

        self.pss_config = PssConfig()

        self.create_test_db()
        self.initialize_pss_admin_app_in_db()

        self.app = PathDispatcher()                
        response,results = self.dispatch_request('/%s/this_does_not_exist' % PSS_ADMIN_EVENT)
        self.pss_admin_app = self.app.instances[PSS_ADMIN_EVENT]
        bootstrap.bootstrap_roles(self.pss_admin_app.tables)
        self.bootstrap_pss_users(self.pss_admin_app)
        
    def dispatch_request(self,url):
        mocked_socket = MagicMock()                
        mocked_request = MagicMock()                
        response = Response(mocked_request, mocked_socket, None)
        req_env = self.create_full_env(url)        
        return response,self.app(req_env,response.start_response)

    def create_full_env(self,url):
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
    
    def assertHttpCodeEquals(self,http_response, http_response_code_expected):
        error_string = 'Was expecting status code %s, but it was %s with message of %s' % (http_response_code_expected, http_response.status_code,http_response.data)
        self.assertEquals(http_response.status_code,
                          http_response_code_expected,
                          error_string)
        
    def bootstrap_pss_users(self, app):
        tables = app.tables
        role_admin=tables.AdminRoles.query.filter_by(name=roles_constants.PSS_ADMIN).first()
        role_user=tables.AdminRoles.query.filter_by(name=roles_constants.PSS_USER).first()
        role_player=tables.AdminRoles.query.filter_by(name=roles_constants.TEST).first()
        admin_pss_user = orm_factories.create_user(app,
                                                   'test_pss_admin_user',
                                                   'password',
                                                   [role_admin])
        normal_pss_user = orm_factories.create_user(app,
                                                    'test_pss_user',
                                                    'password2',
                                                    [role_user])
        player = orm_factories.create_user(app,
                                           'test_player',
                                           'password3',
                                           [role_player])
        pss_user_with_no_roles = orm_factories.create_user(app,
                                                           'test_pss_user_no_roles',
                                                           'password',
                                                           [])
        tables.db_handle.session.commit()        
        
    def tearDown(self):                        
        db_url = self.pss_config.get_db_info().generate_db_url()
        #drop_database(db_url)
        
