import unittest
import os
from mock import MagicMock
import pss_integration_test_base

import json
from flask_login import current_user
from lib import roles_constants

#FIXME : change name of class/file

class RoutePssLogin(pss_integration_test_base.PssIntegrationTestBase):
    def setUp(self):
        super(RoutePssLogin,self).setUp()        
    #FIXME : make tests more defensive - i.e. check if can do things before you login
    def test_login_good_user_good_password(self):
        with self.pss_admin_app.test_client() as c:                        
            rv = c.post('/auth/pss_user/login',
                        data=json.dumps({'username':self.admin_pss_user.username,'password':self.admin_pss_user_password}))
            self.assertHttpCodeEquals(rv,200)            
            self.assertTrue(hasattr(current_user, 'username'),                              
                            "Was expecting current_user to have a username attr, but it did not")
            self.assertEquals(current_user.username,
                              self.admin_pss_user.username,
                              "expected user to be test_pss_admin_user, but got %s" % (current_user.username))
            self.assertTrue(current_user.is_authenticated(),                              
                             "Was expecting user to be logged in, but user was not logged in")            
            returned_user = json.loads(rv.data)['pss_user']
            self.assertEquals(returned_user['username'],self.admin_pss_user.username)            
            self.assertEquals(returned_user['admin_roles'][0]['name'],'pss_admin')
            
    def test_login_fails_with_bad_login(self):
        with self.pss_admin_app.test_client() as c:                        
            rv = c.post('/auth/pss_user/login',
                        data=json.dumps({'username':'test_pss_admin_user2','password':'passwordp'}))
            self.assertHttpCodeEquals(rv,401)
            self.assertFalse(current_user.is_authenticated(),                              
                             "Was expecting user to not be logged in, but user was logged in")

    def test_login_fails_with_bad_password(self):
        with self.pss_admin_app.test_client() as c:                        
            rv = c.post('/auth/pss_user/login',
                        data=json.dumps({'username':self.admin_pss_user.username,'password':'passwordp'}))
            self.assertHttpCodeEquals(rv,401)
            self.assertFalse(current_user.is_authenticated(),                              
                             "Was expecting user to not be logged in, but user was logged in")
    
    def test_login_fails_with_pss_user_with_incorrect_role(self):
        user_pw='password455'
        username='test_pss_user_no_roles%s'% self.create_uniq_id()                
        role_name=roles_constants.TEST
        self.create_user_for_test(self.pss_admin_app,
                                  username,                                  
                                  password=user_pw,
                                  role_name=role_name)

        with self.pss_admin_app.test_client() as c:                        
            rv = c.post('/auth/pss_user/login',
                        data=json.dumps({'username':username,'password':user_pw}))
            self.assertHttpCodeEquals(rv,401)            
            self.assertEquals(rv.data,'{"message": "User can not access this"}')
            self.assertFalse(current_user.is_authenticated(),                              
                             "Was expecting user to not be logged in, but user was logged in")
            
    
    def test_login_fails_with_missing_fields_in_post(self):
        with self.pss_admin_app.test_client() as c:                        
            rv = c.post('/auth/pss_user/login')
            self.assertHttpCodeEquals(rv,400)
            self.assertFalse(current_user.is_authenticated(),                              
                            "Was expecting user to not be logged in, but user was logged in")
            self.assertFalse(hasattr(current_user, 'username'),                              
                            "Was expecting current_user to have not have a username attr, but it did")
    
    def test_login_fails_when_logging_in_as_event_user(self):        
        pass
    
