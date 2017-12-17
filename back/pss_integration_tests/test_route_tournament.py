import unittest
import os
from mock import MagicMock
from pss_integration_tests import pss_integration_test_base
import json

class RouteTournamentTest(pss_integration_test_base.PssIntegrationTestBase):
    def setUp(self):
        super(RouteTournamentTest,self).setUp()        
        self.post_dict = {"event_role_ids":[self.td_event_role_id],"event_users":[{"first_name":"poop_firsta"+self.create_uniq_id(),"last_name":"poop_lasta","password":"password"}]}
        self.admin_login_dict = {'username':self.admin_pss_username,'password':'password'}        
        self.event_id,self.results = self.login_and_create_event_and_create_event_user(self.admin_login_dict, self.post_dict)
        
        
    def test_tournament_create_with_event_creator(self):        
        test_tournament_name="test_tournament"+self.create_uniq_id()
        post_dict = {"tournament":{"tournament_name":test_tournament_name}}
        self.post_dict['event_users'][0]['first_name']=self.create_uniq_id()
        tournaments_dict = self.login_and_create_tournament(self.admin_login_dict,post_dict,self.event_id)        
        self.assertEquals(tournaments_dict['data'][0]['tournament_name'],test_tournament_name)
        
    def test_tournament_create_with_tournament_director(self):        
        test_tournament_name="test_tournament"+self.create_uniq_id()
        post_dict = {"tournament":{"tournament_name":test_tournament_name}}         
        login_dict = {'username':self.results['data'][0]['username'],'password':'password'}        
        tournaments_dict = self.login_and_create_tournament(login_dict,post_dict,self.event_id,True)        
        self.assertEquals(tournaments_dict['data'][0]['tournament_name'],test_tournament_name)
        
        
    def test_tournament_create_fails_with_wrong_event_creator(self):                
        username="test_admin_user"+self.create_uniq_id()
        self.test_app.table_proxy.create_user(username,
                                              'test_first_2',
                                              'test_last_2',
                                              'password',
                                              event_creator=True,
                                              commit=True)

        login_dict = {'username':username,'password':'password'}
        with self.test_app.test_client() as c:            
            rv = c.post('/auth/pss_user/login',
                        data=json.dumps(login_dict))
            self.assertHttpCodeEquals(rv,200)            
            test_tournament_name="test_tournament"+self.create_uniq_id()
            post_dict = {"tournament":{"tournament_name":test_tournament_name}}         
            rv = c.post('/%s/tournament' % self.event_id,
                        data=json.dumps(post_dict))
            self.assertHttpCodeEquals(rv,401,'You are not authorized to create tournaments for this event')
            

    def test_tournament_create_fails_with_scorekeeper(self):                
        #FIXME : need to handle scorekeeper creation in setup()
        post_dict = {"event_role_ids":[self.scorekeeper_role_id],"event_users":[{"first_name":"poop_firsta"+self.create_uniq_id(),"last_name":"poop_lasta","password":"password"}]}
        login_dict = {'username':self.admin_pss_username,'password':'password'}
        
        event_id,results = self.login_and_create_event_and_create_event_user(login_dict, post_dict)
        test_tournament_name="test_tournament"+self.create_uniq_id()
        post_dict = {"tournament":{"tournament_name":test_tournament_name}}                 
        login_dict = {'username':results['data'][0]['username'],'password':'password'}        
        with self.test_app.test_client() as c:
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps(login_dict))
            self.assertHttpCodeEquals(rv,200)        
            rv = c.post('/%s/tournament' % event_id,
                        data=json.dumps(post_dict))
            self.assertHttpCodeEquals(rv,401,'You are not authorized to create tournaments for this event')                        
            

    def test_tournament_edit_with_event_creator(self):        
        test_tournament_name="test_tournament"+self.create_uniq_id()
        post_dict = {"tournament":{"tournament_name":test_tournament_name}}        
        tournaments_dict = self.login_and_create_tournament(self.admin_login_dict,post_dict,self.event_id)        
        tournament_id=tournaments_dict['data'][0]['tournament_id']
        post_dict={"tournament_id":tournament_id,"tournament_name":"new_tournament_name"}
        tournament_dict = self.login_and_edit_tournament(self.admin_login_dict,post_dict,self.event_id,tournament_id)
        self.assertTrue(tournament_dict['data']['stripe_price'] is None)
        self.assertTrue(tournament_dict['data']['discount_stripe_price'] is None)

    def test_tournament_edit_with_tournament_director(self):        
        test_tournament_name="test_tournament"+self.create_uniq_id()
        post_dict = {"tournament":{"tournament_name":test_tournament_name}}        
        tournaments_dict = self.login_and_create_tournament(self.admin_login_dict,post_dict,self.event_id)        
        tournament_id=tournaments_dict['data'][0]['tournament_id']
        post_dict={"tournament_id":tournament_id,"tournament_name":"new_tournament_name"}
        login_dict = {'username':self.results['data'][0]['username'],'password':'password'}                
        tournament_dict = self.login_and_edit_tournament(login_dict,post_dict,self.event_id,tournament_id,True)

    def test_tournament_edit_fails_with_scorekeeper(self):        
        post_dict = {"event_role_ids":[self.scorekeeper_role_id],"event_users":[{"first_name":"poop_firsta"+self.create_uniq_id(),"last_name":"poop_lasta","password":"password"}]}
        login_dict = {'username':self.admin_pss_username,'password':'password'}
        
        event_id,results = self.login_and_create_event_and_create_event_user(login_dict, post_dict)
        test_tournament_name="test_tournament"+self.create_uniq_id()
        post_dict = {"tournament":{"tournament_name":test_tournament_name}}        
        tournaments_dict = self.login_and_create_tournament(login_dict,post_dict, event_id)        
        tournament_id=tournaments_dict['data'][0]['tournament_id']
        post_dict={"tournament_id":tournament_id,"tournament_name":"new_tournament_name"}
        login_dict = {'username':results['data'][0]['username'],'password':'password'}                
        with self.test_app.test_client() as c:                
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps(login_dict))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.put('/%s/tournament' % (event_id),
                        data=json.dumps(post_dict))
            self.assertHttpCodeEquals(rv,401,'You are not authorized to edit tournaments for this event')
            return json.loads(rv.data)

    def test_tournament_edit_stripe(self):        
        api_key = os.environ['TEST_STRIPE_API_KEY']
        test_sku = os.environ['TEST_STRIPE_SKU']
        test_discount_sku = os.environ['TEST_STRIPE_DISCOUNT_SKU']
        event = self.test_app.table_proxy.get_event_by_event_id(self.event_id)
        event.stripe_api_key=api_key
        self.test_app.table_proxy.commit_changes()
        test_tournament_name="test_tournament"+self.create_uniq_id()
        post_dict = {"tournament":{"tournament_name":test_tournament_name}}        
        tournaments_dict = self.login_and_create_tournament(self.admin_login_dict,post_dict,self.event_id)        
        tournament_id=tournaments_dict['data'][0]['tournament_id']
        post_dict={"tournament_id":tournament_id,"use_stripe":True,"stripe_sku":test_sku,"discount_stripe_sku":test_discount_sku}
        tournament_dict = self.login_and_edit_tournament(self.admin_login_dict,post_dict,self.event_id,tournament_id)
        self.assertTrue(tournament_dict['data']['stripe_price'] is not None)
        self.assertTrue(tournament_dict['data']['discount_stripe_price'] is not None)
