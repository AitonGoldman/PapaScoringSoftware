import unittest
import os
from mock import MagicMock
from pss_integration_tests import pss_integration_test_base
import json

class RouteQueueTest(pss_integration_test_base.PssIntegrationTestBase):
    def setUp(self):
        super(RouteQueueTest,self).setUp()        
        post_dict = {"event_role_ids":[self.td_event_role_id],"event_users":[{"first_name":"poop_firsta"+self.create_uniq_id(),"last_name":"poop_lasta","password":"password"}]}
        self.admin_login_dict = {'username':self.admin_pss_username,'password':'password'}        
        self.event_id,self.results = self.login_and_create_event_and_create_event_user(self.admin_login_dict, post_dict)
        self.test_tournament_name="test_tournament"+self.create_uniq_id()
        self.tournament_post_dict = {"tournament":{"tournament_name":self.test_tournament_name}}        
        self.tournaments_dict = self.login_and_create_tournament(self.admin_login_dict,
                                                                 self.tournament_post_dict,
                                                                 self.event_id)
        self.post_dict = {"tournament_id":self.tournaments_dict['data'][0]['tournament_id'],"machine_id":1}
        
    def test_queue_create(self):        
        tournament_machine_dict = self.login_and_create_tournament_machine(self.admin_login_dict,
                                                                           self.post_dict,
                                                                           self.event_id)        
        self.assertTrue(tournament_machine_dict['data']['tournament_machine_name'] is not None)
        queues_in_db = self.test_app.table_proxy.Queues.query.filter_by(tournament_machine_id=tournament_machine_dict['data']['tournament_machine_id']).all()
        self.assertEquals(len(queues_in_db),15)

    def test_add_player_to_queue(self):
        post_dict = {"players":[{"first_name":"poop_first_2"+self.create_uniq_id(),"last_name":"poop_last", "ifpa_ranking":123}]}        
        results = self.login_and_create_event_player(self.admin_login_dict, post_dict, self.event_id)                                                         
        player_id = results['data'][0]['player_id']
        post_dict = {"players":[{"first_name":"poop_first_2"+self.create_uniq_id(),"last_name":"poop_last", "ifpa_ranking":123}]}        
        results = self.login_and_create_event_player(self.admin_login_dict, post_dict, self.event_id)                                                         
        player2_id = results['data'][0]['player_id']        
        post_dict = {"players":[{"first_name":"poop_first_2"+self.create_uniq_id(),"last_name":"poop_last", "ifpa_ranking":123}]}        
        results = self.login_and_create_event_player(self.admin_login_dict, post_dict, self.event_id)                                                         
        player3_id = results['data'][0]['player_id']        
        
        tournament_machine_dict = self.login_and_create_tournament_machine(self.admin_login_dict,
                                                                           self.post_dict,
                                                                           self.event_id)
        tournament_machine_id=tournament_machine_dict['data']['tournament_machine_id']
        tournament_id=self.tournaments_dict['data'][0]['tournament_id']        
        post_dict={"player_id":player_id,
                   "tournament_token_counts":[{"token_count":1,"tournament_id":tournament_id}],
                   "meta_tournament_token_counts":[]}        
        self.login_and_purchase_tickets(self.admin_login_dict,post_dict,self.event_id)
        post_dict={"player_id":player2_id,
                   "tournament_token_counts":[{"token_count":1,"tournament_id":tournament_id}],
                   "meta_tournament_token_counts":[]}        
        self.login_and_purchase_tickets(self.admin_login_dict,post_dict,self.event_id)
        post_dict={"player_id":player3_id,
                   "tournament_token_counts":[{"token_count":1,"tournament_id":tournament_id}],
                   "meta_tournament_token_counts":[]}        
        self.login_and_purchase_tickets(self.admin_login_dict,post_dict,self.event_id)
        
        tournament_machine_in_db = self.test_app.table_proxy.TournamentMachines.query.filter_by(tournament_machine_id=tournament_machine_id).first()
        tournament_machine_in_db.player_id=player_id
        self.test_app.table_proxy.db_handle.session.commit()

        post_dict={"player_id":player2_id,"tournament_machine_id":tournament_machine_id}
        self.login_and_add_player_to_queue(self.admin_login_dict,post_dict,self.event_id)

        post_dict={"player_id":player3_id,"tournament_machine_id":tournament_machine_id}
        self.login_and_add_player_to_queue(self.admin_login_dict,post_dict,self.event_id)

        post_dict={"player_id":player2_id,"tournament_machine_id":tournament_machine_id}
        self.login_and_add_player_to_queue(self.admin_login_dict,post_dict,self.event_id)
        
        post_dict={"action":"bump","player_id":player3_id,"tournament_machine_id":tournament_machine_id}
        self.login_and_bump_player_down_queue(self.admin_login_dict,post_dict,self.event_id)

        post_dict={"action":"bump","player_id":player2_id,"tournament_machine_id":tournament_machine_id}
        self.login_and_bump_player_down_queue(self.admin_login_dict,post_dict,self.event_id)
        
        post_dict={"action":"bump","player_id":player3_id,"tournament_machine_id":tournament_machine_id}
        self.login_and_bump_player_down_queue(self.admin_login_dict,post_dict,self.event_id)
        
