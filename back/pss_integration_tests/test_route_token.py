import unittest
import os
from mock import MagicMock
from pss_integration_tests import pss_integration_test_base
import json

class RouteTokenTest(pss_integration_test_base.PssIntegrationTestBase):
    def setUp(self):        
        super(RouteTokenTest,self).setUp()        
        post_dict = {"players":[{"first_name":"poop_first"+self.create_uniq_id(),"last_name":"poop_last", "ifpa_ranking":123}]} 
        self.admin_login_dict = {'username':self.admin_pss_username,'password':'password'}        
        self.event_id,self.results = self.login_and_create_event_and_create_event_player(self.admin_login_dict, post_dict)                 
        api_key = os.environ['TEST_STRIPE_API_KEY']
        event = self.test_app.table_proxy.get_event_by_event_id(self.event_id)
        event.stripe_api_key=api_key
        self.test_app.table_proxy.commit_changes()
        
    def test_token(self):
        test_tournament_name="test_tournament"+self.create_uniq_id()
        post_dict = {"tournament":{"tournament_name":test_tournament_name}}        
        tournaments_dict = self.login_and_create_tournament(self.admin_login_dict,post_dict,self.event_id)                
        tournament_id=tournaments_dict['data'][0]['tournament_id']

        test_sku = os.environ['TEST_STRIPE_SKU']
        test_discount_sku = os.environ['TEST_STRIPE_DISCOUNT_SKU']

        test_meta_sku = os.environ['TEST_STRIPE_META_SKU']
        test_meta_discount_sku = os.environ['TEST_STRIPE_META_DISCOUNT_SKU']
        
        post_dict={"tournament_id":tournament_id,"use_stripe":True,"stripe_sku":test_sku,"discount_stripe_sku":test_discount_sku,"discount":True,"number_of_tickets_for_discount":2}
        tournament_dict = self.login_and_edit_tournament(self.admin_login_dict,post_dict,self.event_id,tournament_id)         

        post_dict = {"meta_tournament_name":"test_meta_tournament_name"+self.create_uniq_id(),"tournament_ids":[tournament_id]}        
        meta_tournament = self.login_and_create_meta_tournament(self.admin_login_dict,post_dict,self.event_id)        
        meta_tournament_id = meta_tournament['data']["meta_tournament_id"]

        post_dict={"meta_tournament_id":meta_tournament_id,"use_stripe":True,"stripe_sku":test_meta_sku,"discount_stripe_sku":test_meta_discount_sku,"discount":True,"number_of_tickets_for_discount":2}
        self.login_and_edit_meta_tournament(self.admin_login_dict,post_dict,self.event_id,tournament_id)         
        
        player_id=self.results['data'][0]['player_id']
        post_dict={"player_id":player_id,
                   "tournament_token_counts":[{"token_count":1,"tournament_id":tournament_id}],
                   "meta_tournament_token_counts":[{"token_count":1,"meta_tournament_id":meta_tournament['data']['meta_tournament_id']}]}        
        with self.test_app.test_client() as c:
            login_endpoint='/auth/pss_user/login'
            rv = c.post(login_endpoint,
                        data=json.dumps(self.admin_login_dict))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.post('/%s/token' % (self.event_id),
                        data=json.dumps(post_dict))            
        pin = self.results['data'][0]['pin']        
        player_id_for_event = self.results['data'][0]['event_info']['player_id_for_event']
        login_dict = {'player_id_for_event':player_id_for_event,'player_pin':pin}        
        post_dict={"tournament_token_counts":[{"token_count":1,"tournament_id":tournament_id}],
                   "meta_tournament_token_counts":[{"token_count":1,"meta_tournament_id":meta_tournament['data']['meta_tournament_id']}]}
        
        with self.test_app.test_client() as c:
            rv = c.post('/auth/player/login/%s'%self.event_id,
                        data=json.dumps(login_dict))
            self.assertHttpCodeEquals(rv,200)
            rv = c.post('/%s/token' % (self.event_id),
                        data=json.dumps(post_dict))
            self.assertHttpCodeEquals(rv,200)
            token_purchase_id=json.loads(rv.data)['new_token_purchase']['token_purchase_id']            
            rv = c.put('/%s/token/%s' % (self.event_id,token_purchase_id),
                        data=json.dumps({"email":"test@test.com"}))
            self.assertHttpCodeEquals(rv,200)
        
        #print tournaments_dict['data'][0]['tournament_id']        
