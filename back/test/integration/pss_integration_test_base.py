import unittest
from lib import roles
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

class PssIntegrationTestBase(unittest.TestCase):    
    def create_test_db(self):
        dummy_app = Flask('dummy_app')
        self.pss_config.get_db_info().create_db_and_tables(dummy_app,True)        
        del dummy_app
        
    def initialize_pss_admin_app_in_db(self):
        pss_admin_app = Flask('pss_admin')
        db_handle = self.pss_config.get_db_info().create_db_handle(pss_admin_app)        
        #FIXME : need constants for these strings
        result = db_handle.engine.execute("insert into events (flask_secret_key,name) values ('poop','pss_admin')")        
        db_handle.engine.dispose()
        del pss_admin_app
        
    def setUp(self):
        #pss_config.check_db_connection_env_vars_set()
        self.test_db_name='test_db_%s' % random.randrange(9999999)
        os.environ['pss_db_name']=self.test_db_name
        self.pss_config = PssConfig()

        self.create_test_db()
        self.initialize_pss_admin_app_in_db()

        self.app = PathDispatcher()                
        response,results = self.dispatch_request('/pss_admin/this_does_not_exist')
        self.pss_admin_app = self.app.instances['pss_admin']
        
        
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
        error_string = 'Was expecting status code %s, but it was %s' % (http_response_code_expected, http_response.status_code)
        self.assertEquals(http_response.status_code,
                          http_response_code_expected,
                          error_string)
        
    def generate_test_user(self,tables,username,password,roles):
        user = tables.PssUsers(username=username)
        user.crypt_password(password)
        tables.db_handle.session.add(user)
        for role in roles:
            user.roles.append(role)        
        
    def bootstrap_pss_users(self, app):
        db_handle = self.pss_config.get_db_info().create_db_handle(app)        
        tables = self.pss_config.get_db_info().getImportedTables(app,"pss_admin")
        #FIXME : need constants for these strings        
        role_admin=tables.Roles(name=roles.PSS_ADMIN)
        role_user=tables.Roles(name=roles.PSS_USER)
        role_test=tables.Roles(name=roles.TEST)
        tables.db_handle.session.add(role_admin)
        tables.db_handle.session.add(role_user)
        tables.db_handle.session.add(role_test)

        admin_pss_user = self.generate_test_user(tables,
                                                 'test_pss_admin_user',
                                                 'password',
                                                 [role_admin])
        normal_pss_user = self.generate_test_user(tables,
                                                  'test_pss_user',
                                                  'password2',
                                                  [role_user])
        pss_user_with_no_roles = self.generate_test_user(tables,
                                                         'test_pss_user_no_roles',
                                                         'password3',
                                                         [])
        
        tables.db_handle.session.commit()        
        
    def tearDown(self):                
        db_url = self.pss_config.get_db_info().generate_db_url()
        #drop_database(db_url)
        
