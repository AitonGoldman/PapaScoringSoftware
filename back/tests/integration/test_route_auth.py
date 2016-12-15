import unittest
import os
from mock import MagicMock
import td_integration_test_base
import json
from flask_login import current_user
import re
from routes import orm_creation
from routes.orm_creation import RolesEnum

class RouteAuthTD(td_integration_test_base.TdIntegrationDispatchTestBase):
    def setUp(self):
        super(RouteAuthTD,self).setUp()
        response,results = self.dispatch_request('/%s/util/healthcheck' % self.poop_db_name)                
        self.flask_app = self.app.instances[self.poop_db_name]
        orm_creation.create_stanard_roles_and_users(self.flask_app)
        self.new_player = orm_creation.create_player(self.flask_app,{'first_name':'aiton','last_name':'goldman','ifpa_ranking':'123'})        
        
    def test_login(self):        
        with self.flask_app.test_client() as c:            
            
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_scorekeeper','password':'test_scorekeeper'}))
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s' % (rv.status_code))
            self.assertIsNotNone(re.search('session\=.+',rv.headers['Set-Cookie']))            
            self.assertEquals(hasattr(current_user, 'username'),
                              True,
                              "Was expecting current_user to have a username attr, but it did not")
            self.assertEquals(current_user.username,
                              'test_scorekeeper',
                              "expected user to be test_scorekeeper, but got %s" % (current_user.username))
            returned_user = json.loads(rv.data)['data']
            self.assertFalse('player' in returned_user,                              
                            "expected player in logged in user, but none found")

            self.assertEquals('test_scorekeeper',
                              returned_user['username'],
                              "username returned was incorrect - expected %s but found %s" % ('test_scorekeeper',
                                                                                               returned_user['username']))
            self.assertFalse('password_crypt' in returned_user,
                             "Found a password field in returned user, but should not have")

            self.assertFalse('pin' in returned_user,
                             "Found a password field in returned user, but should not have")

            self.assertTrue(RolesEnum.scorekeeper.name in [role['name'] for role in returned_user['roles']],
                            "Role scorekeeper was not found in returned user")

    def test_login_player_through_user_login(self):        
        with self.flask_app.test_client() as c:            
            
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'player%s'%self.new_player.pin,'password':self.new_player.pin}))
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s' % (rv.status_code))
            self.assertIsNotNone(re.search('session\=.+',rv.headers['Set-Cookie']))            
            self.assertEquals(hasattr(current_user, 'username'),
                              True,
                              "Was expecting current_user to have a username attr, but it did not")
            self.assertEquals(current_user.username,
                              'player%s'%self.new_player.pin,
                              "expected user to be %s, but got %s" % ('player%s'%self.new_player.pin, current_user.username))
            returned_user = json.loads(rv.data)['data']
            self.assertEquals('player%s'%self.new_player.pin,
                              returned_user['username'],
                              "username returned was incorrect - expected %s but found %s" % ('player%s'%self.new_player.pin,
                                                                                               returned_user['username']))

            self.assertTrue('player' in returned_user,                              
                            "expected player in logged in user, but none found")
            self.assertEquals(1,
                              returned_user['player']['player_id'],
                              "expected logged in player to have player id of 1, but found %s" % (returned_user['player']['player_id'])
            )
            
            self.assertFalse('password_crypt' in returned_user,
                             "Found a password field in returned user, but should not have")

            self.assertFalse('pin' in returned_user,
                             "Found a password field in returned user, but should not have")
            
            self.assertTrue(RolesEnum.player.name in [role['name'] for role in returned_user['roles']],
                            "Role %s was not found in returned user" % RolesEnum.player.name)

    def test_login_player_through_player_login(self):        
        with self.flask_app.test_client() as c:            
            
            rv = c.put('/auth/player_login',
                       data=json.dumps({'player_pin':self.new_player.pin}))
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s' % (rv.status_code))
            self.assertIsNotNone(re.search('session\=.+',rv.headers['Set-Cookie']))            
            self.assertEquals(hasattr(current_user, 'username'),
                              True,
                              "Was expecting current_user to have a username attr, but it did not")
            self.assertEquals(current_user.username,
                              'player%s'%self.new_player.pin,
                              "expected user to be %s, but got %s" % ('player%s'%self.new_player.pin, current_user.username))
            returned_user = json.loads(rv.data)['data']
            self.assertEquals('player%s'%self.new_player.pin,
                              returned_user['username'],
                              "username returned was incorrect - expected %s but found %s" % ('player%s'%self.new_player.pin,
                                                                                               returned_user['username']))

            self.assertTrue('player' in returned_user,                              
                            "expected player in logged in user, but none found")
            self.assertEquals(1,
                              returned_user['player']['player_id'],
                              "expected logged in player to have player id of 1, but found %s" % (returned_user['player']['player_id'])
            )
            
            self.assertFalse('password_crypt' in returned_user,
                             "Found a password field in returned user, but should not have")

            self.assertFalse('pin' in returned_user,
                             "Found a password field in returned user, but should not have")
            
            self.assertTrue(RolesEnum.player.name in [role['name'] for role in returned_user['roles']],
                            "Role %s was not found in returned user" % RolesEnum.player.name)
            
    def test_logout_user(self):        
        with self.flask_app.test_client() as c:
            rv = c.get('/auth/logout')
            c.put('/auth/login',
                       data=json.dumps({'username':'test_user','password':'test_user_password'}))
            rv = c.get('/auth/logout')
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s' % (rv.status_code))
            self.assertFalse(hasattr(current_user, 'username'),                              
                              "Was expecting current_user to not have a username attr, but it did")
            
    def test_current_user(self):        
        with self.flask_app.test_client() as c:
            rv = c.get('/auth/current_user')
            null_user = json.loads(rv.data)['data']
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s' % (rv.status_code))
            self.assertEquals(null_user,
                              None)            
            c.put('/auth/login',
                       data=json.dumps({'username':'test_scorekeeper','password':'test_scorekeeper'}))
            rv = c.get('/auth/current_user')
            returned_user = json.loads(rv.data)['data']
            self.assertEquals('test_scorekeeper',
                              returned_user['username'],
                              "username returned was incorrect - expected %s but found %s" % ('test_scorekeeper',
                                                                                               returned_user['username']))
                        
    def test_login_bad_username_password(self):        
        with self.flask_app.test_client() as c:            
            
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'bad_baby','password':'no_cookie'}))
            self.assertEquals(rv.status_code,
                              401,
                              'Was expecting status code 401, but it was %s' % (rv.status_code))
            
            
    def test_login_no_username_password(self):        
        with self.flask_app.test_client() as c:                        
            rv = c.put('/auth/login')
            self.assertEquals(rv.status_code,
                              400,
                              'Was expecting status code 400, but it was %s' % (rv.status_code))
            rv = c.put('/auth/login',
                       data=json.dumps({}))
            self.assertEquals(rv.status_code,
                              400,
                              'Was expecting status code 400, but it was %s' % (rv.status_code))

    def test_login_player_bad_pin(self):        
        with self.flask_app.test_client() as c:            
            
            rv = c.put('/auth/player_login',
                       data=json.dumps({'player_pin':'1'}))
            self.assertEquals(rv.status_code,
                              401,
                              'Was expecting status code 401, but it was %s' % (rv.status_code))
            
            
    def test_login_player_no_pin(self):        
        with self.flask_app.test_client() as c:                        
            rv = c.put('/auth/player_login')
            self.assertEquals(rv.status_code,
                              400,
                              'Was expecting status code 400, but it was %s' % (rv.status_code))
            rv = c.put('/auth/player_login',
                       data=json.dumps({}))
            self.assertEquals(rv.status_code,
                              400,
                              'Was expecting status code 400, but it was %s' % (rv.status_code))
            

            
