import unittest
from mock import MagicMock
from pss_unit_test_base import PssUnitTestBase
from lib.flask_lib import app_build
from lib import CustomJsonEncoder
from flask import Flask
from flask_principal import Principal
from lib.PssConfig import PssConfig
from lib import queue_helpers
from lib import roles_constants,orm_factories
import json
from werkzeug.exceptions import BadRequest,Unauthorized


def generate_mock_tournament(tournament_id=None,meta_tournament_id=None):
    mock_tournament = MagicMock()        
    mock_tournament.number_of_tickets_for_discount=None
    if tournament_id:
        mock_tournament.tournament_name="test tournament"
    if meta_tournament_id:
        mock_tournament.meta_tournament_name="test meta tournament"
        
    mock_tournament.team_tournament=False
    mock_tournament.minimum_number_of_tickets_allowed=1
    mock_tournament.number_of_unused_tickets_allowed=15
    mock_tournament.ticket_increment_for_each_purchase=1
    mock_tournament.use_stripe=False
    mock_tournament.manually_set_price=3
    mock_tournament.ifpa_rank_restriction=None
    if tournament_id:
        mock_tournament.tournament_id=tournament_id
    if meta_tournament_id:
        mock_tournament.meta_tournament_id=meta_tournament_id
    return mock_tournament

class LibQueueHelpersTest(PssUnitTestBase):
    def setUp(self):
        self.mock_request = MagicMock()        
        self.mock_tables = MagicMock()
        self.mock_event = MagicMock()
        self.mock_pss_config = MagicMock()
        self.mock_app.tables = self.mock_tables
        self.mock_token_purchase = MagicMock()
        self.mock_token_purchase_summary = MagicMock()
        self.mock_token = MagicMock()                
        self.mock_tournament_machine=MagicMock()
        self.mock_tournament=generate_mock_tournament(tournament_id=1)        
        self.mock_meta_tournament=generate_mock_tournament(meta_tournament_id=1)        
        self.create_mock_queues()
        
    def test_get_queue_for_tounament_machine(self):
        #not needed
        pass
    def test_get_queue_player_is_already_in(self):
        #not needed
        pass
    
    def test_get_queue_for_tounament(self):        
        self.mock_queue_one.tournament_machine_id=1                
        self.mock_queue_two.tournament_machine_id=2                
        self.mock_queue_three.tournament_machine_id=3        

        self.mock_tables.Queues.query.options().join().filter_by().order_by().all.return_value=[self.mock_queue_one,self.mock_queue_two,self.mock_queue_three]
        results = queue_helpers.get_queue_for_tounament(self.mock_app,1) 
        grouped_results = [[q for q in group_q] for id,group_q in results]
        print grouped_results
        self.assertEquals(1,grouped_results[0][0].player_id)
        self.assertEquals(2,grouped_results[1][0].player_id)
        self.assertEquals(3,grouped_results[2][0].player_id)
    
    def test_add_player_to_queue(self):
        self.mock_queue_four.player_id=None
                
        queues = [self.mock_queue_one,self.mock_queue_two,self.mock_queue_three,self.mock_queue_four]
        result = queue_helpers.add_player_to_queue(4,queues,self.mock_app,1)
        self.assertEquals(self.mock_queue_four,result)
        self.assertEquals(1,queues[0].player_id)
        self.assertEquals(2,queues[1].player_id)
        self.assertEquals(3,queues[2].player_id)
        self.assertEquals(4,queues[3].player_id)        
        with self.assertRaises(BadRequest) as cm:                
            result = queue_helpers.add_player_to_queue(4,queues,self.mock_app,1)
        self.assertEquals(cm.exception.description,"no room left in queue")

    def test_remove_player_from_queue(self):
        self.mock_queue_four.player_id=None
        

        self.mock_tables.Queues.query.options().filter_by().first.return_value=self.mock_queue_two
                
        queues = [self.mock_queue_one,self.mock_queue_two,self.mock_queue_three,self.mock_queue_four]
        result = queue_helpers.remove_player_from_queue(self.mock_app,2,queues)
        self.assertTrue(result)
        self.assertEquals(1,queues[0].player_id)
        self.assertEquals(3,queues[1].player_id)
        self.assertEquals(None,queues[2].player_id)
        self.assertEquals(None,queues[3].player_id)        

        self.mock_tables.Queues.query.options().filter_by().first.return_value=self.mock_queue_two        
        result = queue_helpers.remove_player_from_queue(self.mock_app,3,queues)
        self.assertTrue(result)
        self.assertEquals(1,queues[0].player_id)
        self.assertEquals(None,queues[1].player_id)
        self.assertEquals(None,queues[2].player_id)
        self.assertEquals(None,queues[3].player_id)        

        self.mock_tables.Queues.query.options().filter_by().first.return_value=self.mock_queue_one        
        result = queue_helpers.remove_player_from_queue(self.mock_app,1,queues)
        self.assertTrue(result)
        self.assertEquals(None,queues[0].player_id)
        self.assertEquals(None,queues[1].player_id)
        self.assertEquals(None,queues[2].player_id)
        self.assertEquals(None,queues[3].player_id)        
        
        self.mock_tables.Queues.query.options().filter_by().first.return_value=None
        
        result = queue_helpers.remove_player_from_queue(self.mock_app,2,queues)            
        self.assertEquals(result,False)

        
    def test_bump_player_down_queue(self):
                
        queues = [self.mock_queue_one,self.mock_queue_two,self.mock_queue_three,self.mock_queue_four]
        self.mock_tables.Queues.query.options().filter_by().first.return_value=self.mock_queue_one        
        result = queue_helpers.bump_player_down_queue(self.mock_app,1,queues)
        self.assertEquals(queues,result)        
        self.assertEquals(queues[0].player_id,2)
        self.assertEquals(queues[0].bumped,False)
        self.assertEquals(queues[1].player_id,1)
        self.assertEquals(queues[1].bumped,True)

        result = queue_helpers.bump_player_down_queue(self.mock_app,1,queues)        
        self.assertEquals(queues[0].player_id,1)
        self.assertEquals(queues[0].bumped,True)
        self.assertEquals(queues[1].player_id,2)
        self.assertEquals(queues[1].bumped,True)

