import unittest
import os
from mock import MagicMock
import pss_integration_test_existing_event

import json
from flask_login import current_user
from lib import roles_constants

#FIXME : change name of class/file

class RoutePssEventLogin(pss_integration_test_existing_event.PssIntegrationTestExistingEvent):
    def setUp(self):
        super(RoutePssEventLogin,self).setUp()        


    #FIXME : need an actual event user login happy path test
    
    def test_login_fails_when_logging_into_2_events(self):
        
        with self.event_app.test_client() as c:                                    
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.standard_scorekeeper_username,
                                         'password':self.generic_password}))
            self.assertHttpCodeEquals(rv,200)                                    
            cookie = rv.headers['Set-Cookie'].split("=")[1]
            cookie = cookie.split(";")[0]                        

        new_event_name = 'testEvent%s' % self.create_uniq_id()
        self.create_event_for_test(new_event_name)
        event_for_test = self.get_event_app_in_db(new_event_name)
        
        with event_for_test.test_client() as c:                                    
            c.set_cookie('localhost','session', cookie)
            rv = c.get('/auth/pss_event_user/current_user')
            self.assertHttpCodeEquals(rv,200)            
            self.assertEquals(json.loads(rv.data)['current_user'],None)
            
    
    def test_login_fails_when_logging_into_1_event_and_admin_event(self):
        
        with self.event_app.test_client() as c:                        

            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.standard_scorekeeper_username,
                                         'password':self.generic_password}))
            self.assertHttpCodeEquals(rv,200)
            cookie = rv.headers['Set-Cookie'].split("=")[1]
            cookie = cookie.split(";")[0]                        

        with self.pss_admin_app.test_client() as c:                             
            c.set_cookie('localhost','session', cookie)
            rv = c.get('/auth/pss_user/current_user')
            self.assertHttpCodeEquals(rv,200)            
            self.assertEquals(json.loads(rv.data)['current_user'],None)

            
