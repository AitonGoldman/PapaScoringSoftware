import unittest
from mock import MagicMock
from pss_unit_test_base import PssUnitTestBase
from flask_sqlalchemy import SQLAlchemy
from pss_models_v2 import TournamentMachines,Machines

class TablesProxyTournamentTest(PssUnitTestBase):        
    def setUp(self):                
        self.sqlalchemy_tournament_machine=self.initialize_single_sqlalchemy(self.tables_proxy,"TournamentMachines",TournamentMachines.generate_tournament_machines_class,True)                
        self.sqlalchemy_machine=self.initialize_single_sqlalchemy(self.tables_proxy,"Machines",Machines.generate_machines_class,True)                
        
    def test_get_tournament_machine_by_id(self):                        
        self.set_mock_single_query(self.tables_proxy,"TournamentMachines",self.sqlalchemy_tournament_machine)        
        return_value = self.tables_proxy.get_tournament_machine_by_id(1)
        self.assertEquals(return_value,self.sqlalchemy_tournament_machine)        
        filter_by = self.tables_proxy.TournamentMachines.query.filter_by
        self.assertTrue('tournament_machine_id' in filter_by.call_args[1])
        self.assertEquals(filter_by.call_args[1]['tournament_machine_id'],1)

    def test_get_tournament_machines(self):                        
        self.set_mock_all_query(self.tables_proxy,"TournamentMachines",[self.sqlalchemy_tournament_machine])        
        return_value = self.tables_proxy.get_tournament_machines(1)
        self.assertEquals(return_value,[self.sqlalchemy_tournament_machine])        
        filter_by = self.tables_proxy.TournamentMachines.query.filter_by
        self.assertTrue('tournament_id' in filter_by.call_args[1])
        self.assertEquals(filter_by.call_args[1]['tournament_id'],1)
        
    def test_create_tournament_machine(self):
        mock_tournament=MagicMock()
        mock_tournament.tournament_id=1
        
        self.set_mock_single_query(self.tables_proxy,"TournamentMachines",None)
        self.sqlalchemy_machine.machine_id=1
        self.sqlalchemy_machine.machine_name="test_machine"
        self.sqlalchemy_machine.abbreviation="tst"
        return_value = self.tables_proxy.create_tournament_machine(self.sqlalchemy_machine,mock_tournament)
        self.assertEquals(self.sqlalchemy_tournament_machine,return_value)
        self.assertEquals(return_value.machine_id,self.sqlalchemy_machine.machine_id)
        self.assertEquals(return_value.tournament_machine_name,self.sqlalchemy_machine.machine_name)
        self.assertEquals(return_value.tournament_id,mock_tournament.tournament_id)

    def test_create_tournament_machine_with_existing_machine(self):
        mock_tournament=MagicMock()
        mock_tournament.tournament_id=1
        self.sqlalchemy_tournament_machine.removed=True
        self.sqlalchemy_tournament_machine.active=False        
        self.set_mock_single_query(self.tables_proxy,"TournamentMachines",self.sqlalchemy_tournament_machine)
        return_value = self.tables_proxy.create_tournament_machine(self.sqlalchemy_machine,mock_tournament)
        self.assertEquals(self.sqlalchemy_tournament_machine,return_value)
        self.assertEquals(self.sqlalchemy_tournament_machine.removed,False)
        self.assertEquals(self.sqlalchemy_tournament_machine.active,True)
