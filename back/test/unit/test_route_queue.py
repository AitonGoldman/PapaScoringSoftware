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
import routes

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

class RouteQueueTest(PssUnitTestBase):
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

    def test_clear_tournament_queue_route(self):
        self.mock_queue_one.bumped=True                
        self.mock_queue_two.bumped=True
        self.mock_queue_three.bumped=False

        self.mock_tables.Queues.query.options().join().filter_by().order_by().all.return_value=[self.mock_queue_one,self.mock_queue_two,self.mock_queue_three]
        #self.mock_tables.db_handle.session.no_autoflush.return_value.__enter__.return_value=MagicMock()
        result = routes.queue.clear_tournament_queue_route(self.mock_app,1)
        self.assertEquals(result,{'result':'clear!'})
        self.assertEquals(self.mock_queue_one.player_id,None)
        self.assertEquals(self.mock_queue_two.player_id,None)
        self.assertEquals(self.mock_queue_three.player_id,None)
        self.assertEquals(self.mock_queue_one.bumped,False)
        self.assertEquals(self.mock_queue_two.bumped,False)
        
    def test_remove_player_from_queue_route(self):
        mock_request_data = MagicMock()
        mock_tournament_machine = MagicMock()
        mock_player = MagicMock()        
        mock_user = MagicMock()
        mock_user.pss_user_id=1
        
        self.mock_queue_one.bumped=True
        self.mock_queue_two.bumped=True
        self.mock_queue_three.bumped=False        
        
        self.mock_tables.Queues.query.options().filter_by().order_by().all.return_value=[self.mock_queue_one,self.mock_queue_two,self.mock_queue_three]        
        self.mock_tables.TournamentMachines.query.filter_by().first.return_value=mock_tournament_machine
        self.mock_tables.Players.query.filter_by().first.return_value=mock_player

        mock_request_data.data = '{"player_id":2}'
        self.mock_tables.Queues.query.options().filter_by().first.return_value=self.mock_queue_two        
        results = routes.queue.remove_player_from_queue_route(mock_request_data,self.mock_app,1,mock_user)        
        self.assertEquals(results['updated_queue'][0].player_id,1)
        self.assertEquals(results['updated_queue'][0].bumped,True)        
        self.assertEquals(results['updated_queue'][1].player_id,3)
        self.assertEquals(results['updated_queue'][1].bumped,False)        
        self.assertEquals(results['updated_queue'][2].player_id,None)
        self.assertEquals(results['updated_queue'][2].bumped,False)        

        mock_request_data.data = '{"player_id":1}'
        self.mock_tables.Queues.query.options().filter_by().first.return_value=self.mock_queue_one        
        results = routes.queue.remove_player_from_queue_route(mock_request_data,self.mock_app,1,mock_user)        

        self.assertEquals(results['updated_queue'][0].player_id,3)
        self.assertEquals(results['updated_queue'][0].bumped,False)        
        self.assertEquals(results['updated_queue'][1].player_id,None)
        self.assertEquals(results['updated_queue'][1].bumped,False)        
        self.assertEquals(results['updated_queue'][2].player_id,None)
        self.assertEquals(results['updated_queue'][2].bumped,False)        

        mock_request_data.data = '{"player_id":3}'
        self.mock_tables.Queues.query.options().filter_by().first.return_value=self.mock_queue_one        
        results = routes.queue.remove_player_from_queue_route(mock_request_data,self.mock_app,1,mock_user)        

        self.assertEquals(results['updated_queue'][0].player_id,None)
        self.assertEquals(results['updated_queue'][0].bumped,False)        
        self.assertEquals(results['updated_queue'][1].player_id,None)
        self.assertEquals(results['updated_queue'][1].bumped,False)        
        self.assertEquals(results['updated_queue'][2].player_id,None)
        self.assertEquals(results['updated_queue'][2].bumped,False)        

        mock_request_data.data = '{"player_id":3}'
        self.mock_tables.Queues.query.options().filter_by().first.return_value=None        
        results = routes.queue.remove_player_from_queue_route(mock_request_data,self.mock_app,1,mock_user)        

        self.assertEquals(results['result'],'noop')
        
    def test_bump_player_down_queue_route(self):
        mock_request_data = MagicMock()
        mock_tournament_machine = MagicMock()
        mock_request_data.data = '{"action":"bump","player_id":1}'
        mock_player = MagicMock()        
        mock_player.player_id=1
        
        self.mock_tables.Queues.query.options().filter_by().order_by().all.return_value=[self.mock_queue_one,self.mock_queue_two,self.mock_queue_three]        
        self.mock_tables.TournamentMachines.query.filter_by().first.return_value=mock_tournament_machine
        self.mock_tables.Players.query.filter_by().first.return_value=mock_player

        results = routes.queue.bump_player_down_queue_route(mock_request_data,self.mock_app,1)
        self.assertEquals(self.mock_queue_one.player_id,2)
        self.assertEquals(self.mock_queue_one.bumped,False)
        self.assertEquals(self.mock_queue_two.player_id,1)
        self.assertEquals(self.mock_queue_two.bumped,True)

        mock_request_data.data = '{"action":"bump","player_id":2}'        
        mock_player.player_id=2                
        
        results = routes.queue.bump_player_down_queue_route(mock_request_data,self.mock_app,1)
        self.assertEquals(self.mock_queue_one.player_id,1)
        self.assertEquals(self.mock_queue_one.bumped,True)
        self.assertEquals(self.mock_queue_two.player_id,2)
        self.assertEquals(self.mock_queue_two.bumped,True)

        mock_request_data.data = '{"action":"bump","player_id":1}'        
        mock_player.player_id=1                
        
        results = routes.queue.bump_player_down_queue_route(mock_request_data,self.mock_app,1)
        self.assertEquals(self.mock_queue_one.player_id,2)
        self.assertEquals(self.mock_queue_one.bumped,True)
        self.assertEquals(self.mock_queue_two.player_id,3)
        self.assertEquals(self.mock_queue_two.bumped,False)

    def test_bump_player_down_queue_route_removes_player_with_queue_size_of_1(self):
        mock_request_data = MagicMock()
        mock_tournament_machine = MagicMock()
        mock_request_data.data = '{"action":"bump","player_id":1}'
        mock_player = MagicMock()        
        mock_player.player_id=1
        
        self.mock_tables.Queues.query.options().filter_by().order_by().all.return_value=[self.mock_queue_one,self.mock_queue_two]        
        self.mock_tables.TournamentMachines.query.filter_by().first.return_value=mock_tournament_machine
        self.mock_tables.Players.query.filter_by().first.return_value=mock_player

        self.mock_queue_two.player_id=None        
        results = routes.queue.bump_player_down_queue_route(mock_request_data,self.mock_app,1)
        self.assertEquals(self.mock_queue_one.player_id,None)
        self.assertEquals(self.mock_queue_one.bumped,False)
        self.assertEquals(self.mock_queue_two.player_id,None)
        self.assertEquals(self.mock_queue_two.bumped,False)        

    def test_bump_player_down_queue_route_fails_with_wrong_player(self):
        mock_request_data = MagicMock()
        mock_tournament_machine = MagicMock()
        mock_player = MagicMock()        
        
        self.mock_tables.Queues.query.options().filter_by().order_by().all.return_value=[self.mock_queue_one,self.mock_queue_two,self.mock_queue_three]        
        self.mock_tables.TournamentMachines.query.filter_by().first.return_value=mock_tournament_machine
        self.mock_tables.Players.query.filter_by().first.return_value=mock_player

        mock_request_data.data = '{"action":"bump","player_id":2}'
        mock_player.player_id=1

        with self.assertRaises(Exception) as cm:        
            results = routes.queue.bump_player_down_queue_route(mock_request_data,self.mock_app,1)
        self.assertEquals(cm.exception.description,"Tried to bump player that is not at head of queue")


    def test_add_player_to_queue_route(self):
        mock_request_data = MagicMock()
        mock_tournament_machine = MagicMock()
        mock_request_data.data = '{"action":"poop","player_id":4}'
        mock_player = MagicMock()        
        mock_player.player_id=4
        mock_user = MagicMock()
        mock_user.pss_user_id=1

        mock_query = MagicMock()
        mock_query.filter_by().count.return_value=1
        self.mock_tables.Tokens.query.filter_by.return_value = mock_query        
        
        self.mock_queue_three.player_id=None        
        
        self.mock_tables.Queues.query.options().filter_by().order_by().all.return_value=[self.mock_queue_one,self.mock_queue_two,self.mock_queue_three]        
        self.mock_tables.Queues.query.options().filter_by().first.return_value=None

        self.mock_tables.TournamentMachines.query.filter_by().first.return_value=mock_tournament_machine
        self.mock_tournament.meta_tournament_id=None
        self.mock_tables.Tournaments.query.filter_by().first.return_value=self.mock_tournament
        
        self.mock_tables.Players.query.filter_by().first.return_value=mock_player
        routes.queue.add_player_to_queue_route_validate(mock_request_data,self.mock_app,1,mock_user)
        routes.queue.add_player_to_queue_route_remove_existing(mock_request_data,self.mock_app,1,mock_user)
        
        results = routes.queue.add_player_to_queue_route(mock_request_data,self.mock_app,1,mock_user)
        self.assertEquals(results['result'],"player added")
        self.assertEquals(results['added_queue'],self.mock_queue_three)
        self.assertEquals(results['added_queue'].player_id,4)

        self.mock_tournament.meta_tournament_id=1
        self.mock_tables.MetaTournaments.query.filter_by().first.return_value=self.mock_meta_tournament
        self.mock_queue_three.player_id=None
        results = routes.queue.add_player_to_queue_route(mock_request_data,self.mock_app,1,mock_user)
        self.assertEquals(results['result'],"player added")
        self.assertEquals(results['added_queue'],self.mock_queue_three)
        self.assertEquals(results['added_queue'].player_id,4)

    def test_add_player_to_queue_route_when_player_already_in_another_queue(self):
        mock_request_data = MagicMock()
        mock_tournament_machine = MagicMock()
        mock_request_data.data = '{"action":"bump","player_id":4}'
        mock_player = MagicMock()        
        mock_player.player_id=4
        mock_user = MagicMock()
        mock_user.pss_user_id=1

        mock_query = MagicMock()
        mock_query.filter_by().count.return_value=1
        self.mock_tables.Tokens.query.filter_by.return_value = mock_query        
        
        self.mock_queue_three.player_id=None                
        self.mock_queue_four.player_id=4                
        self.mock_queue_four.tournament_machine_id=2                
        
        #self.mock_tables.Queues.query.options().filter_by().order_by().all.return_value=[self.mock_queue_one,self.mock_queue_two,self.mock_queue_three]
        self.mock_tables.Queues.query.options().filter_by().order_by().all.return_value=[self.mock_queue_four]        
        self.mock_tables.Queues.query.options().filter_by().first.return_value=self.mock_queue_four

        self.mock_tables.TournamentMachines.query.filter_by().first.return_value=mock_tournament_machine
        self.mock_tournament.meta_tournament_id=None
        self.mock_tables.Tournaments.query.filter_by().first.return_value=self.mock_tournament
        
        self.mock_tables.Players.query.filter_by().first.return_value=mock_player

        routes.queue.add_player_to_queue_route_validate(mock_request_data,self.mock_app,1,mock_user)
        routes.queue.add_player_to_queue_route_remove_existing(mock_request_data,self.mock_app,1,mock_user)                

        self.mock_tables.Queues.query.options().filter_by().order_by().all.return_value=[self.mock_queue_one,self.mock_queue_two,self.mock_queue_three]        
        results = routes.queue.add_player_to_queue_route(mock_request_data,self.mock_app,1,mock_user)
        
        self.assertEquals(results['result'],"player added")
        self.assertEquals(results['added_queue'],self.mock_queue_three)
        self.assertEquals(results['added_queue'].player_id,4)
        self.assertEquals(self.mock_queue_four.player_id,None)
        
    def test_add_player_to_queue_route_fails_when_queue_is_full_or_empty(self):
        mock_request_data = MagicMock()
        mock_tournament_machine = MagicMock()
        mock_request_data.data = '{"action":"bump","player_id":4}'
        mock_player = MagicMock()        
        mock_player.player_id=4
        mock_user = MagicMock()
        mock_user.pss_user_id=1

        mock_query = MagicMock()
        mock_query.filter_by().count.return_value=1
        self.mock_tables.Tokens.query.filter_by.return_value = mock_query                        
        
        self.mock_tables.Queues.query.options().filter_by().order_by().all.return_value=[self.mock_queue_one,self.mock_queue_two,self.mock_queue_three]        
        self.mock_tables.Queues.query.options().filter_by().first.return_value=None

        self.mock_tables.TournamentMachines.query.filter_by().first.return_value=mock_tournament_machine
        self.mock_tournament.meta_tournament_id=None
        self.mock_tables.Tournaments.query.filter_by().first.return_value=self.mock_tournament
        
        self.mock_tables.Players.query.filter_by().first.return_value=mock_player
        with self.assertRaises(Exception) as cm:                
            results = routes.queue.add_player_to_queue_route(mock_request_data,self.mock_app,1,mock_user)
        self.assertEquals(cm.exception.description,"no room left in queue")

        self.mock_queue_one.player_id=None
        self.mock_queue_two.player_id=None
        self.mock_queue_three.player_id=None

        with self.assertRaises(Exception) as cm:
            routes.queue.add_player_to_queue_route_validate(mock_request_data,self.mock_app,1,mock_user)
            routes.queue.add_player_to_queue_route_remove_existing(mock_request_data,self.mock_app,1,mock_user)                               
            results = routes.queue.add_player_to_queue_route(mock_request_data,self.mock_app,1,mock_user)
        self.assertEquals(cm.exception.description,"Can not add to empty queue.  Please see scorekeeper")
        
    def test_add_player_to_queue_route_fails_with_no_tickets(self):
        mock_request_data = MagicMock()
        mock_tournament_machine = MagicMock()
        mock_request_data.data = '{"action":"bump","player_id":4}'
        mock_player = MagicMock()        
        mock_player.player_id=4
        mock_user = MagicMock()
        mock_user.pss_user_id=1

        mock_query = MagicMock()
        mock_query.filter_by().count.return_value=0
        self.mock_tables.Tokens.query.filter_by.return_value = mock_query        
        
        self.mock_queue_three.player_id=None
        
        self.mock_tables.Queues.query.options().filter_by().order_by().all.return_value=[self.mock_queue_one,self.mock_queue_two,self.mock_queue_three]        
        self.mock_tables.Queues.query.options().filter_by().first.return_value=None

        self.mock_tables.TournamentMachines.query.filter_by().first.return_value=mock_tournament_machine
        self.mock_tournament.meta_tournament_id=None
        self.mock_tables.Tournaments.query.filter_by().first.return_value=self.mock_tournament
        
        self.mock_tables.Players.query.filter_by().first.return_value=mock_player

        with self.assertRaises(Exception) as cm:                
            routes.queue.add_player_to_queue_route_validate(mock_request_data,self.mock_app,1,mock_user)
            routes.queue.add_player_to_queue_route_remove_existing(mock_request_data,self.mock_app,1,mock_user)                               
            results = routes.queue.add_player_to_queue_route(mock_request_data,self.mock_app,1,mock_user)
        self.assertEquals(cm.exception.description,"Player has no tokens")

        self.mock_tournament.meta_tournament_id=1
        self.mock_tables.MetaTournaments.query.filter_by().first.return_value=self.mock_meta_tournament
        
        with self.assertRaises(Exception) as cm:
            routes.queue.add_player_to_queue_route_validate(mock_request_data,self.mock_app,1,mock_user)
            routes.queue.add_player_to_queue_route_remove_existing(mock_request_data,self.mock_app,1,mock_user)                                           
            results = routes.queue.add_player_to_queue_route(mock_request_data,self.mock_app,1,mock_user)
        self.assertEquals(cm.exception.description,"Player has no tokens")
 
        
