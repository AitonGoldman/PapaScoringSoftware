import unittest
import os
from mock import MagicMock
import pss_integration_test_existing_event

import json
from flask_login import current_user
from lib import roles_constants

#FIXME : change name of class/file

class RoutePssPlayerLogin(pss_integration_test_existing_event.PssIntegrationTestExistingEvent):
    def setUp(self):
        super(RoutePssPlayerLogin,self).setUp()        
            
    def test_player_login(self):
                
        with self.event_app.test_client() as c:                        
            tables = self.event_app.tables
            player_id,player_number,player_pin = self.get_player_id_and_number_and_pin(self.standard_player_first_name,
                                                                                       self.standard_player_last_name,
                                                                                       self.event_app)
            rv = c.post('/auth/player/login',
                        data=json.dumps({'event_player_number':player_number,'event_player_pin':player_pin}))
            self.assertHttpCodeEquals(rv,200)            
            self.assertTrue(hasattr(current_user, 'player_id'),                              
                            "Was expecting current_user to have a player_id attr, but it did not")
            self.assertEquals(current_user.player_id,
                              player_number,
                              "expected player_id to be 1, but got %s" % (current_user.player_id))
            self.assertTrue(current_user.is_authenticated(),                              
                             "Was expecting player to be logged in, but player was not logged in")            
            returned_player = json.loads(rv.data)['player']
            self.assertEquals(returned_player['player_id'],1)            
            self.assertTrue('event_player_pin' not in returned_player['event_player'])
            self.assertEquals(returned_player['event_player']['ifpa_ranking'],9999)
            self.assertEquals(len(returned_player['player_roles']),1)

    def test_player_login_with_bad_info_fails(self):
                
        with self.event_app.test_client() as c:                        
            tables = self.event_app.tables
            existing_player = tables.Players.query.filter(tables.Players.event_player.has(tables.EventPlayers.event_player_id==1)).first()
            rv = c.post('/auth/player/login',
                        data=json.dumps({'event_player_number':9999,'event_player_pin':existing_player.event_player.event_player_pin}))
            self.assertHttpCodeEquals(rv,401)            
            self.assertFalse(current_user.is_authenticated())

            rv = c.post('/auth/player/login',
                        data=json.dumps({'event_player_number':1,'event_player_pin':0}))
            self.assertHttpCodeEquals(rv,401)            
            self.assertFalse(current_user.is_authenticated())

    def test_player_login_to_wrong_site_fails(self):
                
        new_event_name = 'testEvent%s' % self.create_uniq_id()
        self.create_event_for_test(new_event_name)
        event_for_test = self.get_event_app_in_db(new_event_name)

        existing_player_id,existing_player_number,existing_player_pin = self.get_player_id_and_number_and_pin(self.standard_player_first_name,
                                                                                                              self.standard_player_last_name,
                                                                                                              self.event_app)
        with event_for_test.test_client() as c:                        
            rv = c.post('/auth/player/login',
                        data=json.dumps({'event_player_number':existing_player_number,'event_player_pin':existing_player_pin}))
            self.assertHttpCodeEquals(rv,401)            
            self.assertFalse(current_user.is_authenticated())

            
            
