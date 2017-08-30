import datetime
import unittest
import os
from mock import MagicMock
import pss_integration_test_base
import json
from flask_login import current_user
from lib import roles_constants
from sqlalchemy.orm import joinedload


class RoutePssUser(pss_integration_test_base.PssIntegrationTestBase):
    def setUp(self):
        super(RoutePssUser,self).setUp()                        
        
    def test_create_pss_user(self):
        new_username = 'new_user_%s'% self.create_uniq_id()
        with self.pss_admin_app.test_client() as c:                        
            nonexistant_new_user_in_db = self.pss_admin_app.tables.PssUsers.query.filter_by(username=new_username).first()
            self.assertTrue(nonexistant_new_user_in_db is None)

            rv = c.post('/auth/pss_user/login',
                        data=json.dumps({'username':self.admin_pss_user.username,'password':self.admin_pss_user_password}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.get('/roles')            
            pss_user_role = [role for role in json.loads(rv.data)['roles'] if (role['name'] == 'pss_user')][0]
            rv = c.post('/pss_user',
                        data=json.dumps({'username':new_username,
                                         'password':'password2',
                                         'first_name':'fake first name %s' % self.create_uniq_id(),
                                         'last_name':'fake_last_name',
                                         'extra_title':'jr',
                                         'role_id':pss_user_role['admin_role_id']}))
            self.assertHttpCodeEquals(rv,200)            
            new_user_in_db = self.pss_admin_app.tables.PssUsers.query.filter_by(username=new_username).first()
            self.assertTrue(new_user_in_db is not None)
            self.assertEquals(new_user_in_db.username,new_username)

    def test_create_pss_user_fails_when_duplicate_usernames(self):
        new_username = 'new_user_dup_%s'% self.create_uniq_id()
        with self.pss_admin_app.test_client() as c:                        
            rv = c.post('/auth/pss_user/login',
                        data=json.dumps({'username':self.admin_pss_user.username,'password':self.admin_pss_user_password}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.get('/roles')            
            pss_user_role = [role for role in json.loads(rv.data)['roles'] if (role['name'] == 'pss_user')][0]
            rv = c.post('/pss_user',
                        data=json.dumps({'username':new_username,
                                         'password':'password2',
                                         'first_name':'fake first name %s' % self.create_uniq_id(),
                                         'last_name':'fake_last_name',
                                         'role_id':pss_user_role['admin_role_id']}))
            self.assertHttpCodeEquals(rv,200)
            rv = c.post('/pss_user',
                        data=json.dumps({'username':new_username,
                                         'password':'password2',
                                         'first_name':'fake first name %s' % self.create_uniq_id(),
                                         'last_name':'fake_last_name',
                                         'role_id':pss_user_role['admin_role_id']}))
            self.assertHttpCodeEquals(rv,409)

    def test_create_pss_user_fails_when_duplicate_full_names(self):
        new_username = 'new_user_dup_%s'% self.create_uniq_id()
        new_username_2 = 'new_user_dup_%s'% self.create_uniq_id()
        first_name = 'first_name %s' % self.create_uniq_id()
        with self.pss_admin_app.test_client() as c:                        
            rv = c.post('/auth/pss_user/login',
                        data=json.dumps({'username':self.admin_pss_user.username,'password':self.admin_pss_user_password}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.get('/roles')            
            pss_user_role = [role for role in json.loads(rv.data)['roles'] if (role['name'] == 'pss_user')][0]
            rv = c.post('/pss_user',
                        data=json.dumps({'username':new_username,
                                         'password':'password2',
                                         'first_name':first_name,
                                         'last_name':'fake_last_name',
                                         'extra_title':'jr',
                                         'role_id':pss_user_role['admin_role_id']}))
            self.assertHttpCodeEquals(rv,200)
            rv = c.post('/pss_user',
                        data=json.dumps({'username':new_username_2,
                                         'password':'password2',
                                         'first_name':first_name,
                                         'last_name':'fake_last_name',
                                         'extra_title':'jr',                                         
                                         'role_id':pss_user_role['admin_role_id']}))
            self.assertHttpCodeEquals(rv,409)

    def test_create_pss_user_when_duplicate_full_names_but_different_extra_title(self):
        new_username = 'new_user_dup_%s'% self.create_uniq_id()
        new_username_2 = 'new_user_dup_%s'% self.create_uniq_id()
        first_name = 'first_name %s' % self.create_uniq_id()

        with self.pss_admin_app.test_client() as c:                        
            rv = c.post('/auth/pss_user/login',
                        data=json.dumps({'username':self.admin_pss_user.username,'password':self.admin_pss_user_password}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.get('/roles')            
            pss_user_role = [role for role in json.loads(rv.data)['roles'] if (role['name'] == 'pss_user')][0]
            rv = c.post('/pss_user',
                        data=json.dumps({'username':new_username,
                                         'password':'password2',
                                         'first_name':first_name,
                                         'last_name':'fake_last_name',
                                         'extra_title':'jr',                                         
                                         'role_id':pss_user_role['admin_role_id']}))
            self.assertHttpCodeEquals(rv,200)
            rv = c.post('/pss_user',
                        data=json.dumps({'username':new_username_2,
                                         'password':'password2',
                                         'first_name':first_name,
                                         'last_name':'fake_last_name',
                                         'extra_title':'sr',                                         
                                         'role_id':pss_user_role['admin_role_id']}))
            self.assertHttpCodeEquals(rv,200)
            
    def test_create_pss_user_fails_with_bad_request_data(self):        
        new_username = 'new_user_%s'% self.create_uniq_id()
        bad_request = {'username':new_username,
                       'password':'password2'}
        with self.pss_admin_app.test_client() as c:                        
            rv = c.post('/auth/pss_user/login',
                        data=json.dumps({'username':self.admin_pss_user.username,
                                         'password':self.admin_pss_user_password}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.get('/roles')                        
            rv = c.post('/pss_user',
                        data=json.dumps({}))
            self.assertHttpCodeEquals(rv,400)            

            bad_request = {'username':new_username,
                           'password':'password'}
            rv = c.post('/pss_user',
                        data=json.dumps(bad_request))
            self.assertHttpCodeEquals(rv,400)            

            bad_request = {'username':new_username,                           
                           'role_id':1}
            rv = c.post('/pss_user',
                        data=json.dumps(bad_request))
            self.assertHttpCodeEquals(rv,400)

            bad_request = {'password':'password',                           
                           'role_id':1}
            rv = c.post('/pss_user',
                        data=json.dumps(bad_request))
            self.assertHttpCodeEquals(rv,400)            

            bad_request = {'password':'password',
                           'username':new_username,
                           'event_role_id':1}
            rv = c.post('/pss_user',
                        data=json.dumps(bad_request))
            self.assertHttpCodeEquals(rv,400)            
                
    def test_create_pss_user_fails_with_incorrect_role(self):
        new_username = 'new_user_%s'% self.create_uniq_id()
        with self.pss_admin_app.test_client() as c:                        
            rv = c.post('/auth/pss_user/login',
                        data=json.dumps({'username':self.admin_pss_user.username,'password':self.admin_pss_user_password}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.get('/roles')                        
            rv = c.post('/pss_user',
                        data=json.dumps({'username':new_username,
                                         'first_name':'fake first name %s' % self.create_uniq_id(),
                                         'last_name':'fake_last_name',                                         
                                         'password':'password2',
                                         'role_id':999999}))
            self.assertHttpCodeEquals(rv,400)            
            nonexistant_new_user_in_db = self.pss_admin_app.tables.PssUsers.query.filter_by(username=new_username).first()
            self.assertTrue(nonexistant_new_user_in_db is None)                         
    
