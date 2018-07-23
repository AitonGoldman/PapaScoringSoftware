import unittest
import os
from mock import MagicMock
from pss_integration_tests import pss_integration_test_base
import json

class RouteEntryTest(pss_integration_test_base.PssIntegrationTestBase):
    def setUp(self):
        super(RouteEntryTest,self).setUp()        
        post_dict = {"event_role_ids":[self.td_event_role_id],"event_users":[{"first_name":"poop_firsta"+self.create_uniq_id(),"last_name":"poop_lasta","password":"password"}]}
        self.admin_login_dict = {'username':self.admin_pss_username,'password':'password'}        
        self.event_id,self.results = self.login_and_create_event_and_create_event_user(self.admin_login_dict, post_dict)
        self.test_tournament_name="test_tournament"+self.create_uniq_id()
        self.tournament_post_dict = {"tournament":{"tournament_name":self.test_tournament_name}}        
        self.tournaments_dict = self.login_and_create_tournament(self.admin_login_dict,
                                                                 self.tournament_post_dict,
                                                                 self.event_id)
        tournament_id=self.tournaments_dict['data'][0]['tournament_id']                
        self.post_dict = {"tournament_id":self.tournaments_dict['data'][0]['tournament_id'],"machine_id":1}
        self.tournament_machine_dict = self.login_and_create_tournament_machine(self.admin_login_dict,
                                                                                self.post_dict,
                                                                                self.event_id)
        self.tournament_machine_id=self.tournament_machine_dict['data']['tournament_machine_id']
        post_dict = {"players":[{"first_name":"poop_first_2"+self.create_uniq_id(),"last_name":"poop_last", "ifpa_ranking":123}]}        
        results = self.login_and_create_event_player(self.admin_login_dict, post_dict, self.event_id)                                                         
        self.player_id=results['data'][0]['player_id']
        post_dict = {"players":[{"first_name":"poop_first_2"+self.create_uniq_id(),"last_name":"poop_last", "ifpa_ranking":123}]}        
        results = self.login_and_create_event_player(self.admin_login_dict, post_dict, self.event_id)                                                         
        self.player_id_2=results['data'][0]['player_id']
        
        post_dict={"player_id":self.player_id,
                   "tournament_token_counts":[{"token_count":1,"tournament_id":tournament_id}],
                   "meta_tournament_token_counts":[]}        
        self.login_and_purchase_tickets(self.admin_login_dict,post_dict,self.event_id)
        post_dict={"player_id":self.player_id_2,
                   "tournament_token_counts":[{"token_count":1,"tournament_id":tournament_id}],
                   "meta_tournament_token_counts":[]}        
        self.login_and_purchase_tickets(self.admin_login_dict,post_dict,self.event_id)

        
    def test_start_player_on_machine(self):
        post_dict={"player_id":self.player_id,"tournament_machine_id":self.tournament_machine_id,'action':'start'}
        self.login_and_start_player_on_machine(self.admin_login_dict,post_dict,self.event_id)
        tournament_machine = self.test_app.table_proxy.TournamentMachines.query.filter_by(tournament_machine_id=self.tournament_machine_id).first()
        self.assertEquals(tournament_machine.player_id,int(self.player_id))

    def test_start_player_on_machine_from_queue(self):
        post_dict={"player_id":self.player_id,"tournament_machine_id":self.tournament_machine_id,"action":"start"}
        self.login_and_start_player_on_machine(self.admin_login_dict,post_dict,self.event_id)

        post_dict={"player_id":self.player_id_2,"tournament_machine_id":self.tournament_machine_id}
        self.login_and_add_player_to_queue(self.admin_login_dict,post_dict,self.event_id)        

        post_dict={"player_id":self.player_id,"tournament_machine_id":self.tournament_machine_id}
        self.login_and_void_tickets(self.admin_login_dict,post_dict,self.event_id)

        tournament_machine = self.test_app.table_proxy.TournamentMachines.query.filter_by(tournament_machine_id=self.tournament_machine_id).first()
        self.assertEquals(tournament_machine.player_id,None)        
        tokens = self.test_app.table_proxy.Tokens.query.filter_by(player_id=self.player_id).all()                
        self.assertTrue(tokens[0].voided)
        self.assertFalse(tokens[0].used)
        self.assertFalse(tokens[0].deleted)
        
        post_dict={"player_id":self.player_id_2,"tournament_machine_id":self.tournament_machine_id,"action":"start_from_queue"}
        self.login_and_start_player_on_machine(self.admin_login_dict,post_dict,self.event_id)

        tournament_machine = self.test_app.table_proxy.TournamentMachines.query.filter_by(tournament_machine_id=self.tournament_machine_id).first()
        self.assertEquals(tournament_machine.player_id,int(self.player_id_2))
        queues = self.test_app.table_proxy.Queues.query.filter_by(tournament_machine_id=self.tournament_machine_id).order_by(self.test_app.table_proxy.Queues.position).all()
        tokens = self.test_app.table_proxy.Tokens.query.filter_by(player_id=self.player_id_2).all()
        self.assertEquals(queues[0].player_id,None)
        self.assertEquals(len([queue for queue in queues if queue.player_id is not None]),0)
        self.assertFalse(tokens[0].voided)
        self.assertFalse(tokens[0].used)
        self.assertFalse(tokens[0].deleted)

    def test_record_score(self):
        post_dict={"player_id":self.player_id,"tournament_machine_id":self.tournament_machine_id,"action":"start"}
        self.login_and_start_player_on_machine(self.admin_login_dict,post_dict,self.event_id)
        post_dict={"player_id":self.player_id,"tournament_machine_id":self.tournament_machine_id,"action":"record_score","score":"123456"}
        self.login_and_record_score(self.admin_login_dict,post_dict,self.event_id)
        
