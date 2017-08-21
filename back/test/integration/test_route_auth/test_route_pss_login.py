import unittest
import os
from mock import MagicMock
import pss_integration_test_existing_event

import json
from flask_login import current_user
from lib import roles_constants

#FIXME : change name of class/file

class RoutePssLogin(pss_integration_test_existing_event.PssIntegrationTestExistingEvent):
    def setUp(self):
        super(RoutePssLogin,self).setUp()        
    #FIXME : make tests more defensive - i.e. check if can do things before you login
    def test_login_good_user_good_password(self):
        with self.pss_admin_app.test_client() as c:                        
            rv = c.post('/auth/pss_user/login',
                        data=json.dumps({'username':self.admin_pss_user.username,'password':self.admin_pss_user_password}))
            self.assertHttpCodeEquals(rv,200)            
            self.assertTrue(hasattr(current_user, 'username'),                              
                            "Was expecting current_user to have a username attr, but it did not")
            self.assertEquals(current_user.username,
                              self.admin_pss_user.username,
                              "expected user to be test_pss_admin_user, but got %s" % (current_user.username))
            self.assertTrue(current_user.is_authenticated(),                              
                             "Was expecting user to be logged in, but user was not logged in")            
            returned_user = json.loads(rv.data)['pss_user']
            self.assertEquals(returned_user['username'],self.admin_pss_user.username)            
            self.assertEquals(returned_user['admin_roles'][0]['name'],'pss_admin')
            
    def test_login_fails_with_bad_login(self):
        with self.pss_admin_app.test_client() as c:                        
            rv = c.post('/auth/pss_user/login',
                        data=json.dumps({'username':'test_pss_admin_user2','password':'passwordp'}))
            self.assertHttpCodeEquals(rv,401)
            self.assertFalse(current_user.is_authenticated(),                              
                             "Was expecting user to not be logged in, but user was logged in")

    def test_login_fails_with_bad_password(self):
        with self.pss_admin_app.test_client() as c:                        
            rv = c.post('/auth/pss_user/login',
                        data=json.dumps({'username':self.admin_pss_user.username,'password':'passwordp'}))
            self.assertHttpCodeEquals(rv,401)
            self.assertFalse(current_user.is_authenticated(),                              
                             "Was expecting user to not be logged in, but user was logged in")
    
    def test_login_fails_with_pss_user_with_incorrect_role(self):
        self.bootstrap_extra_users(self.pss_admin_app)
        with self.pss_admin_app.test_client() as c:                        
            rv = c.post('/auth/pss_user/login',
                        data=json.dumps({'username':self.pss_user_with_no_roles.username,'password':self.pss_user_with_no_roles_password}))
            self.assertHttpCodeEquals(rv,401)            
            self.assertEquals(rv.data,'{"message": "User can not access this"}')
            self.assertFalse(current_user.is_authenticated(),                              
                             "Was expecting user to not be logged in, but user was logged in")
            
    
    def test_login_fails_with_missing_fields_in_post(self):
        with self.pss_admin_app.test_client() as c:                        
            rv = c.post('/auth/pss_user/login')
            self.assertHttpCodeEquals(rv,400)
            self.assertFalse(current_user.is_authenticated(),                              
                            "Was expecting user to not be logged in, but user was logged in")
            self.assertFalse(hasattr(current_user, 'username'),                              
                            "Was expecting current_user to have not have a username attr, but it did")
    
    def test_login_fails_when_logging_in_as_event_user(self):        
        pass
    
    def test_login_fails_when_logging_into_2_events(self):
        self.createEventsAndEventUsers()
        with self.event_app.test_client() as c:                        
            scorekeeper_role = self.event_app.tables.EventRoles.query.filter_by(name=roles_constants.SCOREKEEPER).first()
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.event_user_scorekeeper,
                                         'password':'password'}))
            self.assertHttpCodeEquals(rv,200)                                    
            cookie = rv.headers['Set-Cookie'].split("=")[1]
            cookie = cookie.split(";")[0]                        

        #new_app_2 = self.get_event_app_in_db(new_event_name_2)
        with self.event_app_2.test_client() as c:                                    
            c.set_cookie('localhost','session', cookie)
            rv = c.get('/auth/pss_event_user/current_user')
            self.assertHttpCodeEquals(rv,200)            
            self.assertEquals(json.loads(rv.data)['current_user'],None)
            
    
    def test_login_fails_when_logging_into_1_event_and_admin_event(self):
        self.createEventsAndEventUsers()
        
        with self.event_app.test_client() as c:                        

            scorekeeper_role = self.event_app.tables.EventRoles.query.filter_by(name=roles_constants.SCOREKEEPER).first()
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.event_user_scorekeeper,
                                         'password':'password'}))
            self.assertHttpCodeEquals(rv,200)
            cookie = rv.headers['Set-Cookie'].split("=")[1]
            cookie = cookie.split(";")[0]                        

        with self.pss_admin_app.test_client() as c:                             
            c.set_cookie('localhost','session', cookie)
            rv = c.get('/auth/pss_user/current_user')
            self.assertHttpCodeEquals(rv,200)            
            self.assertEquals(json.loads(rv.data)['current_user'],None)

            
    def test_player_login(self):
        self.createEventsAndEventUsers()        
        with self.event_app.test_client() as c:                        
            tables = self.event_app.tables
            existing_player = tables.Players.query.filter(tables.Players.event_player.has(tables.EventPlayers.event_player_id==1)).first()
            rv = c.post('/auth/player/login',
                        data=json.dumps({'event_player_number':1,'event_player_pin':existing_player.event_player.event_player_pin}))
            self.assertHttpCodeEquals(rv,200)            
            self.assertTrue(hasattr(current_user, 'player_id'),                              
                            "Was expecting current_user to have a player_id attr, but it did not")
            self.assertEquals(current_user.player_id,
                              1,
                              "expected player_id to be 1, but got %s" % (current_user.player_id))
            self.assertTrue(current_user.is_authenticated(),                              
                             "Was expecting player to be logged in, but player was not logged in")            
            returned_player = json.loads(rv.data)['player']
            self.assertEquals(returned_player['player_id'],1)            
            self.assertTrue('event_player_pin' not in returned_player['event_player'])
            self.assertEquals(returned_player['event_player']['ifpa_ranking'],9999)
            self.assertEquals(len(returned_player['player_roles']),1)

    def test_player_login_with_bad_info_fails(self):
        self.createEventsAndEventUsers()        
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
        self.createEventsAndEventUsers()        
        with self.event_app_2.test_client() as c:                        
            tables = self.event_app.tables
            existing_player = self.event_app.tables.Players.query.filter(tables.Players.event_player.has(tables.EventPlayers.event_player_id==2)).first()            
            rv = c.post('/auth/player/login',
                        data=json.dumps({'event_player_number':2,'event_player_pin':existing_player.event_player.event_player_pin}))
            self.assertHttpCodeEquals(rv,401)            
            self.assertFalse(current_user.is_authenticated())

            
            
