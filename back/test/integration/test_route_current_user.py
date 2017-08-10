import unittest
import os
from mock import MagicMock
import pss_integration_test_base
import json
from flask_login import current_user

#FIXME : change name of class/file
class RoutePssCurrentUser(pss_integration_test_base.PssIntegrationTestBase):
    def setUp(self):
        super(RoutePssCurrentUser,self).setUp()        
        self.bootstrap_pss_users(self.pss_admin_app)
        
    def test_get_current_user_after_login(self):
        with self.pss_admin_app.test_client() as c:                        
            rv = c.post('/auth/pss_user/login',
                        data=json.dumps({'username':'test_pss_admin_user','password':'password'}))
            self.assertHttpCodeEquals(rv,200)
            rv = c.get('/auth/pss_user/current_user')
            self.assertHttpCodeEquals(rv,200)
            pss_user_info = json.loads(rv.data)
            self.assertTrue('current_user' in pss_user_info)            
            self.assertFalse('password_crypt' in pss_user_info['current_user'])
            self.assertTrue('username' in pss_user_info['current_user'])
            self.assertEquals('test_pss_admin_user',pss_user_info['current_user']['username'])
            self.assertTrue('roles' in pss_user_info['current_user'])
            self.assertEquals(1,len(pss_user_info['current_user']['roles']))
            #FIXME : need event roles check
