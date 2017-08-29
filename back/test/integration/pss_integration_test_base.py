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
import datetime
from test.integration import test_db_name_for_run,static_setup,PSS_ADMIN_EVENT,dispatch_request


class PssIntegrationTestBase(unittest.TestCase):        

    def create_uniq_id(self):
        random_string = ""
        for x in range(15):
            random_string = random_string+chr(random.randrange(97,122))        
        return random_string
        
    def get_event_app_in_db(self,app_name):        
         response,results = self.dispatch_request('/%s/this_does_not_exist' % app_name)
         return self.app.instances[app_name]                 
        
    def bootstrap_pss_users(self,app):
        tables = app.tables
        self.admin_pss_user = tables.PssUsers.query.filter_by(username='test_pss_admin_user').first()
        self.admin_pss_user_password='password55'
        if self.admin_pss_user:
            return
        role_admin=tables.AdminRoles.query.filter_by(name=roles_constants.PSS_ADMIN).first()        
        #role_user=tables.AdminRoles.query.filter_by(name=roles_constants.PSS_USER).first()
        #role_player=tables.AdminRoles.query.filter_by(name=roles_constants.TEST).first()
        #FIXME : should use self.create_users function
        self.admin_pss_user = orm_factories.create_user(app,                                                       
                                                        'test_pss_admin_user',
                                                        'test_first_name','test_last_name',
                                                        self.admin_pss_user_password,
                                                        admin_roles=[role_admin])
        tables.db_handle.session.commit()                
        
    def setUp(self):        
        self.test_db_name=test_db_name_for_run
        os.environ['pss_db_name']=test_db_name_for_run
        os.environ['pss_admin_event_name']=PSS_ADMIN_EVENT        
        static_setup()
        self.pss_config = PssConfig()
        from test.integration import app
        self.dispatch_request=dispatch_request
        self.app = app        
        self.pss_admin_app = app.instances[PSS_ADMIN_EVENT]                
        bootstrap.bootstrap_roles(self.pss_admin_app.tables)        
        self.bootstrap_pss_users(self.pss_admin_app)                
                
    def assertHttpCodeEquals(self,http_response, http_response_code_expected):
        error_string = 'Was expecting status code %s, but it was %s with message of %s' % (http_response_code_expected, http_response.status_code,http_response.data)
        self.assertEquals(http_response.status_code,
                          http_response_code_expected,
                          error_string)
        
    def bootstrap_extra_users(self,app):
        self.pss_user_with_no_roles_password='password455'                
        self.pss_user_with_no_roles = orm_factories.create_user(app,
                                                                'test_pss_user_no_roles%s' % self.create_uniq_id(),
                                                                'test_event_2_first_name',
                                                                'test_event_2_last_name',
                                                                self.pss_user_with_no_roles_password)
        tables = app.tables
        tables.db_handle.session.commit()        


