import unittest
import os
from mock import MagicMock
#import pss_integration_test_base
import pss_integration_test_existing_event
import json
from flask_login import current_user
from lib import roles_constants

#FIXME : change name of class/file
class RoutePssUser(pss_integration_test_existing_event.PssIntegrationTestExistingEvent):
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
                        data=json.dumps({'username':new_username,'password':'password2','role_id':pss_user_role['admin_role_id']}))
            self.assertHttpCodeEquals(rv,200)            
            new_user_in_db = self.pss_admin_app.tables.PssUsers.query.filter_by(username=new_username).first()
            self.assertTrue(new_user_in_db is not None)
            self.assertEquals(new_user_in_db.username,new_username)

    def test_create_pss_user_fails_when_duplicate_user(self):
        new_username = 'new_user_dup_%s'% self.create_uniq_id()
        with self.pss_admin_app.test_client() as c:                        
            rv = c.post('/auth/pss_user/login',
                        data=json.dumps({'username':self.admin_pss_user.username,'password':self.admin_pss_user_password}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.get('/roles')            
            pss_user_role = [role for role in json.loads(rv.data)['roles'] if (role['name'] == 'pss_user')][0]
            rv = c.post('/pss_user',
                        data=json.dumps({'username':new_username,'password':'password2','role_id':pss_user_role['admin_role_id']}))
            self.assertHttpCodeEquals(rv,200)
            rv = c.post('/pss_user',
                        data=json.dumps({'username':new_username,'password':'password2','role_id':pss_user_role['admin_role_id']}))
            self.assertHttpCodeEquals(rv,409)
    #FIXME : add test cases for no password, no username, etc
    def test_create_pss_user_fails_with_bad_request_data(self):        
        new_username = 'new_user_%s'% self.create_uniq_id()
        with self.pss_admin_app.test_client() as c:                        
            rv = c.post('/auth/pss_user/login',
                        data=json.dumps({'username':self.admin_pss_user.username,'password':self.admin_pss_user_password}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.get('/roles')                        
            rv = c.post('/pss_user',
                        data=json.dumps({}))
            self.assertHttpCodeEquals(rv,400)            
            

    def test_create_pss_user_fails_with_incorrect_role(self):
        new_username = 'new_user_%s'% self.create_uniq_id()
        with self.pss_admin_app.test_client() as c:                        
            rv = c.post('/auth/pss_user/login',
                        data=json.dumps({'username':self.admin_pss_user.username,'password':self.admin_pss_user_password}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.get('/roles')                        
            rv = c.post('/pss_user',
                        data=json.dumps({'username':new_username,'password':'password2','role_id':999999}))
            self.assertHttpCodeEquals(rv,400)            
            nonexistant_new_user_in_db = self.pss_admin_app.tables.PssUsers.query.filter_by(username=new_username).first()
            self.assertTrue(nonexistant_new_user_in_db is None)                         
    #FIXME : test no role id while creating 

    #FIXME : negative tests for creating user 
    def test_create_pss_event_user(self):
        self.createEventsAndEventUsers()
        with self.event_app.test_client() as c:                        
            scorekeeper_role = self.event_app.tables.EventRoles.query.filter_by(name=roles_constants.SCOREKEEPER).first()
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.admin_pss_user.username,
                                         'password':self.admin_pss_user_password}))
            self.assertHttpCodeEquals(rv,200)            

            rv = c.post('/pss_user',
                        data=json.dumps({'username':'test_pss_admin_user_for_test_create_pss_event_user',
                                         'password':'password',
                                         'event_role_id':scorekeeper_role.event_role_id}))
            self.assertHttpCodeEquals(rv,200)            
            new_user = self.event_app.tables.PssUsers.query.filter_by(username='test_pss_admin_user_for_test_create_pss_event_user').first()
            self.assertTrue(new_user is not None)
            self.assertEquals(len(new_user.admin_roles),0)
            self.assertEquals(len(new_user.event_roles),1)
            self.assertEquals(new_user.event_roles[0].name,roles_constants.SCOREKEEPER)

            
