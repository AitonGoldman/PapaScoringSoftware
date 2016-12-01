import unittest
from util import app_build 
from util.dispatch import PathDispatcher
import os
from tempfile import mkstemp
from gunicorn.http.wsgi import Response,WSGIErrorsWrapper, FileWrapper
from gunicorn.http.body import Body
#from app.types import ImportedTables
from mock import MagicMock
from util import db_util
from flask import Flask
from time import sleep
from util.db_info import DbInfo
import time

class TdIntegrationTestBase(unittest.TestCase):    
    def setUp(self):
        #FIXME : need to take new config structure into account
        self.secret_file_info = mkstemp()
        self.public_file_info = mkstemp()
        secret_file_name = self.secret_file_info[1]
        public_file_name = self.public_file_info[1]                
        self.db_temp_info = mkstemp()
        os.close(self.db_temp_info[0])
        os.close(self.secret_file_info[0])
        os.close(self.public_file_info[0])
        db_file_name=self.db_temp_info[1]
        
        flask_file_name = mkstemp()[1]                
        self.poop_db_file_name = mkstemp()[1]
        self.poop_db_name = os.path.basename(self.poop_db_file_name)        
        
        secret_file = open(secret_file_name,'w')
        secret_file.write('FLASK_SECRET_KEY=poop\n')
        secret_file.write('MAX_TICKETS_ALLOWED_PER_DIVISION=5\n')
        secret_file.write('QUEUE_BUMP_AMOUNT=0')

        secret_file.close()

        public_file = open(public_file_name,'w')
        #public_file.write("sqlite=true")
        #public_file.write("db_type=sqlite")
        public_file.close()

        db_file = open(db_file_name,'w')
        #public_file.write("sqlite=true")
        db_file.write("DB_TYPE=sqlite")
        public_file.close()

        
        flask_file = open(flask_file_name,'w')
        flask_file.write("")
        flask_file.close()

        os.environ['td_secret_config_filename']=secret_file_name
        os.environ['td_public_config_filename']=public_file_name
        #os.environ['db_config_filename']=db_file_name
        os.environ['DB_CONFIG_FILENAME']=db_file_name
        os.environ['TD_CONFIG_FILENAME']=secret_file_name
        os.environ['flask_config_filename']=flask_file_name
        
        self.admin_health_check_string = '{\n  "data": {\n    "status": "HEALTHY", \n    "user_count": %s\n  }\n}'
        self.metaadmin_health_check_string = '{\n  "data": "METAADMIN_HEALTHY"\n}'
        
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

    def create_short_env(self, url):
        return {'SERVER_NAME': '0.0.0.0', 'REQUEST_METHOD': 'GET', 'PATH_INFO': url, 'SERVER_PROTOCOL': 'HTTP/1.1', 'QUERY_STRING': '', 'RAW_URI': url,'wsgi.url_scheme': 'http','SERVER_PORT': '8000'}                

class TdIntegrationDispatchTestBase(TdIntegrationTestBase):
    def setUp(self):
        super(TdIntegrationDispatchTestBase,self).setUp()
        dummy_app = Flask('dummy_app')                
        db_util.create_db_and_tables(dummy_app,self.poop_db_name,DbInfo({'DB_TYPE':'sqlite'}),drop_tables=True)
        del dummy_app
        self.app = PathDispatcher(app_build.get_meta_admin_app, app_build.get_admin_app)                
        

