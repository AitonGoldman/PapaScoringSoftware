import unittest
import os
from mock import MagicMock
import pss_integration_test_base
import json
from flask_login import current_user
from flask import Flask
from lib.PssConfig import PssConfig
from lib import roles_constants
#FIXME : change name of class/file
class RouteEventCreate(pss_integration_test_base.PssIntegrationTestBase):
    def setUp(self):
        super(RouteEventCreate,self).setUp()        
        
    def test_create_event(self):
        new_event_name="newEvent%s"%self.create_uniq_id()
        with self.pss_admin_app.test_client() as c:                        
            rv = c.post('/auth/pss_user/login',
                        data=json.dumps({'username':self.admin_pss_user.username,'password':self.admin_pss_user_password}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.post('/event',
                        data=json.dumps({'name':new_event_name}))
            self.assertHttpCodeEquals(rv,200)            
            new_event = self.pss_admin_app.tables.Events.query.filter_by(name=new_event_name).first()
            self.assertTrue(new_event is not None)            
            self.assertEquals(len(current_user.event_roles),0)
        new_app = self.get_event_app_in_db(new_event_name)
        new_event_users = new_app.tables.EventUsers.query.all()
        user_with_new_permissions = new_app.tables.PssUsers.query.filter_by(username=self.admin_pss_user.username).first()
        self.assertEquals(len(user_with_new_permissions.event_roles),1)
        self.assertEquals(user_with_new_permissions.event_roles[0].name,roles_constants.TOURNAMENT_DIRECTOR)

    def test_create_event_fails_with_non_alpha_event_name(self):
        new_event_name="new_Event_Will_Fail"
        with self.pss_admin_app.test_client() as c:                        
            rv = c.post('/auth/pss_user/login',
                        data=json.dumps({'username':self.admin_pss_user.username,'password':self.admin_pss_user_password}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.post('/event',
                        data=json.dumps({'name':new_event_name}))
            self.assertHttpCodeEquals(rv,400)            
            new_event = self.pss_admin_app.tables.Events.query.filter_by(name=new_event_name).first()
            self.assertTrue(new_event is None)            

    def test_create_duplicate_event_fails(self):
        new_event_name="duplicateEvent%s" % self.create_uniq_id()        
        with self.pss_admin_app.test_client() as c:                        
            rv = c.post('/auth/pss_user/login',
                        data=json.dumps({'username':self.admin_pss_user.username,'password':self.admin_pss_user_password}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.post('/event',
                        data=json.dumps({'name':new_event_name}))
            self.assertHttpCodeEquals(rv,200)
            rv = c.post('/event',
                        data=json.dumps({'name':new_event_name}))
            self.assertHttpCodeEquals(rv,409)                        
            
            
            
