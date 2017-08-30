import datetime
import unittest
import os
from mock import MagicMock
import pss_integration_test_existing_event
import json
from flask_login import current_user
from lib import roles_constants
from sqlalchemy.orm import joinedload


class RouteEventUser(pss_integration_test_existing_event.PssIntegrationTestExistingEvent):
    def setUp(self):
        super(RouteEventUser,self).setUp()                        
        
    def test_create_pss_event_user_while_logged_into_event_as_admin(self):
        #FIXME : use generated names
        
        with self.event_app.test_client() as c:                        
            scorekeeper_role = self.event_app.tables.EventRoles.query.filter_by(name=roles_constants.SCOREKEEPER).first()
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.admin_pss_user.username,
                                         'password':self.admin_pss_user_password}))
            self.assertHttpCodeEquals(rv,200)            

            rv = c.post('/pss_event_user',
                        data=json.dumps({'username':'test_pss_admin_user_for_test_create_pss_event_user',
                                         'password':'password',
                                         'first_name':'fake_first_name',
                                         'last_name':'fake_last_name',
                                         'event_role_id':scorekeeper_role.event_role_id}))
            self.assertHttpCodeEquals(rv,200)            
            new_user = self.event_app.tables.PssUsers.query.filter_by(username='test_pss_admin_user_for_test_create_pss_event_user').first()
            self.assertTrue(new_user is not None)
            self.assertEquals(len(new_user.admin_roles),0)
            self.assertEquals(len(new_user.event_roles),1)
            self.assertEquals(new_user.event_roles[0].name,roles_constants.SCOREKEEPER)

    def test_create_pss_event_user_while_logged_into_event_as_td(self):        
        with self.event_app.test_client() as c:                        
            td_role = self.event_app.tables.EventRoles.query.filter_by(name=roles_constants.TOURNAMENT_DIRECTOR).first()
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.standard_td_username,
                                         'password':self.generic_password}))
            self.assertHttpCodeEquals(rv,200)            
            new_username = 'test_pss_user%s' % self.create_uniq_id()
            rv = c.post('/pss_event_user',
                        data=json.dumps({'username':new_username ,
                                         'password':'password',
                                         'first_name':'fake_first_name%s'% self.create_uniq_id(),
                                         'last_name':'fake_last_name%s'% self.create_uniq_id(),
                                         'event_role_id':td_role.event_role_id}))
            self.assertHttpCodeEquals(rv,200)            
            new_user = self.event_app.tables.PssUsers.query.filter_by(username=new_username).first()
            self.assertTrue(new_user is not None)
            self.assertEquals(len(new_user.admin_roles),0)
            self.assertEquals(len(new_user.event_roles),1)
            self.assertEquals(new_user.event_roles[0].name,roles_constants.TOURNAMENT_DIRECTOR)

    def test_create_pss_event_user_fails_when_duplicate_usernames(self):
        
        new_username = 'new_user_dup_%s'% self.create_uniq_id()
        with self.event_app.test_client() as c:                        
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.admin_pss_user.username,'password':self.admin_pss_user_password}))
            self.assertHttpCodeEquals(rv,200)            
            td_role = self.event_app.tables.EventRoles.query.filter_by(name=roles_constants.TOURNAMENT_DIRECTOR).first()

            rv = c.post('/pss_event_user',
                        data=json.dumps({'username':new_username,
                                         'password':'password2',
                                         'first_name':'fake first name %s' % self.create_uniq_id(),
                                         'last_name':'fake_last_name',
                                         'event_role_id':td_role.event_role_id}))
            self.assertHttpCodeEquals(rv,200)
            rv = c.post('/pss_event_user',
                        data=json.dumps({'username':new_username,
                                         'password':'password2',
                                         'first_name':'fake first name %s' % self.create_uniq_id(),
                                         'last_name':'fake_last_name',
                                         'event_role_id':td_role.event_role_id}))
            self.assertHttpCodeEquals(rv,409)
            
    def test_create_pss_event_user_while_logged_in_as_scorekeeper_fails(self):                
        
        with self.event_app.test_client() as c:                        
            td_role = self.event_app.tables.EventRoles.query.filter_by(name=roles_constants.TOURNAMENT_DIRECTOR).first()
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.standard_scorekeeper_username,
                                         'password':self.generic_password}))
            self.assertHttpCodeEquals(rv,200)            
            new_username = 'test_pss_user%s' % self.create_uniq_id()
            rv = c.post('/pss_event_user',
                        data=json.dumps({'username':new_username ,
                                         'password':'password',
                                         'first_name':'fake_first_name%s'% self.create_uniq_id(),
                                         'last_name':'fake_last_name%s'% self.create_uniq_id(),
                                         'event_role_id':td_role.event_role_id}))
            self.assertHttpCodeEquals(rv,403)            
            new_user = self.event_app.tables.PssUsers.query.filter_by(username=new_username).first()
            self.assertTrue(new_user is None)

    def test_create_pss_event_user_fails_with_bad_request_data(self):        
        new_username = 'new_user_%s'% self.create_uniq_id()
        bad_request = {'username':new_username,
                       'password':'password2',
                       'first_name':'test_first_name_bad',
                       'last_name':'test_last_name_bad',
                       'event_role_id':1}
        with self.event_app.test_client() as c:                        
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.admin_pss_user.username,
                                         'password':self.admin_pss_user_password}))
            self.assertHttpCodeEquals(rv,200)                        
            rv = c.post('/pss_event_user',
                        data=json.dumps({}))
            self.assertHttpCodeEquals(rv,400)            

            bad_request_copy = bad_request.copy()
            bad_request_copy.pop('event_role_id',None)
            rv = c.post('/pss_event_user',
                        data=json.dumps(bad_request_copy))
            self.assertHttpCodeEquals(rv,400)            

            bad_request_copy = bad_request.copy()
            bad_request_copy.pop('event_role_id',None)
            bad_request_copy['role_id']=1
            rv = c.post('/pss_event_user',
                        data=json.dumps(bad_request_copy))
            self.assertHttpCodeEquals(rv,400)            
            
            bad_request_copy = bad_request.copy()
            bad_request_copy.pop('username',None)
            rv = c.post('/pss_event_user',
                        data=json.dumps(bad_request_copy))
            self.assertHttpCodeEquals(rv,400)            

            bad_request_copy = bad_request.copy()
            bad_request_copy.pop('password',None)
            rv = c.post('/pss_event_user',
                        data=json.dumps(bad_request_copy))
            self.assertHttpCodeEquals(rv,400)            

            bad_request_copy = bad_request.copy()
            bad_request_copy.pop('first_name',None)
            rv = c.post('/pss_event_user',
                        data=json.dumps(bad_request_copy))
            self.assertHttpCodeEquals(rv,400)            

            bad_request_copy = bad_request.copy()
            bad_request_copy.pop('last_name',None)
            rv = c.post('/pss_event_user',
                        data=json.dumps(bad_request_copy))
            self.assertHttpCodeEquals(rv,400)            


    def test_add_existing_pss_user_scorekeeper_to_event_as_tournament_director(self):                        
        
        new_event_name = 'testEvent%s' % self.create_uniq_id()
        self.create_event_for_test(new_event_name)
        event_for_test = self.get_event_app_in_db(new_event_name)
            
        with event_for_test.test_client() as c:                        
            #FIXME : should be using /roles route
            td_role = self.event_app.tables.EventRoles.query.filter_by(name=roles_constants.TOURNAMENT_DIRECTOR).first()            
            existing_scorekeeper_user = self.get_existing_event_user(self.standard_scorekeeper_username,self.event_app)
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.admin_pss_user.username,
                                         'password':self.admin_pss_user_password}))
            self.assertHttpCodeEquals(rv,200)                        
            rv = c.put('/pss_event_user',
                       data=json.dumps({'username':existing_scorekeeper_user.username,
                                        'password':'%snew'%self.generic_password,
                                        'pss_user_id':existing_scorekeeper_user.pss_user_id,
                                        'event_role_id':td_role.event_role_id}))
            self.assertHttpCodeEquals(rv,200)            
            existing_scorekeeper_user = self.get_existing_event_user(self.standard_scorekeeper_username,event_for_test)

            self.assertTrue(roles_constants.TOURNAMENT_DIRECTOR in [ role.name for role in existing_scorekeeper_user.event_roles])            
            self.assertTrue(self.event_app.name in [ event.name for event in existing_scorekeeper_user.events])            

    def test_edit_existing_pss_event_user(self):                
        
        td_role = self.event_app.tables.EventRoles.query.filter_by(name=roles_constants.TOURNAMENT_DIRECTOR).first()        
        td_role_id = td_role.event_role_id
            
        with self.event_app.test_client() as c:                                    
            
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.standard_td_username,
                                         'password':'password'}))
            self.assertHttpCodeEquals(rv,200)

            user_pw='password222'
            username='test_pss_user_scorekeeper%s'% self.create_uniq_id()                
            role_name=roles_constants.SCOREKEEPER
            new_user = self.create_event_user_for_test(self.event_app,
                                                       username,role_name,                                  
                                                       password=user_pw)

            new_user_id = new_user['new_pss_user']['pss_user_id']            
            rv = c.put('/pss_event_user',
                       data=json.dumps({'username':username,
                                        'password':'newpassword',
                                        'pss_user_id':new_user_id,
                                        'event_role_id':td_role.event_role_id}))
            self.assertHttpCodeEquals(rv,200)
            existing_user = self.event_app.tables.PssUsers.query.filter_by(username=username).first()
            self.assertTrue(roles_constants.TOURNAMENT_DIRECTOR in [ role.name for role in existing_user.event_roles])            
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':username,
                                         'password':'newpassword'}))
            self.assertHttpCodeEquals(rv,200)                        
            
            
    def test_add_existing_pss_user_with_incorrect_permissions_fails(self):                
        
        with self.event_app.test_client() as c:                        
            td_role = self.event_app.tables.EventRoles.query.filter_by(name=roles_constants.TOURNAMENT_DIRECTOR).first()
            existing_scorekeeper_user = self.get_existing_event_user(self.standard_scorekeeper_username,self.event_app)
            
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.standard_scorekeeper_username,
                                         'password':self.generic_password}))
            self.assertHttpCodeEquals(rv,200)                        
            rv = c.put('/pss_event_user',
                       data=json.dumps({'username':self.standard_scorekeeper_username,
                                        'password':self.generic_password+'new',
                                        'pss_user_id':existing_scorekeeper_user.pss_user_id,
                                        'event_role_id':td_role.event_role_id}))
            self.assertHttpCodeEquals(rv,403)                        
            
                                    
    def test_get_users(self):        
        
        with self.pss_admin_app.test_client() as c:                                                
            existing_users = self.pss_admin_app.tables.PssUsers.query.all()
            rv = c.get('/pss_user')
            self.assertHttpCodeEquals(rv,200)
            pss_users = json.loads(rv.data)['existing_pss_users']                        
            self.assertEquals(len(pss_users),len(existing_users))
            for pss_user in pss_users:
                if pss_user['event_user']:
                    self.assertTrue('password_crypt' not in pss_user['event_user'])

        with self.event_app.test_client() as c:                                                
            user_count = self.pss_admin_app.tables.PssUsers.query.count()
            rv = c.get('/pss_user')
            self.assertHttpCodeEquals(rv,200)
            pss_users = json.loads(rv.data)['existing_pss_users']            
            self.assertEquals(len(pss_users),user_count)
            pss_users = json.loads(rv.data)['existing_pss_users']                        
            self.assertEquals(len(pss_users),len(existing_users))
            for pss_user in pss_users:
                if pss_user['event_user']:                    
                    self.assertTrue('password_crypt' not in pss_user['event_user'])

    def test_get_event_users(self):        
        with self.event_app.test_client() as c:                                                
            event_users = self.event_app.tables.PssUsers.query.filter(self.event_app.tables.PssUsers.event_user!=None).all()
            rv = c.get('/pss_event_user')
            self.assertHttpCodeEquals(rv,200)
            returned_event_users = json.loads(rv.data)['existing_pss_event_users']
            self.assertEquals(len(returned_event_users),len(event_users))
            for returned_event_user in returned_event_users:               
                self.assertTrue('password_crypt' not in returned_event_user['event_user'])
                    
    def test_get_user(self):        
        with self.pss_admin_app.test_client() as c:                                                
            existing_user = self.get_existing_event_user(self.standard_td_username,self.pss_admin_app)
            rv = c.get('/pss_user/%s' % existing_user.pss_user_id)
            self.assertHttpCodeEquals(rv,200)
            pss_user = json.loads(rv.data)['existing_pss_user']                                    
            self.assertEquals(pss_user['username'],existing_user.username)
            self.assertTrue(pss_user['event_user'] is None)
                        
        with self.event_app.test_client() as c:                                                
            existing_user = self.get_existing_event_user(self.standard_td_username,self.event_app)
            rv = c.get('/pss_event_user/%s' % existing_user.pss_user_id)
            self.assertHttpCodeEquals(rv,200)
            pss_user = json.loads(rv.data)['existing_pss_user']            
            self.assertEquals(pss_user['username'],existing_user.username)
            self.assertTrue(pss_user['event_user'] is not None)

            existing_users = self.pss_admin_app.tables.PssUsers.query.all()
            event = self.event_app.tables.Events.query.filter_by(name=self.event_app.name).first()
            for existing_user in existing_users:
                if existing_user.event_user and event not in existing_user.events:
                    event_user = existing_user                    
            rv = c.get('/pss_event_user/%s'%event_user.pss_user_id)
            self.assertHttpCodeEquals(rv,400)
                        
            
            
