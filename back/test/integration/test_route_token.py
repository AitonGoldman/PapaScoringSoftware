import datetime
import unittest
import os
from mock import MagicMock
import pss_integration_test_existing_tournament_and_metatournament
import json
from flask_login import current_user
from lib import roles_constants
from sqlalchemy.orm import joinedload


class RouteTokenTest(pss_integration_test_existing_tournament_and_metatournament.PssIntegrationTestExistingTournamentAndMetaTournament):
    def setUp(self):
        super(RouteTokenTest,self).setUp()                        
    def test_create_token(self):        
        with self.event_app.test_client() as c:                        
            tables = self.event_app.tables
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.standard_td_username,
                                         'password':self.generic_password}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.post('/token/player_id/%s' % self.player_id_with_no_tokens,
                        data=json.dumps({'tournament_token_counts':[{'tournament_id':1,'token_count':2}],'meta_tournament_token_counts':[{'meta_tournament_id':1,'token_count':2}]}))

            self.assertHttpCodeEquals(rv,200)            
            results = json.loads(rv.data)
            self.assertTrue('new_token_purchase' in results)
            self.assertTrue('purchase_summary' in results)            
            self.assertEquals(len(results['purchase_summary']),2)
            self.assertTrue('total_cost' in results)
            self.assertEquals(results['total_cost'],60)
            new_token_purchase = tables.TokenPurchases.query.filter_by(token_purchase_id=results['new_token_purchase']['token_purchase_id']).first()
            for token in new_token_purchase.tokens:
                self.assertTrue(token.paid_for)
            self.assertEquals(4,len(new_token_purchase.tokens))
            #FIXME : check actual databse results
            
    def test_create_token_with_discount(self):        
        with self.event_app.test_client() as c:                        
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.standard_td_username,
                                         'password':self.generic_password}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.post('/token/player_id/%s' % self.player_id_with_no_tokens,
                        data=json.dumps({'tournament_token_counts':[{'tournament_id':4,'token_count':2}],'meta_tournament_token_counts':[]}))
            self.assertHttpCodeEquals(rv,200)            
            results = json.loads(rv.data)            
            self.assertEquals(results['total_cost'],30)

            rv = c.post('/token/player_id/%s' % self.player_id_with_no_tokens,
                        data=json.dumps({'tournament_token_counts':[{'tournament_id':4,'token_count':3}],'meta_tournament_token_counts':[]}))
            self.assertHttpCodeEquals(rv,200)            
            results = json.loads(rv.data)            
            self.assertEquals(results['total_cost'],40)

            rv = c.post('/token/player_id/%s' % self.player_id_with_no_tokens,
                        data=json.dumps({'tournament_token_counts':[{'tournament_id':4,'token_count':4}],'meta_tournament_token_counts':[]}))
            self.assertHttpCodeEquals(rv,200)            
            results = json.loads(rv.data)            
            self.assertEquals(results['total_cost'],55)
            # FIXME : test discounts on metatournaments - depends on edit metatournament existing

    def test_create_token_by_player(self):        
        with self.event_app.test_client() as c:
            tables = self.event_app.tables
            rv = c.post('/auth/player/login',
                        data=json.dumps({'event_player_number':self.player_event_id_with_no_tokens,'event_player_pin':self.player_event_pin_with_no_tokens}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.post('/token',
                        data=json.dumps({'tournament_token_counts':[{'tournament_id':4,'token_count':2}],'meta_tournament_token_counts':[]}))
            self.assertHttpCodeEquals(rv,200)            
            results = json.loads(rv.data)            
            self.assertEquals(results['total_cost'],30)
            new_token_purchase = tables.TokenPurchases.query.filter_by(token_purchase_id=results['new_token_purchase']['token_purchase_id']).first()
            for token in new_token_purchase.tokens:
                self.assertFalse(token.paid_for)
                
    def test_create_token_with_wrong_permissions_fails(self):        
        with self.event_app.test_client() as c:
            tables = self.event_app.tables
            rv = c.post('/auth/player/login',
                        data=json.dumps({'event_player_number':self.player_event_id_with_no_tokens,'event_player_pin':self.player_event_pin_with_no_tokens}))

            self.assertHttpCodeEquals(rv,200)            
            rv = c.post('/token/player_id/1',
                        data=json.dumps({'tournament_token_counts':[{'tournament_id':1,'token_count':2}],'meta_tournament_token_counts':[{'meta_tournament_id':1,'token_count':2}]}))

            self.assertHttpCodeEquals(rv,403)            

        with self.event_app.test_client() as c:                        
            tables = self.event_app.tables
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.standard_td_username,
                                         'password':self.generic_password}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.post('/token',
                        data=json.dumps({'tournament_token_counts':[{'tournament_id':4,'token_count':2}],'meta_tournament_token_counts':[]}))
            self.assertHttpCodeEquals(rv,403)
            
        with self.event_app.test_client() as c:                        
            tables = self.event_app.tables
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.standard_scorekeeper_username,
                                         'password':self.generic_password}))
            self.assertHttpCodeEquals(rv,200)                                    
            rv = c.post('/token',
                        data=json.dumps({'tournament_token_counts':[{'tournament_id':4,'token_count':2}],'meta_tournament_token_counts':[]}))
            self.assertHttpCodeEquals(rv,403)

            rv = c.post('/token/player_id/1',
                        data=json.dumps({'tournament_token_counts':[{'tournament_id':1,'token_count':2}],'meta_tournament_token_counts':[{'meta_tournament_id':1,'token_count':2}]}))

            self.assertHttpCodeEquals(rv,403)            

    def test_create_token_fails_when_limits_exceeded(self):        
        with self.event_app.test_client() as c:                        
            tables = self.event_app.tables
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.standard_td_username,
                                         'password':self.generic_password}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.post('/token/player_id/%s' % self.player_id_with_no_tokens,
                        data=json.dumps({'tournament_token_counts':[{'tournament_id':1,'token_count':16}],'meta_tournament_token_counts':[{'meta_tournament_id':1,'token_count':2}]}))

            self.assertHttpCodeEquals(rv,400)            
            self.assertEquals(json.loads(rv.data)['message'],'Fuck off, Ass Wipe')

            rv = c.post('/token/player_id/%s' % self.player_id_with_no_tokens,
                        data=json.dumps({'tournament_token_counts':[{'tournament_id':1,'token_count':14}],'meta_tournament_token_counts':[{'meta_tournament_id':1,'token_count':2}]}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.post('/token/player_id/%s' % self.player_id_with_no_tokens,
                        data=json.dumps({'tournament_token_counts':[{'tournament_id':1,'token_count':2}],'meta_tournament_token_counts':[{'meta_tournament_id':1,'token_count':2}]}))
            self.assertHttpCodeEquals(rv,400)            
            self.assertEquals(json.loads(rv.data)['message'],'Fuck off, Ass Wipe')
            
    def test_create_token_for_team(self):        
        new_player_first_name_1='%s' % self.create_uniq_id()
        new_player_first_name_2='%s' % self.create_uniq_id()
        
        player_1 = self.create_player_for_test(self.event_app,
                                               first_name=new_player_first_name_1,
                                               last_name='new_last_name',
                                               ifpa_ranking=9999)
        player_2 = self.create_player_for_test(self.event_app,
                                               first_name=new_player_first_name_2,
                                               last_name='new_last_name',
                                               ifpa_ranking=9999)
        player_1_id=player_1['player_id']
        player_2_id=player_2['player_id']

        team_id = self.createTeamAndAddPlayers('team_test%s'% self.create_uniq_id(),player_1_id,player_2_id,self.event_app)
        
        with self.event_app.test_client() as c:                        
            tables = self.event_app.tables
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.standard_td_username,
                                         'password':self.generic_password}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.post('/token/player_id/%s' % player_1_id,
                        data=json.dumps({'tournament_token_counts':[{'tournament_id':5,'token_count':2}],'meta_tournament_token_counts':[{'meta_tournament_id':1,'token_count':2}]}))

            self.assertHttpCodeEquals(rv,200)            
            results = json.loads(rv.data)            
            team_token_results = [summary for summary in results['purchase_summary'] if summary[0]=='newTeamTournament']
            self.assertEquals(len(team_token_results),1)
            rv = c.get('/token/player_id/%s' % player_2_id)
            results = json.loads(rv.data)            
            player_2_team_token_results = [summary for summary in results['tournament_token_count'] if summary['tournament_name']=='newTeamTournament']
            self.assertEquals(len(player_2_team_token_results),1)

            rv = c.post('/token/player_id/%s' % player_2_id,
                        data=json.dumps({'tournament_token_counts':[{'tournament_id':5,'token_count':14}],'meta_tournament_token_counts':[{'meta_tournament_id':1,'token_count':2}]}))

            self.assertHttpCodeEquals(rv,400)            
            results = json.loads(rv.data)            
            self.assertEquals(results['message'],'Fuck off, Ass Wipe')
            
            
            
            
    # test bad input
    
        
