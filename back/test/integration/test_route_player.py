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
                        data=json.dumps({'username':self.event_user_td,
                                         'password':'password'}))
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
                        data=json.dumps({'username':self.event_user_td,
                                         'password':'password'}))
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
                        data=json.dumps({'username':self.event_user_td,
                                         'password':'password'}))
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
                        data=json.dumps({'username':self.event_user_scorekeeper,
                                         'password':'password'}))
            self.assertHttpCodeEquals(rv,200)                        
            rv = c.post('/player',
                        data=json.dumps({'first_name':new_player_first_name,
                                         'last_name':'last_name',
                                         'ifpa_ranking':9999}))

            self.assertHttpCodeEquals(rv,403)                        

    def test_add_existing_player_to_event_as_tournament_director(self):                
        self.createEventsAndEventUsers()
        existing_player = self.event_app_2.tables.Players.query.filter_by(first_name=self.player_one_first_name).first()
        player_one_player_id = existing_player.player_id
        with self.event_app_2.test_client() as c:                        
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.event_user_td_2,
                                         'password':'password'}))
            self.assertHttpCodeEquals(rv,200)                        
            rv = c.put('/player',
                       data=json.dumps({'player_id':player_one_player_id,
                                        'ifpa_ranking':9999}))
            self.assertHttpCodeEquals(rv,200)            
            returned_player = json.loads(rv.data)['existing_player_added_to_event']
            self.assertEquals(returned_player['first_name'],self.player_one_first_name)
            self.assertEquals(returned_player['last_name'],'test_player_last_name')
            self.assertEquals(returned_player['event_player']['ifpa_ranking'],9999)
            self.assertEquals(len(returned_player['player_roles']),1)
            self.assertEquals(len(returned_player['events']),2)            
            modified_player = self.event_app_2.tables.Players.query.filter_by(first_name=self.player_one_first_name).first()
            self.assertTrue(modified_player.event_player is not None)            

    def test_add_existing_player_to_event_as_scorekeeper_fails(self):                
        self.createEventsAndEventUsers()
        existing_player = self.event_app_2.tables.Players.query.filter_by(first_name=self.player_one_first_name).first()
        player_one_player_id = existing_player.player_id
        with self.event_app_2.test_client() as c:                        
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.event_user_scorekeeper_2,
                                         'password':'password'}))
            self.assertHttpCodeEquals(rv,200)                        
            rv = c.put('/player',
                       data=json.dumps({'player_id':player_one_player_id,
                                        'ifpa_ranking':9999}))
            self.assertHttpCodeEquals(rv,403)                                    
                                    
    def test_get_players(self):        
        self.createEventsAndEventUsers()
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
        self.createEventsAndEventUsers()
        with self.event_app.test_client() as c:                                                
            event_players = self.event_app.tables.Players.query.filter(self.event_app.tables.Players.event_player!=None).all()
            rv = c.get('/event_player')
            self.assertHttpCodeEquals(rv,200)
            returned_event_players = json.loads(rv.data)['existing_event_players']
            self.assertEquals(len(returned_event_players),len(event_players))
            for returned_event_player in returned_event_players:               
                self.assertTrue('event_player_pin' not in returned_event_player['event_player'])
                    
    def test_get_player(self):        
        self.createEventsAndEventUsers()
        with self.pss_admin_app.test_client() as c:                                                
            rv = c.get('/player/1')
            self.assertHttpCodeEquals(rv,200)
            player = json.loads(rv.data)['existing_player']                                    
            self.assertEquals(player['first_name'],'playerOneFirstName')
            self.assertFalse('event_player' in player)
                        
        with self.event_app.test_client() as c:                                                
            rv = c.get('/event_player/1')
            self.assertHttpCodeEquals(rv,200)
            player = json.loads(rv.data)['existing_player']            
            self.assertEquals(player['first_name'],'playerOneFirstName')
            self.assertTrue(player['event_player'] is not None)

                        
            
            
