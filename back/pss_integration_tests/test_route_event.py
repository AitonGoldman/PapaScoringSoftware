import unittest
import os
from mock import MagicMock
from pss_integration_tests import pss_integration_test_base
import json

class RouteAuthTest(pss_integration_test_base.PssIntegrationTestBase):
    def setUp(self):
        super(RouteAuthTest,self).setUp()

    #FIXME : add tests for event creation with user
    def test_event_create(self):        
        with self.test_app.test_client() as c:
            rv = c.post('/auth/pss_user/login',
                        data=json.dumps({'username':self.admin_pss_username,'password':'password'}))
            self.assertHttpCodeEquals(rv,200)
            event_name = 'test_event_'+self.create_uniq_id()
            rv = c.post('/event',
                        data=json.dumps({'name':event_name}))
            self.assertHttpCodeEquals(rv,200)
            results = json.loads(rv.data)
            self.assertEquals(results['data']['name'],event_name)            

    def test_event_create_fails_with_anonymous(self):        
        with self.test_app.test_client() as c:
            rv = c.post('/event',
                        data=json.dumps({'name':'test_event'}))
            self.assertHttpCodeEquals(rv,401,'You are not authorized to create an event')                        


    def test_event_edit(self):        
        with self.test_app.test_client() as c:
            rv = c.post('/auth/pss_user/login',
                        data=json.dumps({'username':self.admin_pss_username,'password':'password'}))
            self.assertHttpCodeEquals(rv,200)
            rv = c.post('/event',
                        data=json.dumps({'name':'test_event'}))
            self.assertHttpCodeEquals(rv,200)
            results = json.loads(rv.data)                        
            event_id = results['data']['event_id']
            rv = c.put('/event',
                        data=json.dumps({'name':'test_event_new','event_id':event_id}))
            self.assertHttpCodeEquals(rv,200)
            results = json.loads(rv.data)
            self.assertEquals(results['data']['name'],'test_event_new')
            
    def test_event_edit_fails_with_anonymous(self):        
        with self.test_app.test_client() as c:            
            rv = c.put('/event',
                        data=json.dumps({'name':'test_event_new','event_id':1}))
            self.assertHttpCodeEquals(rv,401,'You are not authorized to edit this event')
    def test_event_get_all_events(self):
        pass
    def test_event_get_all_events_and_tournaments(self):
        pass
            
