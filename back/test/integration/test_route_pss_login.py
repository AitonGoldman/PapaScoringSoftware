import unittest
import os
from mock import MagicMock
import pss_integration_test_base
import json
from flask_login import current_user

#FIXME : change name of class/file
class RoutePssLogin(pss_integration_test_base.PssIntegrationTestBase):
    def setUp(self):
        super(RoutePssLogin,self).setUp()        
        self.bootstrap_pss_users(self.pss_admin_app)
        
    def test_login_good_user_good_password(self):
        with self.pss_admin_app.test_client() as c:                        
            rv = c.post('/auth/pss_user/login',
                        data=json.dumps({'username':'test_pss_admin_user','password':'password'}))
            self.assertHttpCodeEquals(rv,200)            
            self.assertTrue(hasattr(current_user, 'username'),                              
                            "Was expecting current_user to have a username attr, but it did not")
            self.assertEquals(current_user.username,
                              'test_pss_admin_user',
                              "expected user to be test_pss_admin_user, but got %s" % (current_user.username))
            returned_user = json.loads(rv.data)['pss_user']
            self.assertEquals(returned_user['username'],'test_pss_admin_user')
            self.assertEquals(returned_user['roles'][0]['name'],'pss_admin')
            
    def test_login_bad_login(self):
        with self.pss_admin_app.test_client() as c:                        
            rv = c.post('/auth/pss_user/login',
                        data=json.dumps({'username':'test_pss_admin_user2','password':'passwordp'}))
            self.assertHttpCodeEquals(rv,401)
            self.assertFalse(hasattr(current_user, 'username'),                              
                            "Was expecting current_user to have not have a username attr, but it did")
    
    def test_login_missing_fields_in_post(self):
        with self.pss_admin_app.test_client() as c:                        
            rv = c.post('/auth/pss_user/login')
            self.assertHttpCodeEquals(rv,400)
            self.assertFalse(hasattr(current_user, 'username'),                              
                            "Was expecting current_user to have not have a username attr, but it did")

    def test_login_fails_when_logging_in_as_event_user(self):
        pass
    
