import unittest
import os
from mock import MagicMock
import td_integration_test_base
import json
from flask_login import current_user
import re
from routes import orm_creation

class RouteUserTD(td_integration_test_base.TdIntegrationDispatchTestBase):
    def setUp(self):
        super(RouteUserTD,self).setUp()
        response,results = self.dispatch_request('/%s/util/healthcheck' % self.poop_db_name)                
        self.flask_app = self.app.instances[self.poop_db_name]
        orm_creation.create_stanard_roles_and_users(self.flask_app)
        self.new_player = orm_creation.create_player(self.flask_app,{'first_name':'aiton','last_name':'goldman','ifpa_ranking':'123'})        

        # self.new_role = self.flask_app.tables.Role(name='test_role')
        # self.flask_app.tables.db_handle.session.add(self.new_role)
        # self.flask_app.tables.db_handle.session.commit()

        # self.new_role_id = self.new_role.role_id
        
        # self.new_role_2 = self.flask_app.tables.Role(name='test_role_2')
        # self.flask_app.tables.db_handle.session.add(self.new_role_2)
        # self.flask_app.tables.db_handle.session.commit()

        # self.new_role_2_id = self.new_role_2.role_id
        
        # self.admin_role = self.flask_app.tables.Role(name='admin')
        # self.flask_app.tables.db_handle.session.add(self.admin_role)
        # self.flask_app.tables.db_handle.session.commit()

        # self.admin_role_id = self.admin_role.role_id
        
        # self.admin_user = self.flask_app.tables.User(username='test_admin')
        # self.admin_user.crypt_password('test_admin')
        # self.admin_user.roles.append(self.admin_role)
        # self.flask_app.tables.db_handle.session.add(self.admin_user)
        # self.flask_app.tables.db_handle.session.commit()
        self.admin_user_name='test_admin'
        self.admin_user_password='test_admin'
        self.player_pin = self.new_player.pin
        
    def test_user_get(self):        
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                   data=json.dumps({'username':self.admin_user_name,'password':'test_admin'}))            
            rv = c.get('/user')            
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s' % (rv.status_code))
            user = json.loads(rv.data)['data']                        

            self.assertIsNotNone(user)

        
    def test_user_create(self):        
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                   data=json.dumps({'username':self.admin_user_name,'password':'test_admin'}))            
            rv = c.post('/user',
                       data=json.dumps({'username':'test_user','password':'test_user_password'}))            
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s' % (rv.status_code))
            self.assertIsNotNone(self.flask_app.tables.User.query.filter_by(username='test_user').first(),
                                 "Could not find the user we just created")

    def test_user_create_no_username_password(self):        
        with self.flask_app.test_client() as c:            
            rv = c.put('/auth/login',
                   data=json.dumps({'username':self.admin_user_name,'password':'test_admin'}))            
            rv = c.post('/user',
                       data=json.dumps({}))            
            self.assertEquals(rv.status_code,
                              400,
                              'Was expecting status code 400, but it was %s' % (rv.status_code))
            rv = c.put('/auth/login')            
            self.assertEquals(rv.status_code,
                              400,
                              'Was expecting status code 400, but it was %s' % (rv.status_code))

    def test_user_create_duplicate_user(self):        
        with self.flask_app.test_client() as c:            
            rv = c.put('/auth/login',
                   data=json.dumps({'username':self.admin_user_name,'password':'test_admin'}))            
            rv = c.post('/user',
                       data=json.dumps({'username':'test_user','password':'test_user_password'}))            
            rv = c.post('/user',
                       data=json.dumps({'username':'test_user','password':'test_user_password'}))            
            self.assertEquals(rv.status_code,
                              409,
                              'Was expecting status code 409, but it was %s' % (rv.status_code))

            

    def test_user_create_with_roles(self):        
        with self.flask_app.test_client() as c:            
            rv = c.put('/auth/login',
                   data=json.dumps({'username':self.admin_user_name,'password':'test_admin'}))                        
            rv = c.post('/user',
                       data=json.dumps({'username':'test_user','password':'test_user_password',
                                        'roles':[orm_creation.RolesEnum.test.value]}))
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s' % (rv.status_code))
            self.assertIsNotNone(self.flask_app.tables.User.query.filter_by(username='test_user').first(),
                                 "Could not find the user we just created")
            roles = self.flask_app.tables.User.query.filter_by(username='test_user').first().roles            
            self.assertTrue(len(roles) == 1,
                            "Found %s users but expected only 1" % len(roles))
            self.assertTrue(roles[0].name == "test",
                            "Expected role %s but found role %s instead" % ('test',roles[0].name))
            
    def test_user_create_with_bad_roles(self):        
        with self.flask_app.test_client() as c:            
            rv = c.put('/auth/login',
                   data=json.dumps({'username':self.admin_user_name,
                                    'password':'test_admin'}))                        
            rv = c.post('/user',
                       data=json.dumps({'username':'test_user',
                                        'password':'test_user_password',
                                        'roles':[str(55)]}))
            self.assertEquals(rv.status_code,
                              400,
                              'Was expecting status code 400, but it was %s' % (rv.status_code))
            
    def test_user_delete(self):        
        with self.flask_app.test_client() as c:            
            rv = c.put('/auth/login',
                   data=json.dumps({'username':self.admin_user_name,'password':'test_admin'}))
            rv = c.post('/user',
                       data=json.dumps({'username':'test_user','password':'test_user_password'}))                        
            user = json.loads(rv.data)['data']                        
            rv = c.delete('/user/%s' % user['user_id'])            
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s' % (rv.status_code))
            self.assertIsNone(self.flask_app.tables.User.query.filter_by(username='test_user').first(),
                              "Was expecting to find no user, but found user")

    def test_user_delete_on_nonexistant_user(self):        
        with self.flask_app.test_client() as c:            
            rv = c.put('/auth/login',
                   data=json.dumps({'username':self.admin_user_name,'password':'test_admin'}))
            rv = c.post('/user',
                       data=json.dumps({'username':'test_user','password':'test_user_password'}))
            rv = c.delete('/user/%s' % "55")
            self.assertEquals(rv.status_code,
                              400,
                              'Was expecting status code 400, but it was %s' % (rv.status_code))
            self.assertIsNone(self.flask_app.tables.User.query.filter_by(username='test_user_does_not_exist').first(),
                              "Was expecting to find no user, but found user with user_id %s" % 55)
            

    def test_user_edit_username_and_roles_and_haspicture(self):        
        with self.flask_app.test_client() as c:            
            rv = c.put('/auth/login',
                   data=json.dumps({'username':self.admin_user_name,'password':'test_admin'}))
            rv = c.post('/user',
                       data=json.dumps({'username':'test_user_changed','password':'test_user_password',
                                        'roles':[str(orm_creation.RolesEnum.admin.value)]}))
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s' % (rv.status_code))
            new_user = self.flask_app.tables.User.query.filter_by(username='test_user_changed').first()            
            rv = c.put('/user/%s' % new_user.user_id,
                       data=json.dumps({'username':'test_user_changed',
                                        #'roles':{'%s' % self.admin_role_id:False,'%s'%(self.new_role_2_id):True},
                                        'roles':[str(orm_creation.RolesEnum.test.value)],
                                        'has_picture':True}))
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s' % (rv.status_code))            
            self.assertIsNotNone(self.flask_app.tables.User.query.filter_by(username='test_user_changed').first(),
                              "Was expecting to find user, but found no user with user_name test_user_changed")
            changed_user = self.flask_app.tables.User.query.filter_by(username='test_user_changed').first()
            
            self.assertEquals(len(changed_user.roles),1)
            self.assertEquals(changed_user.roles[0].name,"test")
            self.assertEquals(changed_user.has_picture, True)

    def test_user_edit_bad_roles(self):        
        with self.flask_app.test_client() as c:            
            rv = c.put('/auth/login',
                   data=json.dumps({'username':self.admin_user_name,'password':'test_admin'}))
            rv = c.post('/user',
                       data=json.dumps({'username':'test_user_changed','password':'test_user_password',
                                        'roles':[orm_creation.RolesEnum.admin.value]}))
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s' % (rv.status_code))
            new_user = self.flask_app.tables.User.query.filter_by(username='test_user_changed').first()            
            rv = c.put('/user/%s' % new_user.user_id,
                       data=json.dumps({'username':'test_user_changed',
                                        'roles':[str(989)],
                                        'has_picture':True}))
            self.assertEquals(rv.status_code,
                              400,
                              'Was expecting status code 400, but it was %s' % (rv.status_code))

    def test_user_edit_no_username(self):        
        with self.flask_app.test_client() as c:            
            rv = c.put('/auth/login',
                   data=json.dumps({'username':self.admin_user_name,'password':'test_admin'}))
            rv = c.post('/user',
                       data=json.dumps({'username':'test_user_changed','password':'test_user_password',
                                        'roles':[orm_creation.RolesEnum.admin.value]}))
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s' % (rv.status_code))
            new_user = self.flask_app.tables.User.query.filter_by(username='test_user_changed').first()            
            rv = c.put('/user/%s' % new_user.user_id,
                       data=json.dumps({'has_picture':True}))
            self.assertEquals(rv.status_code,
                              400,
                              'Was expecting status code 400, but it was %s' % (rv.status_code))
            
    def test_user_edit_password(self):        
        with self.flask_app.test_client() as c:            
            rv = c.put('/auth/login',
                   data=json.dumps({'username':self.admin_user_name,'password':'test_admin'}))
            rv = c.post('/user',
                       data=json.dumps({'username':'test_user_password_changed','password':'test_new_password',
                                        'roles':[orm_creation.RolesEnum.admin.value]}))
            new_user = self.flask_app.tables.User.query.filter_by(username='test_user_password_changed').first()            
            rv = c.put('/user/%s' % new_user.user_id,
                       data=json.dumps({'username':'test_user_password_changed',
                                         'password':'poop'}))
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s' % (rv.status_code))
            rv = c.put('/auth/login',
                   data=json.dumps({'username':'test_user_password_changed','password':'poop'}))
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s' % (rv.status_code))
            
            
    def test_user_create_bad_auth(self):        
        with self.flask_app.test_client() as c:
            self.checkWrongPermissions(c,'post','/user')            
        with self.flask_app.test_client() as c:
            self.checkWrongPermissions(c,'post','/user','test_scorekeeper')            
        with self.flask_app.test_client() as c:
            self.checkWrongPermissions(c,'post','/user',pin=self.player_pin)            

    def test_user_edit_bad_auth(self):    
        with self.flask_app.test_client() as c:
            self.checkWrongPermissions(c,'put','/user/1')            
        with self.flask_app.test_client() as c:
            self.checkWrongPermissions(c,'put','/user/1','test_scorekeeper')            
        with self.flask_app.test_client() as c:
            self.checkWrongPermissions(c,'put','/user/1',pin=self.player_pin)            


