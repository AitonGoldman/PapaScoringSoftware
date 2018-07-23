import datetime
import unittest
import os
from mock import MagicMock
import pss_integration_test_existing_tournament_and_metatournament
import json
from flask_login import current_user
from lib import roles_constants
from sqlalchemy.orm import joinedload


class RouteQueueTest(pss_integration_test_existing_tournament_and_metatournament.PssIntegrationTestExistingTournamentAndMetaTournament):
    def setUp(self):
        super(RouteQueueTest,self).setUp()
        self.tournament_machine = self.createTournamentMachine()
        

    def generate_player_with_no_tokens(self,app):
        player_name_with_no_tokens = 'player_with_no_tokens_%s' % self.create_uniq_id()
        return self.create_player_for_test(app,first_name=player_name_with_no_tokens,last_name='test_player_last_name')
        
    def bootstrap_queue(self,tables,tournament_machine):
        first_queue_slot = tables.Queues.query.filter_by(tournament_machine_id=tournament_machine['tournament_machine_id'],position=1).first()
        first_queue_slot.player_id=1
        tables.db_handle.session.commit()            
        
    def test_add_player_to_queue(self):
        with self.event_app.test_client() as c:                        
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.standard_td_username,
                                         'password':self.generic_password}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.post('/token/player_id/%s' % self.player_id_with_no_tokens,
                        data=json.dumps({'tournament_token_counts':[{'tournament_id':1,'token_count':2}],'meta_tournament_token_counts':[]}))
            self.assertHttpCodeEquals(rv,200)                    
        with self.event_app.test_client() as c:                        
            tables = self.event_app.tables
            self.bootstrap_queue(tables,self.tournament_machine)
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.standard_scorekeeper_username,
                                         'password':self.generic_password}))
            self.assertHttpCodeEquals(rv,200)                        
            rv = c.post('/queue/tournament_machine/%s' % self.tournament_machine['tournament_machine_id'],
                        data=json.dumps({'action':'add','player_id':self.player_id_with_no_tokens}))
            self.assertHttpCodeEquals(rv,200)            
            second_queue_slot = tables.Queues.query.filter_by(tournament_machine_id=self.tournament_machine['tournament_machine_id'],position=2).first()
            self.assertEquals(second_queue_slot.player_id,self.player_id_with_no_tokens)

    def test_add_player_to_queue_when_already_in_another_queue(self):
        with self.event_app.test_client() as c:                        
            self.tournament_machine_2 = self.createTournamentMachine()
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.standard_td_username,
                                         'password':self.generic_password}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.post('/token/player_id/%s' % self.player_id_with_no_tokens,
                        data=json.dumps({'tournament_token_counts':[{'tournament_id':1,'token_count':2}],'meta_tournament_token_counts':[]}))
            self.assertHttpCodeEquals(rv,200)                    
        with self.event_app.test_client() as c:                        
            tables = self.event_app.tables
            self.bootstrap_queue(tables,self.tournament_machine)
            self.bootstrap_queue(tables,self.tournament_machine_2)                        
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.standard_scorekeeper_username,
                                         'password':self.generic_password}))
            self.assertHttpCodeEquals(rv,200)                        
            rv = c.post('/queue/tournament_machine/%s' % self.tournament_machine['tournament_machine_id'],
                        data=json.dumps({'action':'add','player_id':self.player_id_with_no_tokens}))
            self.assertHttpCodeEquals(rv,200)
            rv = c.post('/queue/tournament_machine/%s' % self.tournament_machine_2['tournament_machine_id'],
                        data=json.dumps({'action':'add','player_id':self.player_id_with_no_tokens}))
            self.assertHttpCodeEquals(rv,200)                        
            second_queue_slot = tables.Queues.query.filter_by(tournament_machine_id=self.tournament_machine_2['tournament_machine_id'],position=2).first()
            self.assertEquals(second_queue_slot.player_id,self.player_id_with_no_tokens)
            
            
    def test_add_player_to_queue_with_player_login(self):
        with self.event_app.test_client() as c:                        
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.standard_td_username,
                                         'password':self.generic_password}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.post('/token/player_id/%s' % self.player_id_with_no_tokens,
                        data=json.dumps({'tournament_token_counts':[{'tournament_id':1,'token_count':2}],'meta_tournament_token_counts':[]}))
            self.assertHttpCodeEquals(rv,200)            
        with self.event_app.test_client() as c:                        
            tables = self.event_app.tables
            self.bootstrap_queue(tables,self.tournament_machine)            

            rv = c.post('/auth/player/login',
                        data=json.dumps({'event_player_number':self.player_event_id_with_no_tokens,'event_player_pin':self.player_event_pin_with_no_tokens}))
            self.assertHttpCodeEquals(rv,200)            

            rv = c.post('/queue/tournament_machine/%s' % self.tournament_machine['tournament_machine_id'],
                        data=json.dumps({'action':'add'}))
            self.assertHttpCodeEquals(rv,200)            
            second_queue_slot = tables.Queues.query.filter_by(tournament_machine_id=self.tournament_machine['tournament_machine_id'],position=2).first()
            self.assertEquals(second_queue_slot.player_id,self.player_id_with_no_tokens)

    def test_add_player_to_queue_fails_with_no_login(self):
        with self.event_app.test_client() as c:                        
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.standard_td_username,
                                         'password':self.generic_password}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.post('/token/player_id/%s' % self.player_id_with_no_tokens,
                        data=json.dumps({'tournament_token_counts':[{'tournament_id':1,'token_count':2}],'meta_tournament_token_counts':[]}))
            self.assertHttpCodeEquals(rv,200)                    
        with self.event_app.test_client() as c:                        
            tables = self.event_app.tables            
            rv = c.post('/queue/tournament_machine/%s' % self.tournament_machine['tournament_machine_id'],
                        data=json.dumps({'action':'add','player_id':self.player_id_with_no_tokens}))
            self.assertHttpCodeEquals(rv,403,'Permission denied')            
            
            
    def test_add_player_to_queue_fails_with_empty_queue(self):
        with self.event_app.test_client() as c:                        
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.standard_td_username,
                                         'password':self.generic_password}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.post('/token/player_id/%s' % self.player_id_with_no_tokens,
                        data=json.dumps({'tournament_token_counts':[{'tournament_id':1,'token_count':2}],'meta_tournament_token_counts':[]}))
            self.assertHttpCodeEquals(rv,200)                    
        with self.event_app.test_client() as c:                        
            tables = self.event_app.tables            
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.standard_scorekeeper_username,
                                         'password':self.generic_password}))
            self.assertHttpCodeEquals(rv,200)                        
            rv = c.post('/queue/tournament_machine/%s' % self.tournament_machine['tournament_machine_id'],
                        data=json.dumps({'action':'add','player_id':self.player_id_with_no_tokens}))
            self.assertHttpCodeEquals(rv,400)            
                        

    def test_add_player_to_queue_fails_with_full_queue(self):
        with self.event_app.test_client() as c:                        
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.standard_td_username,
                                         'password':self.generic_password}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.post('/token/player_id/%s' % self.player_id_with_no_tokens,
                        data=json.dumps({'tournament_token_counts':[{'tournament_id':1,'token_count':2}],'meta_tournament_token_counts':[]}))
            self.assertHttpCodeEquals(rv,200)
            player_2_id_with_no_tokens=self.generate_player_with_no_tokens(self.event_app)['player_id']
            rv = c.post('/token/player_id/%s' % player_2_id_with_no_tokens,
                        data=json.dumps({'tournament_token_counts':[{'tournament_id':1,'token_count':2}],'meta_tournament_token_counts':[]}))
            self.assertHttpCodeEquals(rv,200)            
            player_3_id_with_no_tokens=self.generate_player_with_no_tokens(self.event_app)['player_id']
            rv = c.post('/token/player_id/%s' % player_3_id_with_no_tokens,
                        data=json.dumps({'tournament_token_counts':[{'tournament_id':1,'token_count':2}],'meta_tournament_token_counts':[]}))
            self.assertHttpCodeEquals(rv,200)            

        with self.event_app.test_client() as c:                        
            tables = self.event_app.tables            
            self.bootstrap_queue(tables,self.tournament_machine)
            
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.standard_scorekeeper_username,
                                         'password':self.generic_password}))
            self.assertHttpCodeEquals(rv,200)                        
            rv = c.post('/queue/tournament_machine/%s' % self.tournament_machine['tournament_machine_id'],
                        data=json.dumps({'action':'add','player_id':self.player_id_with_no_tokens}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.post('/queue/tournament_machine/%s' % self.tournament_machine['tournament_machine_id'],
                        data=json.dumps({'action':'add','player_id':player_2_id_with_no_tokens}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.post('/queue/tournament_machine/%s' % self.tournament_machine['tournament_machine_id'],
                        data=json.dumps({'action':'add','player_id':player_3_id_with_no_tokens}))
            self.assertHttpCodeEquals(rv,400,'no room left in queue')                                    

    def test_add_player_to_queue_fails_with_no_tokens(self):
        with self.event_app.test_client() as c:                        
            tables = self.event_app.tables
            self.bootstrap_queue(tables,self.tournament_machine)
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.standard_scorekeeper_username,
                                         'password':self.generic_password}))
            self.assertHttpCodeEquals(rv,200)                        
            rv = c.post('/queue/tournament_machine/%s' % self.tournament_machine['tournament_machine_id'],
                        data=json.dumps({'action':'add','player_id':self.player_id_with_no_tokens}))
            self.assertHttpCodeEquals(rv,400,'Player has no tokens')             
            
    def test_remove_player_from_queue(self):
        player_2_id_with_no_tokens=self.generate_player_with_no_tokens(self.event_app)['player_id']
        with self.event_app.test_client() as c:                        
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.standard_td_username,
                                         'password':self.generic_password}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.post('/token/player_id/%s' % self.player_id_with_no_tokens,
                        data=json.dumps({'tournament_token_counts':[{'tournament_id':1,'token_count':2}],'meta_tournament_token_counts':[]}))
            self.assertHttpCodeEquals(rv,200)
            rv = c.post('/token/player_id/%s' % player_2_id_with_no_tokens,
                        data=json.dumps({'tournament_token_counts':[{'tournament_id':1,'token_count':2}],'meta_tournament_token_counts':[]}))
            self.assertHttpCodeEquals(rv,200)                    
            
        with self.event_app.test_client() as c:                        
            tables = self.event_app.tables
            self.bootstrap_queue(tables,self.tournament_machine)
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.standard_scorekeeper_username,
                                         'password':self.generic_password}))
            self.assertHttpCodeEquals(rv,200)                        
            rv = c.post('/queue/tournament_machine/%s' % self.tournament_machine['tournament_machine_id'],
                        data=json.dumps({'action':'add','player_id':self.player_id_with_no_tokens}))
            self.assertHttpCodeEquals(rv,200)
            rv = c.post('/queue/tournament_machine/%s' % self.tournament_machine['tournament_machine_id'],
                        data=json.dumps({'action':'add','player_id':player_2_id_with_no_tokens}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.delete('/queue/tournament_machine/%s' % self.tournament_machine['tournament_machine_id'],
                        data=json.dumps({'action':'remove','player_id':self.player_id_with_no_tokens}))
            self.assertHttpCodeEquals(rv,200)                        
            second_queue_slot = tables.Queues.query.filter_by(tournament_machine_id=self.tournament_machine['tournament_machine_id'],position=2).first()
            self.assertEquals(second_queue_slot.player_id,player_2_id_with_no_tokens)
            third_queue_slot = tables.Queues.query.filter_by(tournament_machine_id=self.tournament_machine['tournament_machine_id'],position=3).first()
            self.assertEquals(third_queue_slot.player_id,None)        

    def test_remove_player_with_player_login(self):
        with self.event_app.test_client() as c:                        
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.standard_td_username,
                                         'password':self.generic_password}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.post('/token/player_id/%s' % self.player_id_with_no_tokens,
                        data=json.dumps({'tournament_token_counts':[{'tournament_id':1,'token_count':2}],'meta_tournament_token_counts':[]}))
            self.assertHttpCodeEquals(rv,200)            
        with self.event_app.test_client() as c:                        
            tables = self.event_app.tables
            self.bootstrap_queue(tables,self.tournament_machine)            

            rv = c.post('/auth/player/login',
                        data=json.dumps({'event_player_number':self.player_event_id_with_no_tokens,'event_player_pin':self.player_event_pin_with_no_tokens}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.post('/queue/tournament_machine/%s' % self.tournament_machine['tournament_machine_id'],
                        data=json.dumps({'action':'add'}))
            second_queue_slot = tables.Queues.query.filter_by(tournament_machine_id=self.tournament_machine['tournament_machine_id'],position=2).first()
            self.assertEquals(second_queue_slot.player_id,self.player_id_with_no_tokens)            
            rv = c.delete('/queue/tournament_machine/%s' % self.tournament_machine['tournament_machine_id'],
                        data=json.dumps({'action':'remove','player_id':1}))
            self.assertHttpCodeEquals(rv,200)            
            second_queue_slot = tables.Queues.query.filter_by(tournament_machine_id=self.tournament_machine['tournament_machine_id'],position=2).first()
            self.assertEquals(second_queue_slot.player_id,None)

    def test_bump_player_down_queue(self):
        with self.event_app.test_client() as c:                        
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.standard_td_username,
                                         'password':self.generic_password}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.post('/token/player_id/%s' % self.player_id_with_no_tokens,
                        data=json.dumps({'tournament_token_counts':[{'tournament_id':1,'token_count':2}],'meta_tournament_token_counts':[]}))
            self.assertHttpCodeEquals(rv,200)            
        with self.event_app.test_client() as c:                        
            tables = self.event_app.tables
            self.bootstrap_queue(tables,self.tournament_machine)            

            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.standard_scorekeeper_username,
                                         'password':self.generic_password}))
            self.assertHttpCodeEquals(rv,200)                        
            rv = c.post('/queue/tournament_machine/%s' % self.tournament_machine['tournament_machine_id'],
                        data=json.dumps({'action':'add','player_id':self.player_id_with_no_tokens}))                        

            #FIXME : don't hardcode player id 1 here - i.e. do proper bootstrapping of queue            
            rv = c.put('/queue/tournament_machine/%s' % self.tournament_machine['tournament_machine_id'],
                        data=json.dumps({'action':'bump','player_id':1}))
            self.assertHttpCodeEquals(rv,200)            
            second_queue_slot = tables.Queues.query.filter_by(tournament_machine_id=self.tournament_machine['tournament_machine_id'],position=2).first()
            first_queue_slot = tables.Queues.query.filter_by(tournament_machine_id=self.tournament_machine['tournament_machine_id'],position=1).first()            
            self.assertEquals(first_queue_slot.player_id,self.player_id_with_no_tokens)
            self.assertFalse(first_queue_slot.bumped)
            self.assertEquals(second_queue_slot.player_id,1)
            self.assertTrue(second_queue_slot.bumped)

            rv = c.put('/queue/tournament_machine/%s' % self.tournament_machine['tournament_machine_id'],
                        data=json.dumps({'action':'bump','player_id':self.player_id_with_no_tokens}))
            self.assertHttpCodeEquals(rv,200)            
            second_queue_slot = tables.Queues.query.filter_by(tournament_machine_id=self.tournament_machine['tournament_machine_id'],position=2).first()
            first_queue_slot = tables.Queues.query.filter_by(tournament_machine_id=self.tournament_machine['tournament_machine_id'],position=1).first()            
            self.assertEquals(first_queue_slot.player_id,1)
            self.assertEquals(second_queue_slot.player_id,self.player_id_with_no_tokens)
            self.assertTrue(first_queue_slot.bumped)
            self.assertTrue(second_queue_slot.bumped)
            
        pass       

    def test_bump_player_down_queue_removes_player(self):
        with self.event_app.test_client() as c:                        
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.standard_td_username,
                                         'password':self.generic_password}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.post('/token/player_id/%s' % self.player_id_with_no_tokens,
                        data=json.dumps({'tournament_token_counts':[{'tournament_id':1,'token_count':2}],'meta_tournament_token_counts':[]}))
            self.assertHttpCodeEquals(rv,200)            
        with self.event_app.test_client() as c:                        
            tables = self.event_app.tables
            self.bootstrap_queue(tables,self.tournament_machine)            

            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.standard_scorekeeper_username,
                                         'password':self.generic_password}))
            self.assertHttpCodeEquals(rv,200)                        
            rv = c.post('/queue/tournament_machine/%s' % self.tournament_machine['tournament_machine_id'],
                        data=json.dumps({'action':'add','player_id':self.player_id_with_no_tokens}))                        
            self.assertHttpCodeEquals(rv,200)                        
            #FIXME : don't hardcode player id 1 here - i.e. do proper bootstrapping of queue            
            rv = c.put('/queue/tournament_machine/%s' % self.tournament_machine['tournament_machine_id'],
                        data=json.dumps({'action':'bump','player_id':1}))
            self.assertHttpCodeEquals(rv,200)            

            rv = c.put('/queue/tournament_machine/%s' % self.tournament_machine['tournament_machine_id'],
                        data=json.dumps({'action':'bump','player_id':self.player_id_with_no_tokens}))
            self.assertHttpCodeEquals(rv,200)
            
            rv = c.put('/queue/tournament_machine/%s' % self.tournament_machine['tournament_machine_id'],
                        data=json.dumps({'action':'bump','player_id':1}))
            self.assertHttpCodeEquals(rv,200)
            
            second_queue_slot = tables.Queues.query.filter_by(tournament_machine_id=self.tournament_machine['tournament_machine_id'],position=2).first()
            first_queue_slot = tables.Queues.query.filter_by(tournament_machine_id=self.tournament_machine['tournament_machine_id'],position=1).first()            
            self.assertEquals(second_queue_slot.player_id,None)
            self.assertFalse(second_queue_slot.bumped)
            self.assertEquals(first_queue_slot.player_id,self.player_id_with_no_tokens)
            self.assertTrue(first_queue_slot.bumped)

            rv = c.put('/queue/tournament_machine/%s' % self.tournament_machine['tournament_machine_id'],
                        data=json.dumps({'action':'bump','player_id':self.player_id_with_no_tokens}))
            self.assertHttpCodeEquals(rv,200)
            second_queue_slot = tables.Queues.query.filter_by(tournament_machine_id=self.tournament_machine['tournament_machine_id'],position=2).first()
            first_queue_slot = tables.Queues.query.filter_by(tournament_machine_id=self.tournament_machine['tournament_machine_id'],position=1).first()            
            self.assertEquals(second_queue_slot.player_id,None)            
            self.assertEquals(first_queue_slot.player_id,None)
            self.assertFalse(second_queue_slot.bumped)
            self.assertFalse(first_queue_slot.bumped)
            
    def test_bump_player_down_queue_fails_when_wrong_player_given(self):
        with self.event_app.test_client() as c:                        
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.standard_td_username,
                                         'password':self.generic_password}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.post('/token/player_id/%s' % self.player_id_with_no_tokens,
                        data=json.dumps({'tournament_token_counts':[{'tournament_id':1,'token_count':2}],'meta_tournament_token_counts':[]}))
            self.assertHttpCodeEquals(rv,200)            
        with self.event_app.test_client() as c:                        
            tables = self.event_app.tables
            self.bootstrap_queue(tables,self.tournament_machine)            

            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.standard_scorekeeper_username,
                                         'password':self.generic_password}))
            self.assertHttpCodeEquals(rv,200)                        
            rv = c.post('/queue/tournament_machine/%s' % self.tournament_machine['tournament_machine_id'],
                        data=json.dumps({'action':'add','player_id':self.player_id_with_no_tokens}))                        
            self.assertHttpCodeEquals(rv,200)                        
            #FIXME : don't hardcode player id 1 here - i.e. do proper bootstrapping of queue            
            rv = c.put('/queue/tournament_machine/%s' % self.tournament_machine['tournament_machine_id'],
                        data=json.dumps({'action':'bump','player_id':self.player_id_with_no_tokens}))
            self.assertHttpCodeEquals(rv,400,'Bump failed (the queue might have changed under you).  Please try again')            

    def test_bump_player_down_queue_fails_with_player_login(self):
        with self.event_app.test_client() as c:                        
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.standard_td_username,
                                         'password':self.generic_password}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.post('/token/player_id/%s' % self.player_id_with_no_tokens,
                        data=json.dumps({'tournament_token_counts':[{'tournament_id':1,'token_count':2}],'meta_tournament_token_counts':[]}))
            self.assertHttpCodeEquals(rv,200)            
        with self.event_app.test_client() as c:                        
            tables = self.event_app.tables
            self.bootstrap_queue(tables,self.tournament_machine)            
            rv = c.put('/queue/tournament_machine/%s' % self.tournament_machine['tournament_machine_id'],
                        data=json.dumps({'action':'bump','player_id':1}))
            self.assertHttpCodeEquals(rv,403,'Permission denied')            
            rv = c.post('/auth/player/login',
                        data=json.dumps({'event_player_number':self.player_event_id_with_no_tokens,'event_player_pin':self.player_event_pin_with_no_tokens}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.put('/queue/tournament_machine/%s' % self.tournament_machine['tournament_machine_id'],
                        data=json.dumps({'action':'bump','player_id':1}))
            self.assertHttpCodeEquals(rv,403,'Permission denied')            
         
    
