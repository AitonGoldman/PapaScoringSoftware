import unittest
import os
from mock import MagicMock
from pss_integration_tests import pss_integration_test_base
import json

class RouteAuthTest(pss_integration_test_base.PssIntegrationTestBase):
    def setUp(self):
        super(RouteAuthTest,self).setUp()
        
    def test_event_creator_login(self):        
        with self.test_app.test_client() as c:
            rv = c.post('/auth/pss_user/login',
                        data=json.dumps({'username':self.admin_pss_user.username,'password':'password'}))
            self.assertHttpCodeEquals(rv,200)

    def test_normal_login_fails(self):        
        with self.test_app.test_client() as c:
            rv = c.post('/auth/pss_user/login',
                        data=json.dumps({'username':self.normal_pss_user.username,'password':'password'}))
            self.assertHttpCodeEquals(rv,401,"Bad username")
            
