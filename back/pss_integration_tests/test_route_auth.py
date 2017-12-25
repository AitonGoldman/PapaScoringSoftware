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
                        data=json.dumps({'username':self.admin_pss_username,'password':'password'}))
            self.assertHttpCodeEquals(rv,200)

    def test_event_user_login(self):
        #FIXME: need to generate event_users first/last name before each time you try and create an event user
        post_dict = {"event_role_ids":[self.td_event_role_id],"event_users":[{"first_name":"poop_first"+self.create_uniq_id(),"last_name":"poop_last","password":"password"}]}
        login_dict = {'username':self.admin_pss_username,'password':'password'}
        event_id,results = self.login_and_create_event_and_create_event_user(login_dict, post_dict)
        login_dict = {'username':results['data'][0]['username'],'password':'password'}        
        with self.test_app.test_client() as c:
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps(login_dict))
            self.assertHttpCodeEquals(rv,200)
            rv = c.post('/%s/event_user' % event_id,
                        data=json.dumps(post_dict))
            self.assertHttpCodeEquals(rv,200)

    def test_event_user_login_on_event_creator_endpoint_fails(self):
        post_dict = {"event_role_ids":[self.td_event_role_id],"event_users":[{"first_name":"poop_first"+self.create_uniq_id(),"last_name":"poop_last","password":"password"}]}
        login_dict = {'username':self.admin_pss_username,'password':'password'}
        event_id,results = self.login_and_create_event_and_create_event_user(login_dict, post_dict)
        login_dict = {'username':results['data'][0]['username'],'password':'password'}        
        with self.test_app.test_client() as c:
            rv = c.post('/auth/pss_user/login',
                        data=json.dumps(login_dict))
            self.assertHttpCodeEquals(rv,401,"User is not an event creator")


    def test_player_login(self):
        post_dict = {"event_role_ids":[self.td_event_role_id],"event_users":[{"first_name":"poop_first"+self.create_uniq_id(),"last_name":"poop_last","password":"password"}]}
        login_dict = {'username':self.admin_pss_username,'password':'password'}
        event_id,results = self.login_and_create_event_and_create_event_user(login_dict, post_dict) 
        post_dict = {"players":[{"first_name":"poop_first_2"+self.create_uniq_id(),"last_name":"poop_last", "ifpa_ranking":123}]}        
        results = self.login_and_create_event_player(login_dict, post_dict, event_id)                                                 
        pin = results['data'][0]['pin']        
        player_id_for_event = results['data'][0]['event_info']['player_id_for_event']
        login_dict = {'player_id_for_event':player_id_for_event,'player_pin':pin}
        with self.test_app.test_client() as c:
            rv = c.post('/auth/player/login/%s'%event_id,
                        data=json.dumps(login_dict))
            self.assertHttpCodeEquals(rv,200)
        