import unittest
import os
from mock import MagicMock
from pss_integration_tests import pss_integration_test_base
import json
import random

class RouteResultsTest(pss_integration_test_base.PssIntegrationTestBase):
    def create_tournament(self):
        test_tournament_name='test_tournament_'+self.create_uniq_id()
        tournament_post_dict = {"tournament":{"tournament_name":test_tournament_name}}        
        tournaments_dict = self.login_and_create_tournament(self.admin_login_dict,
                                                                 tournament_post_dict,
                                                                 self.event_id)
        return tournaments_dict['data'][0]['tournament_id']
        
    def create_tournament_machine(self,tournament_id,machine_id):        
        post_dict = {"tournament_id":tournament_id,"machine_id":machine_id}
        tournament_machine_dict = self.login_and_create_tournament_machine(self.admin_login_dict,
                                                                                post_dict,
                                                                                self.event_id)
        return tournament_machine_dict['data']['tournament_machine_id']
    def create_player(self):
        post_dict = {"players":[{"first_name":"poop_first_2"+self.create_uniq_id(),"last_name":"poop_last", "ifpa_ranking":123}]}        
        results = self.login_and_create_event_player(self.admin_login_dict, post_dict, self.event_id)                                                         
        return results['data'][0]['player_id']

    def buy_tickets(self,player_id,tournament_id):
        post_dict={"player_id":player_id,
                   "tournament_token_counts":[{"token_count":10,"tournament_id":tournament_id}],
                   "meta_tournament_token_counts":[]}        
        self.login_and_purchase_tickets(self.admin_login_dict,post_dict,self.event_id)

    def start_on_machine_and_record_score(self,player_id,tournament_machine_id,score=None):
        post_dict={"player_id":player_id,"tournament_machine_id":tournament_machine_id,"action":"start"}
        self.login_and_start_player_on_machine(self.admin_login_dict,post_dict,self.event_id)
        if score is None:
            score = random.randrange(1,999999)
        post_dict={"player_id":player_id,"tournament_machine_id":tournament_machine_id,"action":"record_score","score":"%s"%score}
        self.login_and_record_score(self.admin_login_dict,post_dict,self.event_id)

    def setUp(self):
        super(RouteResultsTest,self).setUp()        
        post_dict = {"event_role_ids":[self.td_event_role_id],"event_users":[{"first_name":"poop_firsta"+self.create_uniq_id(),"last_name":"poop_lasta","password":"password"}]}
        self.admin_login_dict = {'username':self.admin_pss_username,'password':'password'}        
        self.event_id,self.results = self.login_and_create_event_and_create_event_user(self.admin_login_dict, post_dict)
        
        self.tournament_machines=[]
        self.tournaments=[]
        for x in range(0,20):
            self.tournaments.append(self.create_tournament())        
        self.players=[]
        for y in self.tournaments:            
            for x in range(0,20):
                self.tournament_machines.append(self.create_tournament_machine(y,x+1))
        for x in range(0,100):            
            self.players.append(self.create_player())
                
    def test_get_tournament_machine_results(self):
        pass
        # for y in range(0,15):
        #     for x in range(0,100):
        #         self.buy_tickets(self.players[x],self.tournament_id)
        #         for z in range(0,10):                        
        #             self.start_on_machine_and_record_score(self.players[x],self.tournament_machines[y])
                
        #self.get_machine_results(self.event_id,self.tournament_machine_id)
        
