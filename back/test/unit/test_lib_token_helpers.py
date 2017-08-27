import unittest
from mock import MagicMock
from pss_unit_test_base import PssUnitTestBase
from lib.flask_lib import app_build
from lib import CustomJsonEncoder
from flask import Flask
from flask_principal import Principal
from lib.PssConfig import PssConfig
from lib import token_helpers
from lib import roles_constants,orm_factories
import json
from werkzeug.exceptions import BadRequest,Unauthorized

class LibTokenHelpersTest(PssUnitTestBase):
    def setUp(self):
        self.mock_request = MagicMock()        
        self.mock_tables = MagicMock()
        self.mock_event = MagicMock()
        self.mock_pss_config = MagicMock()
        self.mock_app.tables = self.mock_tables
        
    def test_get_number_of_unused_tickets_for_player(self):
        mock_tournament = MagicMock()
        mock_tournament.team_tournament = False
        mock_tournament.tournament_id = 1
        
        mock_token = MagicMock()
        mock_player = MagicMock()
        mock_player.player_id=1
        mock_multi_division_tournament = MagicMock()        
        
        mock_tokens=MagicMock()
        mock_tokens.filter_by.side_effect = self.generate_side_effect_confirm_args(['tournament_id','player_id'],return_count=1)
        list_of_arg_names = ['used',
                             'voided',
                             'paid_for',
                             'deleted']
        list_of_arg_values = {            
            'used':False,
            'voided':False,
            'paid_for':True,
            'deleted':False
        }
        self.mock_tables.Tokens.query.filter_by.side_effect = self.generate_side_effect_confirm_args(list_of_arg_names,
                                                                                                     values=list_of_arg_values,
                                                                                                     return_value=mock_tokens)
        returned_token_count = token_helpers.get_number_of_unused_tickets_for_player(mock_player,self.mock_app,tournament=mock_tournament)
        self.assertEquals(returned_token_count,1)

    def test_get_number_of_unused_tickets_for_player_in_team_tournament(self):
        mock_tournament = MagicMock()
        mock_tournament.team_tournament = True
        mock_tournament.tournament_id = 1
        
        mock_token = MagicMock()
        mock_player = MagicMock()
        mock_player.player_id=1
        mock_player.team_id=1
        
        mock_multi_division_tournament = MagicMock()        
        
        mock_tokens=MagicMock()
        mock_tokens.filter_by().count.return_value=1
        self.mock_tables.Tokens.query.filter_by.return_value = mock_tokens
        returned_token_count = token_helpers.get_number_of_unused_tickets_for_player(mock_player,self.mock_app,tournament=mock_tournament)        
        self.assertEquals(returned_token_count,1)

    def test_get_number_of_unused_tickets_for_player_in_team_tournament_with_no_team(self):
        mock_tournament = MagicMock()
        mock_tournament.team_tournament = True
        mock_tournament.tournament_id = 1
        
        mock_token = MagicMock()
        mock_player = MagicMock()
        mock_player.player_id=1
        mock_player.team_id=None
        
        mock_multi_division_tournament = MagicMock()        
        
        mock_tokens=MagicMock()
        mock_tokens.filter_by().count.return_value=1
        self.mock_tables.Tokens.query.filter_by.return_value = mock_tokens
        returned_token_count = token_helpers.get_number_of_unused_tickets_for_player(mock_player,self.mock_app,tournament=mock_tournament)        
        self.assertEquals(returned_token_count,0)

    def test_get_number_of_unused_tickets_for_player_in_meta_tournament(self):
        mock_meta_tournament = MagicMock()
        mock_meta_tournament.team_tournament = False
        mock_meta_tournament.meta__tournament_id = 1
        
        mock_token = MagicMock()
        mock_player = MagicMock()
        mock_player.player_id=1
        mock_player.team_id=1
        
        mock_multi_division_tournament = MagicMock()        
        
        mock_tokens=MagicMock()
        mock_tokens.filter_by().count.return_value=1
        self.mock_tables.Tokens.query.filter_by.return_value = mock_tokens
        returned_token_count = token_helpers.get_number_of_unused_tickets_for_player(mock_player,self.mock_app,meta_tournament=mock_meta_tournament)        
        self.assertEquals(returned_token_count,1)

    def test_get_number_of_unused_tickets_for_player_in_all_tournaments(self):                
        mock_player = MagicMock()
        mock_player.player_id=1
        mock_tournament = MagicMock()
        mock_tournament.tournament_name='test_tournament'
        mock_tournament.tournament_id=1
        mock_meta_tournament = MagicMock()
        mock_meta_tournament.meta_tournament_name='test_meta_tournament'
        mock_meta_tournament.meta_tournament_id=2

        self.mock_tables.Tournaments.query.filter_by().all.return_value = [mock_tournament]
        self.mock_tables.MetaTournaments.query.all.return_value = [mock_meta_tournament]

        mock_query = MagicMock()
        mock_query.filter_by().count.return_value=1
        self.mock_tables.Tokens.query.filter_by.return_value = mock_query
        
        mock_tournament.team_tournament = False
        mock_player.team_id = None
        mock_tokens_count = token_helpers.get_number_of_unused_tickets_for_player_in_all_tournaments(mock_player,self.mock_app)
        self.assertEquals(len(mock_tokens_count),2)
        self.assertEquals(mock_tokens_count[0][0]['tournament_id'],1)
        self.assertEquals(mock_tokens_count[0][0]['count'],1)
        self.assertEquals(mock_tokens_count[1][0]['meta_tournament_id'],2)
        self.assertEquals(mock_tokens_count[1][0]['count'],1)


        mock_query.filter_by().count.return_value=0
        mock_tokens_count = token_helpers.get_number_of_unused_tickets_for_player_in_all_tournaments(mock_player,self.mock_app)
        self.assertEquals(len(mock_tokens_count),2)
        self.assertEquals(len(mock_tokens_count[0]),0)
        self.assertEquals(len(mock_tokens_count[1]),0)
        
    def test_get_normal_and_discount_amounts(self):
        mock_tournament = MagicMock()
        mock_tournament.number_of_tickets_for_discount=None
        counts = token_helpers.get_normal_and_discount_amounts(mock_tournament,11)
        self.assertEquals(counts,(11,0))

        mock_tournament.number_of_tickets_for_discount=3
        counts = token_helpers.get_normal_and_discount_amounts(mock_tournament,3)
        self.assertEquals(counts,(0,1))

        counts = token_helpers.get_normal_and_discount_amounts(mock_tournament,2)
        self.assertEquals(counts,(2,0))        
                
        counts = token_helpers.get_normal_and_discount_amounts(mock_tournament,11)
        self.assertEquals(counts,(2,3))
        
