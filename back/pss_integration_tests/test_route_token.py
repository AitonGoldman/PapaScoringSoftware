import unittest
import os
from mock import MagicMock
from pss_integration_tests import pss_integration_test_base
import json

class RouteTokenTest(pss_integration_test_base.PssIntegrationTestBase):
    def setUp(self):
        super(RouteTokenTest,self).setUp()        
        post_dict = {"players":[{"first_name":"poop_first"+self.create_uniq_id(),"last_name":"poop_last", "ifpa_ranking":123}]} 
        self.admin_login_dict = {'username':self.admin_pss_username,'password':'password'}        
        self.event_id,self.results = self.login_and_create_event_and_create_event_player(self.admin_login_dict, post_dict)                 
        
        
    def test_token(self):        
        test_tournament_name="test_tournament"+self.create_uniq_id()
        post_dict = {"tournament":{"tournament_name":test_tournament_name}}        
        tournaments_dict = self.login_and_create_tournament(self.admin_login_dict,post_dict,self.event_id)        
        tournament_id=tournaments_dict['data'][0]['tournament_id']
        player_id=self.results['data'][0]['player_id']
        post_dict={"player_id":player_id,
                   "tournament_token_counts":[{"token_count":1,"tournament_id":tournament_id}],
                   "meta_tournament_token_counts":[]}

        with self.test_app.test_client() as c:
            login_endpoint='/auth/pss_user/login'
            rv = c.post(login_endpoint,
                        data=json.dumps(self.admin_login_dict))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.put('/%s/token' % (self.event_id),
                        data=json.dumps(post_dict))
            

        #print tournaments_dict['data'][0]['tournament_id']        
