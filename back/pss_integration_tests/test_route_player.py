import unittest
import os
from mock import MagicMock
from pss_integration_tests import pss_integration_test_base
import json

class RoutePlayerTest(pss_integration_test_base.PssIntegrationTestBase):
    def setUp(self):
        super(RoutePlayerTest,self).setUp()        
        player_create_player_post_dict = {"players":[{"first_name":"poop_first"+self.create_uniq_id(),"last_name":"poop_last", "ifpa_ranking":123}]}
        self.admin_login_dict = {'username':self.admin_pss_username,'password':'password'}
        self.event_id,self.player_create_results = self.login_and_create_event_and_create_event_player(self.admin_login_dict, player_create_player_post_dict)                
        player_create_player_post_dict = {"players":[{"first_name":"poop_first_2"+self.create_uniq_id(),"last_name":"poop_last", "ifpa_ranking":123}]}        
        self.event_id_2, self.player_create_results_2 = self.login_and_create_event_and_create_event_player(self.admin_login_dict, player_create_player_post_dict)
        
    def test_player_create_with_event_creator(self):                        
        self.assertTrue(len(self.player_create_results['data'])==1)
        self.assertTrue(self.player_create_results['data'][0]['player_id'] is not None)
        new_player_id=int(self.player_create_results['data'][0]['player_id'])
        player_in_db = self.test_app.table_proxy.Players.query.filter_by(player_id=new_player_id).first()        
        self.assertTrue(player_in_db is not None)
        player_event_info_in_db = self.test_app.table_proxy.EventPlayersInfo.query.filter_by(player_id=new_player_id,event_id=self.event_id).all()
        self.assertEquals(len(player_event_info_in_db),1)
        self.assertEquals(player_event_info_in_db[0].ifpa_ranking,123)

    def test_add_existing_player_to_event_with_event_creator(self):                        
        new_player_id=int(self.player_create_results_2['data'][0]['player_id'])        
        add_player_to_existing_event_post_dict = {"players":[{"player_id":new_player_id,"ifpa_ranking":123}]}
        num_players_in_db = len(self.test_app.table_proxy.Players.query.filter_by(player_id=new_player_id).all())
        create_new_player_results = self.login_and_create_event_player(self.admin_login_dict, add_player_to_existing_event_post_dict, self.event_id)                
        
        new_num_players_in_db = len(self.test_app.table_proxy.Players.query.filter_by(player_id=new_player_id).all())
        self.assertEquals(num_players_in_db,new_num_players_in_db)        
        player_event_info_in_db = self.test_app.table_proxy.EventPlayersInfo.query.filter_by(player_id=new_player_id).all()
        self.assertEquals(len(player_event_info_in_db),2)
        pin = create_new_player_results['data'][0]['pin']
        player_id_for_event = create_new_player_results['data'][0]['event_info']['player_id_for_event']
        player_login_dict = {'player_id_for_event':player_id_for_event,'player_pin':pin}
        with self.test_app.test_client() as c:
            rv = c.post('/auth/player/login/%s'%self.event_id,
                        data=json.dumps(player_login_dict))
            self.assertHttpCodeEquals(rv,200)
        

