import datetime
import unittest
import os
from mock import MagicMock
import pss_integration_test_existing_event
import json
from flask_login import current_user
from lib import roles_constants
from sqlalchemy.orm import joinedload


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
    
    def test_create_pss_event_user_while_logged_into_event_as_admin(self):
        #FIXME : use generated names
        self.createEventsAndEventUsers()
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
        #FIXME : use generated names
        #FIXME : for all tests, make sure passwords are generated
        self.createEventsAndEventUsers()
        with self.event_app.test_client() as c:                        
            td_role = self.event_app.tables.EventRoles.query.filter_by(name=roles_constants.TOURNAMENT_DIRECTOR).first()
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.event_user_td,
                                         'password':'password'}))
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
        self.createEventsAndEventUsers()
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
        self.createEventsAndEventUsers()
        with self.event_app.test_client() as c:                        
            td_role = self.event_app.tables.EventRoles.query.filter_by(name=roles_constants.TOURNAMENT_DIRECTOR).first()
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.event_user_scorekeeper,
                                         'password':'password'}))
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
        #FIXME : should only need to create event and roles once for whole test run
        self.createEventsAndEventUsers()
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
        self.createEventsAndEventUsers()
        scorekeeper_role = self.event_app_2.tables.EventRoles.query.filter_by(name=roles_constants.SCOREKEEPER).first()
        td_role = self.event_app_2.tables.EventRoles.query.filter_by(name=roles_constants.TOURNAMENT_DIRECTOR).first()        
        existing_pss_user = self.event_app_2.tables.PssUsers.query.filter(self.event_app_2.tables.PssUsers.event_roles.contains(scorekeeper_role)).first()
        existing_pss_user_id=existing_pss_user.pss_user_id
        existing_pss_username=existing_pss_user.username
            
        with self.event_app.test_client() as c:                        
            td_role = self.event_app.tables.EventRoles.query.filter_by(name=roles_constants.TOURNAMENT_DIRECTOR).first()
            
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.event_user_td,
                                         'password':'password'}))
            self.assertHttpCodeEquals(rv,200)                        
            rv = c.put('/pss_event_user',
                       data=json.dumps({'username':existing_pss_username,
                                        'password':'passwordpassword',
                                        'pss_user_id':existing_pss_user_id,
                                        'event_role_id':td_role.event_role_id}))
            self.assertHttpCodeEquals(rv,200)            
            existing_user = self.event_app.tables.PssUsers.query.filter_by(username=existing_pss_username).first()
            self.assertTrue(roles_constants.TOURNAMENT_DIRECTOR in [ role.name for role in existing_user.event_roles])            
            self.assertTrue(self.event_app.name in [ event.name for event in existing_user.events])            

    def test_edit_existing_pss_event_user(self):                
        self.createEventsAndEventUsers()
        scorekeeper_role = self.event_app.tables.EventRoles.query.filter_by(name=roles_constants.SCOREKEEPER).first()
        td_role = self.event_app.tables.EventRoles.query.filter_by(name=roles_constants.TOURNAMENT_DIRECTOR).first()        
        td_role_id = td_role.event_role_id
        existing_pss_user = self.event_app.tables.PssUsers.query.filter(self.event_app.tables.PssUsers.event_roles.contains(scorekeeper_role)).first()
        existing_pss_user_id=existing_pss_user.pss_user_id
        existing_pss_username=existing_pss_user.username
            
        with self.event_app.test_client() as c:                                    
            
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.event_user_td,
                                         'password':'password'}))
            self.assertHttpCodeEquals(rv,200)                        
            rv = c.put('/pss_event_user',
                       data=json.dumps({'username':existing_pss_username,
                                        'password':'newpassword',
                                        'pss_user_id':existing_pss_user_id,
                                        'event_role_id':td_role.event_role_id}))
            self.assertHttpCodeEquals(rv,200)            
            existing_user = self.event_app.tables.PssUsers.query.filter_by(username=existing_pss_username).first()
            self.assertTrue(roles_constants.TOURNAMENT_DIRECTOR in [ role.name for role in existing_user.event_roles])            
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':existing_pss_username,
                                         'password':'newpassword'}))
            self.assertHttpCodeEquals(rv,200)                        
            
            
    def test_add_existing_pss_user_with_incorrect_permissions_fails(self):                
        self.createEventsAndEventUsers()
        scorekeeper_role = self.event_app_2.tables.EventRoles.query.filter_by(name=roles_constants.SCOREKEEPER).first()
        td_role = self.event_app_2.tables.EventRoles.query.filter_by(name=roles_constants.TOURNAMENT_DIRECTOR).first()        
        existing_pss_user = self.event_app_2.tables.PssUsers.query.filter(self.event_app_2.tables.PssUsers.event_roles.contains(scorekeeper_role)).first()
        existing_pss_user_id=existing_pss_user.pss_user_id
        existing_pss_username=existing_pss_user.username                
        
        with self.event_app.test_client() as c:                        
            td_role = self.event_app.tables.EventRoles.query.filter_by(name=roles_constants.TOURNAMENT_DIRECTOR).first()
            scorekeeper_user = self.event_app.tables.PssUsers.query.filter(self.event_app.tables.PssUsers.event_roles.contains(scorekeeper_role)).first()
            
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':scorekeeper_user.username,
                                         'password':'password'}))
            self.assertHttpCodeEquals(rv,200)                        
            rv = c.put('/pss_event_user',
                       data=json.dumps({'username':existing_pss_username,
                                        'password':'passwordpassword',
                                        'pss_user_id':existing_pss_user_id,
                                        'event_role_id':td_role.event_role_id}))
            self.assertHttpCodeEquals(rv,403)                        
            
                                    
    def test_get_users(self):        
        self.createEventsAndEventUsers()
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
        self.createEventsAndEventUsers()
        with self.event_app.test_client() as c:                                                
            event_users = self.event_app.tables.PssUsers.query.filter(self.event_app.tables.PssUsers.event_user!=None).all()
            rv = c.get('/pss_event_user')
            self.assertHttpCodeEquals(rv,200)
            returned_event_users = json.loads(rv.data)['existing_pss_event_users']
            self.assertEquals(len(returned_event_users),len(event_users))
            for returned_event_user in returned_event_users:               
                self.assertTrue('password_crypt' not in returned_event_user['event_user'])
                    
    def test_get_user(self):        
        self.createEventsAndEventUsers()
        with self.pss_admin_app.test_client() as c:                                                
            rv = c.get('/pss_user/2')
            self.assertHttpCodeEquals(rv,200)
            pss_user = json.loads(rv.data)['existing_pss_user']                                    
            self.assertEquals(pss_user['username'],'eventUserScorekeeper')
            self.assertTrue(pss_user['event_user'] is None)
                        
        with self.event_app.test_client() as c:                                                
            rv = c.get('/pss_event_user/1')
            self.assertHttpCodeEquals(rv,200)
            pss_user = json.loads(rv.data)['existing_pss_user']            
            self.assertEquals(pss_user['username'],'test_pss_admin_user')
            self.assertTrue(pss_user['event_user'] is not None)

            existing_users = self.pss_admin_app.tables.PssUsers.query.all()
            event = self.event_app.tables.Events.query.filter_by(name=self.event_app.name).first()
            for existing_user in existing_users:
                if existing_user.event_user and event not in existing_user.events:
                    event_user = existing_user                    
            rv = c.get('/pss_event_user/%s'%event_user.pss_user_id)
            self.assertHttpCodeEquals(rv,400)
                        
            
            
