import datetime
import unittest
import os
from mock import MagicMock
import pss_integration_test_existing_event
import json
from flask_login import current_user
from lib import roles_constants
from sqlalchemy.orm import joinedload


class RoutePlayer(pss_integration_test_existing_event.PssIntegrationTestExistingEvent):
    def setUp(self):
        super(RoutePlayer,self).setUp()                        
        
    def test_create_player_while_logged_into_event_as_td(self):        
        self.createEventsAndEventUsers()
        new_player_first_name='first_name%s'%self.create_uniq_id()
        with self.event_app.test_client() as c:                        
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.standard_td_username,
                                         'password':self.generic_password}))
            self.assertHttpCodeEquals(rv,200)                        
            rv = c.post('/player',
                        data=json.dumps({'first_name':new_player_first_name,
                                         'last_name':'last_name',
                                         'ifpa_ranking':9999,
                                         'ifpa_id':1}))

            self.assertHttpCodeEquals(rv,200)            
            returned_player = json.loads(rv.data)['new_player']
            self.assertEquals(returned_player['first_name'],new_player_first_name)
            self.assertEquals(returned_player['last_name'],'last_name')
            self.assertEquals(returned_player['ifpa_id'], 1)
            #FIXME : make sure pin number is returned
            
            self.assertEquals(returned_player['event_player']['ifpa_ranking'],9999)
            self.assertEquals(len(returned_player['player_roles']),1)
            self.assertEquals(len(returned_player['events']),1)            
            new_player_in_db = self.event_app.tables.Players.query.filter_by(first_name=new_player_first_name).first()
            self.assertTrue(new_player_in_db is not None)
            self.assertTrue(new_player_in_db.event_player is not None)


    def test_duplicate_create_player_fails_with_duplicate_full_names(self):        
        self.createEventsAndEventUsers()
        new_player_first_name='first_name%s'%self.create_uniq_id()
        with self.event_app.test_client() as c:                        
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.standard_td_username,
                                         'password':self.generic_password}))
            self.assertHttpCodeEquals(rv,200)                        
            rv = c.post('/player',
                        data=json.dumps({'first_name':new_player_first_name,
                                         'last_name':'last_name',
                                         'extra_title':'jr',
                                         'ifpa_ranking':9999}))

            self.assertHttpCodeEquals(rv,200)
            rv = c.post('/player',
                        data=json.dumps({'first_name':new_player_first_name,
                                         'last_name':'last_name',
                                         'extra_title':'jr',
                                         'ifpa_ranking':9999}))
            self.assertHttpCodeEquals(rv,409)

    def test_duplicate_create_player_with_duplicate_full_names_but_different_extra_title(self):        
        self.createEventsAndEventUsers()
        new_player_first_name='first_name%s'%self.create_uniq_id()
        with self.event_app.test_client() as c:                        
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.standard_td_username,
                                         'password':self.generic_password}))
            self.assertHttpCodeEquals(rv,200)                        
            rv = c.post('/player',
                        data=json.dumps({'first_name':new_player_first_name,
                                         'last_name':'last_name',
                                         'extra_title':'jr',
                                         'ifpa_ranking':9999}))

            self.assertHttpCodeEquals(rv,200)
            rv = c.post('/player',
                        data=json.dumps({'first_name':new_player_first_name,
                                         'last_name':'last_name',
                                         'extra_title':'sr',
                                         'ifpa_ranking':9999}))
            self.assertHttpCodeEquals(rv,200)
            
            
    def test_create_player_while_logged_into_event_as_scorekeeper_fails(self):        
        self.createEventsAndEventUsers()
        new_player_first_name='first_name%s'%self.create_uniq_id()
        with self.event_app.test_client() as c:                        
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.standard_scorekeeper_username,
                                         'password':self.generic_password}))
            self.assertHttpCodeEquals(rv,200)                        
            rv = c.post('/player',
                        data=json.dumps({'first_name':new_player_first_name,
                                         'last_name':'last_name',
                                         'ifpa_ranking':9999}))

            self.assertHttpCodeEquals(rv,403)                        

    def test_add_existing_player_to_event_as_tournament_director(self):                
        self.createEventsAndEventUsers()
        new_event_name = 'testEvent%s' % self.create_uniq_id()
        self.create_event_for_test(new_event_name)
        event_for_test = self.get_event_app_in_db(new_event_name)
        player_id,player_num,player_pin = self.get_player_id_and_number_and_pin(self.standard_player_first_name,self.standard_player_last_name,self.event_app)

        new_td_username='new_td%s' % self.create_uniq_id()
        self.create_event_user_for_test(event_for_test,
                                        new_td_username,
                                        password=self.generic_password,
                                        role_name=roles_constants.TOURNAMENT_DIRECTOR)

        with event_for_test.test_client() as c:                        
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':new_td_username,
                                         'password':self.generic_password}))
            self.assertHttpCodeEquals(rv,200)                        
            rv = c.put('/player',
                       data=json.dumps({'player_id':player_id,
                                        'ifpa_ranking':9999}))
            self.assertHttpCodeEquals(rv,200)            
            returned_player = json.loads(rv.data)['existing_player_added_to_event']
            self.assertEquals(returned_player['first_name'],self.standard_player_first_name)
            self.assertEquals(returned_player['last_name'],self.standard_player_last_name)
            self.assertEquals(returned_player['event_player']['ifpa_ranking'],9999)
            self.assertEquals(len(returned_player['player_roles']),1)
            self.assertEquals(len(returned_player['events']),2)            
            modified_player = event_for_test.tables.Players.query.filter_by(player_id=returned_player['player_id']).first()
            self.assertTrue(modified_player.event_player is not None)            

    def test_add_existing_player_to_event_as_scorekeeper_fails(self):                
        self.createEventsAndEventUsers()
        new_event_name = 'testEvent%s' % self.create_uniq_id()
        self.create_event_for_test(new_event_name)
        event_for_test = self.get_event_app_in_db(new_event_name)
        
        player_id,player_num,player_pin = self.get_player_id_and_number_and_pin(self.standard_player_first_name,self.standard_player_last_name,self.event_app)
        new_scorekeper_username='new_scorekeeper%s' % self.create_uniq_id()
        self.create_event_user_for_test(event_for_test,
                                        new_scorekeper_username,
                                        password=self.generic_password,
                                        role_name=roles_constants.SCOREKEEPER)

        with event_for_test.test_client() as c:                        

            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':new_scorekeper_username,
                                         'password':self.generic_password}))
            self.assertHttpCodeEquals(rv,200)                        
            rv = c.put('/player',
                       data=json.dumps({'player_id':player_id,
                                        'ifpa_ranking':9999}))
            self.assertHttpCodeEquals(rv,403)                                    
                                    
    def test_get_players(self):        
        
        with self.pss_admin_app.test_client() as c:                                                
            existing_players = self.pss_admin_app.tables.Players.query.all()
            rv = c.get('/player')
            self.assertHttpCodeEquals(rv,200)
            pss_players = json.loads(rv.data)['existing_players']                        
            self.assertEquals(len(pss_players),len(existing_players))
            for pss_player in pss_players:
                self.assertFalse('event_player' in pss_player)

        with self.event_app.test_client() as c:                                                
            player_count = self.pss_admin_app.tables.Players.query.count()
            rv = c.get('/player')
            self.assertHttpCodeEquals(rv,200)
            pss_players = json.loads(rv.data)['existing_players']            
            self.assertEquals(len(pss_players),player_count)
            for pss_player in pss_players:
                self.assertTrue('event_player_pin' not in pss_player['event_player'])

    def test_get_event_players(self):        
        
        with self.event_app.test_client() as c:                                                
            event_players = self.event_app.tables.Players.query.filter(self.event_app.tables.Players.event_player!=None).all()
            rv = c.get('/event_player')
            self.assertHttpCodeEquals(rv,200)
            returned_event_players = json.loads(rv.data)['existing_event_players']
            self.assertEquals(len(returned_event_players),len(event_players))
            for returned_event_player in returned_event_players:               
                self.assertTrue('event_player_pin' not in returned_event_player['event_player'])
            #FIXME : add check to make sure we are not returning players from other events
            
    def test_get_player(self):        
        
        with self.pss_admin_app.test_client() as c:                                                
            rv = c.get('/player/1')
            self.assertHttpCodeEquals(rv,200)
            player = json.loads(rv.data)['existing_player']                                    
            self.assertEquals(player['first_name'],self.standard_player_first_name)
            self.assertFalse('event_player' in player)
                        
        with self.event_app.test_client() as c:                                                
            rv = c.get('/event_player/1')
            self.assertHttpCodeEquals(rv,200)
            player = json.loads(rv.data)['existing_player']            
            self.assertEquals(player['first_name'],self.standard_player_first_name)
            self.assertTrue(player['event_player'] is not None)

    def test_add_existing_player_to_event_with_multi_division_tournament_selected(self):
        pass
            
            
