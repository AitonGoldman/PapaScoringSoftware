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
        
    def create_user_for_test(self,app,
                             username,
                             first_name=None,last_name=None,
                             password=None,extra_title=None,
                             role_name=None):
        
        with app.test_client() as c:
            rv = c.post('/auth/pss_user/login',
                        data=json.dumps({'username':self.admin_pss_user.username,'password':self.admin_pss_user_password}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.get('/roles')            
            if password is None:
                password=self.create_uniq_id()
            if first_name is None:
                first_name=self.create_uniq_id()
            if last_name is None:
                last_name=self.create_uniq_id()
            if role_name is None:
                pss_user_role = [role for role in json.loads(rv.data)['roles'] if (role['name'] == roles_constants.PSS_USER)][0]
            else:
                pss_user_role = [role for role in json.loads(rv.data)['roles'] if (role['name'] == role_name)][0]            
            rv = c.post('/pss_user',
                        data=json.dumps({'username':username,
                                         'password':password,
                                         'first_name':first_name,
                                         'last_name':last_name,
                                         'extra_title':extra_title,
                                         'role_id':pss_user_role['admin_role_id']}))
            self.assertHttpCodeEquals(rv,200)            
        
    # def bootstrap_extra_users(self,app):
    #     self.create_user_for_test(app
    #                               username,
    #                               first_name,last_name=None,
    #                               password=None,extra_title=None,
    #                               role_name=None)
    #     # self.pss_user_with_no_roles_password='password455'                
    #     # self.pss_user_with_no_roles = orm_factories.create_user(app,
    #     #                                                         'test_pss_user_no_roles%s' % self.create_uniq_id(),
    #     #                                                         'test_event_2_first_name',
    #     #                                                         'test_event_2_last_name',
    #     #                                                         self.pss_user_with_no_roles_password)
    #     # tables = app.tables
    #     # tables.db_handle.session.commit()        


