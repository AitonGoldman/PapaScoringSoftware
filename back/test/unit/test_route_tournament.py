import unittest
from mock import MagicMock
from pss_unit_test_base import PssUnitTestBase
from lib.flask_lib import app_build
from lib import CustomJsonEncoder
from flask import Flask
from flask_principal import Principal
from lib.PssConfig import PssConfig
from routes import tournament
from lib import roles_constants,orm_factories
import json
from werkzeug.exceptions import BadRequest,Unauthorized

class RouteTournamentTest(PssUnitTestBase):
    def setUp(self):
        self.mock_request = MagicMock()        
        self.mock_tables = MagicMock()
        self.mock_event = MagicMock()
        self.mock_pss_config = MagicMock()
        self.mock_app.tables = self.mock_tables
        
    def test_create_tournament_route(self):
        mock_input_data=MagicMock()
        mock_input_data.data = json.dumps({'tournament_name':'poop_tournament'})
        mock_tournament = MagicMock()
        mock_multi_division_tournament = MagicMock()

        self.mock_tables.Tournaments.query.filter_by().first.return_value=None
        self.mock_tables.MultiDivisionTournaments.return_value=mock_multi_division_tournament
        
        self.mock_tables.Tournaments.side_effect = self.generate_side_effect_confirm_args(['tournament_name'],return_value=mock_tournament)
        
        returned_tournament = tournament.create_tournament_route(mock_input_data,self.mock_app)        
        self.assertEquals(mock_tournament,returned_tournament)

    def test_create_tournament_route_fails_with_duplicate_name(self):
        mock_input_data=MagicMock()
        mock_input_data.data = json.dumps({'tournament_name':'poop_tournament'})
        mock_tournament = MagicMock()
        mock_multi_division_tournament = MagicMock()

        self.mock_tables.Tournaments.query.filter_by().first.return_value=mock_tournament
        self.mock_tables.MultiDivisionTournaments.return_value=mock_multi_division_tournament
                
        with self.assertRaises(Exception) as cm:        
            returned_tournament = tournament.create_tournament_route(mock_input_data,self.mock_app)        
        self.assertEquals(cm.exception.description,"Trying to use an already used name for tournament")
        
         
    def test_create_multi_division_tournament_route(self):
        mock_input_data=MagicMock()
        mock_input_data.data = json.dumps({'tournament_name':'poop_tournament'})
        mock_tournament = MagicMock()
        mock_multi_division_tournament = MagicMock()

        self.mock_tables.Tournaments.query.filter_by().first.return_value=None
        self.mock_tables.MultiDivisionTournaments.return_value=mock_multi_division_tournament
        
        mock_input_data.data = json.dumps({'tournament_name':'poop_tournament','multi_division_tournament_name':'poop_main'})        
        self.mock_tables.Tournaments.side_effect = self.generate_side_effect_confirm_args(['tournament_name'],
                                                                                          return_value=mock_tournament)

        returned_tournament = tournament.create_tournament_route(mock_input_data,self.mock_app)                
        self.assertEquals(returned_tournament.multi_division_tournament,mock_multi_division_tournament)
        self.assertEquals(returned_tournament.multi_division_tournament_name,'poop_main')
        
    def test_create_division_for_existing_multi_division_tournament_route(self):
        mock_input_data=MagicMock()
        mock_input_data.data = json.dumps({'tournament_name':'poop_tournament'})
        mock_tournament = MagicMock()
        mock_multi_division_tournament = MagicMock()
        mock_multi_division_tournament.multi_division_tournament_id=1
        mock_multi_division_tournament.multi_division_tournament_name='poop_main'
        
        self.mock_tables.Tournaments.query.filter_by().first.return_value=None
        self.mock_tables.Tournaments.return_value=mock_tournament
        
        self.mock_tables.MultiDivisionTournaments.query.filter_by().first.return_value=mock_multi_division_tournament
        
        mock_input_data.data = json.dumps({'tournament_name':'poop_tournament','multi_division_tournament_id':'1'})        
        self.mock_tables.Tournaments.side_effect = self.generate_side_effect_confirm_args(['tournament_name'],
                                                                                          return_value=mock_tournament)

        returned_tournament = tournament.create_tournament_route(mock_input_data,self.mock_app)                
        self.assertEquals(returned_tournament.multi_division_tournament,mock_multi_division_tournament)
        self.assertEquals(returned_tournament.multi_division_tournament_name,'poop_main')

    def test_create_tournament_with_ppo_style_finals(self):
        #FIXME : this also means fixes are needed in the normal style test
        pass
    
    def test_get_tournaments(self):        
        pass
