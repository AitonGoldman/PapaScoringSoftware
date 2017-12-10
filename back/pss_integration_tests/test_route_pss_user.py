import unittest
import os
from mock import MagicMock
from pss_integration_tests import pss_integration_test_base
import json

class RoutePssUserTest(pss_integration_test_base.PssIntegrationTestBase):
    def setUp(self):
        super(RoutePssUserTest,self).setUp()        

    def test_event_user_create(self):        
        self.test_app.table_proxy.create_user(self.admin_pss_username+"2",
                                              'test_first_two',
                                              'test_last_two',
                                              'password',
                                              event_creator=True,
                                              commit=True)

        with self.test_app.test_client() as c:

            rv = c.post('/auth/pss_user/login',
                        data=json.dumps({'username':self.admin_pss_username,'password':'password'}))
            self.assertHttpCodeEquals(rv,200)
            event_name = 'test_event_'+self.create_uniq_id()
            rv = c.post('/event',
                        data=json.dumps({'name':event_name}))
            self.assertHttpCodeEquals(rv,200)
            results = json.loads(rv.data)
            event_id = results['data']['event_id']
            #print self.td_event_role_id
            rv = c.post('/%s/event_user' % event_id,
                        data=json.dumps({"event_role_ids":["1"],"event_users":[{"first_name":"poop_first","last_name":"poop_last"}]}))
            self.assertHttpCodeEquals(rv,200)

        with self.test_app.test_client() as c:
            rv = c.post('/auth/pss_user/login',
                        data=json.dumps({'username':self.admin_pss_username+"2",'password':'password'}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.post('/%s/event_user' % event_id,
                        data=json.dumps({"event_role_ids":["1"],"event_users":[{"first_name":"poop_first","last_name":"poop_last"}]}))
            self.assertHttpCodeEquals(rv,200)
            
