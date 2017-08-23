import unittest
from mock import MagicMock
from pss_unit_test_base import PssUnitTestBase
from lib.flask_lib import app_build
from lib import CustomJsonEncoder
from flask import Flask
from flask_principal import Principal
from lib.PssConfig import PssConfig
from routes import tournament_machine
from lib import roles_constants,orm_factories
import json
from werkzeug.exceptions import BadRequest,Unauthorized

class RouteTournamentMachineTest(PssUnitTestBase):
    def setUp(self):
        self.mock_request = MagicMock()        
        self.mock_tables = MagicMock()
        self.mock_event = MagicMock()
        self.mock_pss_config = MagicMock()
        self.mock_app.tables = self.mock_tables
        
    def test_create_tournament_machine_route(self):
        mock_input_data=MagicMock()
        mock_input_data.data = json.dumps({'tournament_id':'1',
                                           'machine_id':'1'})
        mock_tournament = MagicMock()
        mock_tournament_machine = MagicMock()
        mock_machine = MagicMock()
        
        self.mock_tables.TournamentMachines.query.filter_by().first.return_value=None
        #self.mock_tables.TournamentMachines.return_value=mock_tournament_machine
        self.mock_tables.Machines.query.filter_by().first.return_value=mock_machine
        self.mock_tables.Tournaments.query.filter_by().first.return_value=mock_tournament
        
        self.mock_tables.TournamentMachines.side_effect = self.generate_side_effect_confirm_args(['machine_id',
                                                                                                  'tournament_machine_name',
                                                                                                  'tournament_machine_abbreviation',
                                                                                                  'active'],
                                                                                                 return_value=mock_tournament_machine)
        
        returned_tournament_machine = tournament_machine.create_tournament_machine_route(mock_input_data,self.mock_app)        
        self.assertEquals(mock_tournament_machine,returned_tournament_machine)

    def test_create_tournament_machine_route_fails_with_missing_info(self):
        mock_input_data=MagicMock()
        mock_input_data.data = json.dumps({'tournament_id':'1'})
        mock_tournament = MagicMock()
        mock_tournament_machine = MagicMock()
        mock_machine = MagicMock()
        with self.assertRaises(Exception) as cm:                        
            returned_tournament_machine = tournament_machine.create_tournament_machine_route(mock_input_data,self.mock_app)        
        self.assertEquals(cm.exception.description,"Missing information")

        mock_input_data.data = json.dumps({'machine_id':'1'})
        with self.assertRaises(BadRequest) as cm:                        
            returned_tournament_machine = tournament_machine.create_tournament_machine_route(mock_input_data,self.mock_app)        
        self.assertEquals(cm.exception.description,"Missing information")

    def test_create_tournament_machine_route_fails_with_bad_info(self):
        mock_input_data=MagicMock()
        mock_input_data.data = json.dumps({'tournament_id':'999',
                                           'machine_id':'1'})
        mock_tournament = MagicMock()
        mock_tournament_machine = MagicMock()
        mock_machine = MagicMock()
        
        self.mock_tables.TournamentMachines.query.filter_by().first.return_value=None
        #self.mock_tables.TournamentMachines.return_value=mock_tournament_machine
        self.mock_tables.Machines.query.filter_by().first.return_value=mock_machine
        self.mock_tables.Tournaments.query.filter_by().first.return_value=None
        with self.assertRaises(BadRequest) as cm:                                        
            returned_tournament_machine = tournament_machine.create_tournament_machine_route(mock_input_data,self.mock_app)        
        self.assertEquals(cm.exception.description,"Trying to add to a bad tournament, or trying to add a bad machine")

        mock_input_data.data = json.dumps({'tournament_id':'1',
                                           'machine_id':'999'})
        self.mock_tables.Machines.query.filter_by().first.return_value=None
        self.mock_tables.Tournaments.query.filter_by().first.return_value=mock_tournament
        with self.assertRaises(BadRequest) as cm:                                        
            returned_tournament_machine = tournament_machine.create_tournament_machine_route(mock_input_data,self.mock_app)        
        self.assertEquals(cm.exception.description,"Trying to add to a bad tournament, or trying to add a bad machine")
        
        
    def test_create_tournament_machine_route_readd_machine(self):
        mock_input_data=MagicMock()
        mock_input_data.data = json.dumps({'tournament_id':'1',
                                           'machine_id':'1'})
        mock_tournament = MagicMock()
        mock_tournament_machine = MagicMock()
        mock_tournament_machine.removed=True
        mock_tournament_machine.active=False
        
        mock_machine = MagicMock()
        
        self.mock_tables.TournamentMachines.query.filter_by().first.return_value=mock_tournament_machine
        #self.mock_tables.TournamentMachines.return_value=mock_tournament_machine
        self.mock_tables.Machines.query.filter_by().first.return_value=mock_machine
        self.mock_tables.Tournaments.query.filter_by().first.return_value=mock_tournament
                
        returned_tournament_machine = tournament_machine.create_tournament_machine_route(mock_input_data,self.mock_app)        
        self.assertEquals(mock_tournament_machine,returned_tournament_machine)
        self.assertFalse(mock_tournament_machine.removed)
        self.assertTrue(mock_tournament_machine.active)

    #FIXME : clean this test up
    def test_edit_tournament_machine_route(self):
        mock_input_data=MagicMock()
        mock_input_data.data = json.dumps({'removed':True,
                                           'active':True})        
        mock_tournament_machine = MagicMock()
        mock_tournament_machine.__table__= MagicMock()
        
        self.mock_tables.TournamentMachines.query.filter_by().first.return_value=mock_tournament_machine                
        returned_tournament_machine = tournament_machine.edit_tournament_machine_route(1,mock_input_data,self.mock_app)        
        self.assertEquals(mock_tournament_machine,returned_tournament_machine)
        self.assertEquals(mock_tournament_machine.removed,True)
        self.assertEquals(mock_tournament_machine.active,False)

        mock_tournament_machine.removed=False
        mock_input_data.data = json.dumps({'removed':False,
                                           'active':False})        

        returned_tournament_machine = tournament_machine.edit_tournament_machine_route(1,mock_input_data,self.mock_app)        
        
        self.assertEquals(mock_tournament_machine,returned_tournament_machine)
        self.assertEquals(mock_tournament_machine.active,False)
        self.assertEquals(mock_tournament_machine.removed,False)
        
        
