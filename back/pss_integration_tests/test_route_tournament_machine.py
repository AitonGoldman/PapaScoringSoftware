import unittest
import os
from mock import MagicMock
from pss_integration_tests import pss_integration_test_base
import json

class RouteTournamentMachineTest(pss_integration_test_base.PssIntegrationTestBase):
    def setUp(self):
        super(RouteTournamentMachineTest,self).setUp()        
        post_dict = {"event_role_ids":[self.td_event_role_id],"event_users":[{"first_name":"poop_firsta"+self.create_uniq_id(),"last_name":"poop_lasta","password":"password"}]}
        self.admin_login_dict = {'username':self.admin_pss_username,'password':'password'}        
        self.event_id,self.results = self.login_and_create_event_and_create_event_user(self.admin_login_dict, post_dict)
        self.test_tournament_name="test_tournament"+self.create_uniq_id()
        self.tournament_post_dict = {"tournament":{"tournament_name":self.test_tournament_name}}        
        self.tournaments_dict = self.login_and_create_tournament(self.admin_login_dict,
                                                                 self.tournament_post_dict,
                                                                 self.event_id)
        self.post_dict = {"tournament_id":self.tournaments_dict['data'][0]['tournament_id'],"machine_id":1}
        
    def test_tournament_machine_create(self):        
        tournament_machine_dict = self.login_and_create_tournament_machine(self.admin_login_dict,
                                                                           self.post_dict,
                                                                           self.event_id)        
        self.assertTrue(tournament_machine_dict['data']['tournament_machine_name'] is not None)

    def test_tournament_machine_remove_and_add_again(self):        
        tournament_machine_dict = self.login_and_create_tournament_machine(self.admin_login_dict,
                                                                           self.post_dict,
                                                                           self.event_id)
        tournament_machine_dict['data']['removed']=True
        tournament_machine_id=tournament_machine_dict['data']['tournament_machine_id']
        edited_tournament_machine_dict = self.login_and_edit_tournament_machine(self.admin_login_dict,
                                                                                tournament_machine_dict['data'],
                                                                                self.event_id)
        self.assertEquals(edited_tournament_machine_dict['data']['removed'],True)
        self.assertEquals(edited_tournament_machine_dict['data']['active'],False)
        
        tournament_machine_dict = self.login_and_create_tournament_machine(self.admin_login_dict,
                                                                           self.post_dict,
                                                                           self.event_id)        
        self.assertEquals(tournament_machine_id,tournament_machine_dict['data']['tournament_machine_id'])
        self.assertEquals(tournament_machine_dict['data']['removed'],False)
        self.assertEquals(tournament_machine_dict['data']['active'],True)
        
        
