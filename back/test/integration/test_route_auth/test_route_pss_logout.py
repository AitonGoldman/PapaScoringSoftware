import unittest
import os
from mock import MagicMock
from test.integration import pss_integration_test_base
import json
from flask_login import current_user

#FIXME : change name of class/file
class RoutePssLogout(pss_integration_test_base.PssIntegrationTestBase):
    def setUp(self):
        super(RoutePssLogout,self).setUp()        
        
    def test_logout_after_login(self):
        with self.pss_admin_app.test_client() as c:                        
            rv = c.post('/auth/pss_user/login',
                        data=json.dumps({'username':self.admin_pss_user.username,'password':self.admin_pss_user_password}))
            rv = c.get('/auth/pss_user/logout')           
            self.assertHttpCodeEquals(rv,200)            
            self.assertFalse(current_user.is_authenticated(),                            
                            "expected current_user to be anonymous, but it was not")

    def test_logout_with_no_one_logged_in(self):
        with self.pss_admin_app.test_client() as c:                        
            rv = c.get('/auth/pss_user/logout')           
            self.assertHttpCodeEquals(rv,200)            
            self.assertFalse(current_user.is_authenticated(),                            
                            "expected current_user to be anonymous, but it was not")
            
