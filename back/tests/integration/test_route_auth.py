import unittest
import os
from mock import MagicMock
import td_integration_test_base
import json
from flask_login import current_user
import re

class RouteAuthTD(td_integration_test_base.TdIntegrationDispatchTestBase):
    def setUp(self):
        super(RouteAuthTD,self).setUp()
        response,results = self.dispatch_request('/%s/util/healthcheck' % self.poop_db_name)                
        self.flask_app = self.app.instances[self.poop_db_name]
        self.new_user = self.flask_app.tables.User(username='test_user')
        self.new_user.crypt_password('test_user_password')

        self.new_role = self.flask_app.tables.Role(name='test_role')
        self.flask_app.tables.db_handle.session.add(self.new_role)
        self.flask_app.tables.db_handle.session.commit()

        self.new_user.roles.append(self.new_role)
        self.flask_app.tables.db_handle.session.add(self.new_user)
        self.flask_app.tables.db_handle.session.commit()
        
    def test_login(self):        
        with self.flask_app.test_client() as c:            
            
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.new_user.username,'password':'test_user_password'}))
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s' % (rv.status_code))
            self.assertIsNotNone(re.search('session\=.+',rv.headers['Set-Cookie']))            
            self.assertEquals(hasattr(current_user, 'username'),
                              True,
                              "Was expecting current_user to have a username attr, but it did not")
            self.assertEquals(current_user.username,
                              self.new_user.username,
                              "expected user to be %s, but got %s" % (self.new_user.username, current_user.username))
            returned_user = json.loads(rv.data)['data']
            self.assertEquals(self.new_user.username,
                              returned_user['username'],
                              "username returned was incorrect - expected %s but found %s" % (self.new_user.username,
                                                                                               returned_user['username']))
            self.assertFalse(hasattr(returned_user,'password_crypt'),
                             "Found a password field in returned user, but should not have")

            self.assertTrue(self.new_role.name in returned_user['roles'],
                            "Role %s was not found in returned user" % self.new_role.name)

    def test_logout_user(self):        
        with self.flask_app.test_client() as c:
            rv = c.get('/auth/logout')
            self.assertEquals(rv.status_code,
                              401,
                              'Was expecting status code 401, but it was %s' % (rv.status_code))
            c.put('/auth/login',
                       data=json.dumps({'username':self.new_user.username,'password':'test_user_password'}))
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
                       data=json.dumps({'username':self.new_user.username,'password':'test_user_password'}))
            rv = c.get('/auth/current_user')
            returned_user = json.loads(rv.data)['data']
            self.assertEquals(self.new_user.username,
                              returned_user['username'],
                              "username returned was incorrect - expected %s but found %s" % (self.new_user.username,
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
                              'Was expecting status code 401, but it was %s' % (rv.status_code))
            rv = c.put('/auth/login',
                       data=json.dumps({}))
            self.assertEquals(rv.status_code,
                              400,
                              'Was expecting status code 401, but it was %s' % (rv.status_code))
            

            
