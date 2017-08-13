import unittest
import os
from mock import MagicMock
import pss_integration_test_base
import json
from flask_login import current_user

#FIXME : change name of class/file
class RoutePssUserCreate(pss_integration_test_base.PssIntegrationTestBase):
    def setUp(self):
        super(RoutePssUserCreate,self).setUp()        
        
    def test_create_pss_user(self):
        with self.pss_admin_app.test_client() as c:                        
            nonexistant_new_user_in_db = self.pss_admin_app.tables.PssUsers.query.filter_by(username='new_test_user').first()
            self.assertTrue(nonexistant_new_user_in_db is None)

            rv = c.post('/auth/pss_user/login',
                        data=json.dumps({'username':'test_pss_admin_user','password':'password'}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.get('/roles')            
            pss_user_role = [role for role in json.loads(rv.data)['roles'] if (role['name'] == 'pss_user')][0]
            rv = c.post('/pss_user',
                        data=json.dumps({'username':'new_test_user','password':'password2','role_id':pss_user_role['role_id']}))
            self.assertHttpCodeEquals(rv,200)            
            new_user_in_db = self.pss_admin_app.tables.PssUsers.query.filter_by(username='new_test_user').first()
            self.assertTrue(new_user_in_db is not None)
            self.assertEquals(new_user_in_db.username,'new_test_user')

    def test_create_pss_user_fails_when_duplicate_user(self):
        with self.pss_admin_app.test_client() as c:                        
            rv = c.post('/auth/pss_user/login',
                        data=json.dumps({'username':'test_pss_admin_user','password':'password'}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.get('/roles')            
            pss_user_role = [role for role in json.loads(rv.data)['roles'] if (role['name'] == 'pss_user')][0]
            rv = c.post('/pss_user',
                        data=json.dumps({'username':'new_test_user','password':'password2','role_id':pss_user_role['role_id']}))
            self.assertHttpCodeEquals(rv,200)
            rv = c.post('/pss_user',
                        data=json.dumps({'username':'new_test_user','password':'password2','role_id':pss_user_role['role_id']}))
            self.assertHttpCodeEquals(rv,409)
            
    def test_create_pss_user_fails_with_bad_request_data(self):
        with self.pss_admin_app.test_client() as c:                        
            rv = c.post('/auth/pss_user/login',
                        data=json.dumps({'username':'test_pss_admin_user','password':'password'}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.get('/roles')                        
            rv = c.post('/pss_user',
                        data=json.dumps({}))
            self.assertHttpCodeEquals(rv,400)            
            nonexistant_new_user_in_db = self.pss_admin_app.tables.PssUsers.query.filter_by(username='new_test_user').first()
            self.assertTrue(nonexistant_new_user_in_db is None)                         
            

    def test_create_pss_user_fails_with_incorrect_role(self):
        with self.pss_admin_app.test_client() as c:                        
            rv = c.post('/auth/pss_user/login',
                        data=json.dumps({'username':'test_pss_admin_user','password':'password'}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.get('/roles')                        
            rv = c.post('/pss_user',
                        data=json.dumps({'username':'new_test_user','password':'password2','role_id':999999}))
            self.assertHttpCodeEquals(rv,400)            
            nonexistant_new_user_in_db = self.pss_admin_app.tables.PssUsers.query.filter_by(username='new_test_user').first()
            self.assertTrue(nonexistant_new_user_in_db is None)                         
            
            
