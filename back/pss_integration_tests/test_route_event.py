import unittest
import os
from mock import MagicMock
from pss_integration_tests import pss_integration_test_base
import json

class RouteAuthTest(pss_integration_test_base.PssIntegrationTestBase):
    def setUp(self):
        super(RouteAuthTest,self).setUp()
        
    def test_event_create(self):        
        with self.test_app.test_client() as c:
            rv = c.post('/auth/pss_user/login',
                        data=json.dumps({'username':self.admin_pss_user.username,'password':'password'}))
            self.assertHttpCodeEquals(rv,200)
            rv = c.post('/event',
                        data=json.dumps({'name':'test_event'}))
            self.assertHttpCodeEquals(rv,200)
            results = json.loads(rv.data)
            self.assertEquals(results['data']['name'],'test_event')

    def test_event_create_fails_with_non_event_creator(self):        
        with self.test_app.test_client() as c:
            rv = c.post('/event',
                        data=json.dumps({'name':'test_event'}))
            self.assertHttpCodeEquals(rv,401,'You are not authorized to create an event')                        
            
