import unittest
import os
from mock import MagicMock
from pss_integration_tests import pss_integration_test_base
import json

class RoutePssUserTest(pss_integration_test_base.PssIntegrationTestBase):
    def setUp(self):
        super(RoutePssUserTest,self).setUp()        
        
    def test_event_user_create_with_event_creator(self):        
        post_dict = {"event_role_ids":[self.td_event_role_id],"event_users":[{"first_name":"poop_first","last_name":"poop_last"}]}
        login_dict = {'username':self.admin_pss_username,'password':'password'}
        
        event_id,results = self.login_and_create_event_and_create_event_user(login_dict, post_dict)
        self.assertTrue(len(results['data'])==1)
        self.assertTrue(results['data'][0]['pss_user_id'] is not None)
        new_pss_user_id=int(results['data'][0]['pss_user_id'])
        pss_user_in_db = self.test_app.table_proxy.PssUsers.query.filter_by(pss_user_id=new_pss_user_id).first()        

        self.assertTrue(pss_user_in_db is not None)
        self.assertEquals(pss_user_in_db.event_roles[0].event_role_id,1)

    def test_event_user_create_with_tournament_director(self):        
        post_dict = {"event_role_ids":[self.td_event_role_id],"event_users":[{"first_name":"poop_first","last_name":"poop_last","password":"password"}]}
        login_dict = {'username':self.admin_pss_username,'password':'password'}
        
        event_id,results = self.login_and_create_event_and_create_event_user(login_dict, post_dict)
        login_dict = {'username':results['data'][0]['username'],'password':'password'}        
        with self.test_app.test_client() as c:
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps(login_dict))
            self.assertHttpCodeEquals(rv,200)        
            rv = c.post('/%s/event_user' % event_id,
                        data=json.dumps(post_dict))
            self.assertHttpCodeEquals(rv,200)        
            new_pss_user_id=int(results['data'][0]['pss_user_id'])
            pss_user_in_db = self.test_app.table_proxy.PssUsers.query.filter_by(pss_user_id=new_pss_user_id).first()        

            self.assertTrue(pss_user_in_db is not None)
            self.assertEquals(pss_user_in_db.event_roles[0].event_role_id,1)


        
    def test_event_user_create_fails_with_wrong_event_creator(self):                
        self.test_app.table_proxy.create_user(self.admin_pss_username+"2",
                                              'test_first_2',
                                              'test_last_2',
                                              'password',
                                              event_creator=True,
                                              commit=True)

        post_dict = {"event_role_ids":[self.td_event_role_id],"event_users":[{"first_name":"poop_first","last_name":"poop_last"}]}
        login_dict = {'username':self.admin_pss_username,'password':'password'}        
        event_id,results = self.login_and_create_event_and_create_event_user(login_dict, post_dict)
        login_dict = {'username':self.admin_pss_username+'2','password':'password'}
        with self.test_app.test_client() as c:
            rv = c.post('/auth/pss_user/login',
                        data=json.dumps(login_dict))
            self.assertHttpCodeEquals(rv,200)        
            rv = c.post('/%s/event_user' % event_id,
                        data=json.dumps(post_dict))
            self.assertHttpCodeEquals(rv,401,"You are not authorized to register users for this event")

    def test_event_user_create_fails_with_scorekeeper(self):                
        post_dict = {"event_role_ids":[self.scorekeeper_role_id],"event_users":[{"first_name":"poop_first","last_name":"poop_last","password":"password"}]}
        login_dict = {'username':self.admin_pss_username,'password':'password'}        
        event_id,results = self.login_and_create_event_and_create_event_user(login_dict, post_dict)
        login_dict = {'username':results['data'][0]['username'],'password':'password'}        
        with self.test_app.test_client() as c:
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps(login_dict))
            self.assertHttpCodeEquals(rv,200)        
            rv = c.post('/%s/event_user' % event_id,
                        data=json.dumps(post_dict))
            self.assertHttpCodeEquals(rv,401,"You are not authorized to register users for this event")
            

    def test_event_user_edit_change_role(self):
        post_dict = {"event_role_ids":[self.td_event_role_id],"event_users":[{"first_name":"poop_first","last_name":"poop_last","password":"password"}]}
        login_dict = {'username':self.admin_pss_username,'password':'password'}
        
        event_id,results = self.login_and_create_event_and_create_event_user(login_dict, post_dict)        
        post_dict = {"event_user":{"pss_user_id":results['data'][0]['pss_user_id']},"event_role_ids":[self.scorekeeper_role_id]}

        with self.test_app.test_client() as c:
            rv = c.post('/auth/pss_user/login',
                        data=json.dumps(login_dict))
            self.assertHttpCodeEquals(rv,200)        
            rv = c.put('/%s/event_role_mapping' % event_id,
                        data=json.dumps(post_dict))
            self.assertHttpCodeEquals(rv,200)        
            
            pss_user_in_db = self.test_app.table_proxy.PssUsers.query.filter_by(pss_user_id=results['data'][0]['pss_user_id']).first()                                
            results = json.loads(rv.data)
            self.assertEquals(pss_user_in_db.event_roles[0].event_role_id,self.scorekeeper_role_id)            
            self.assertEquals(len(pss_user_in_db.event_roles),1)            


