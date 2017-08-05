import unittest
from td_types import ImportedTables
from util import db_util
from td_unit_test_base import TdUnitTestBase

class ModelDivisionMachineTD(TdUnitTestBase):
    def setUp(self):        
        self.db_handle = db_util.create_db_handle_no_app()        
        self.tables = ImportedTables(self.db_handle)
        self.create_single_division_tournament()
        self.create_division_machine()
        self.player = self.create_player(1)
        self.create_team()            
            
    def test_to_dict_simple(self):
        returned_division_machine_dict = self.division_machine.to_dict_simple()
        for value in self.division_machine.__table__.columns:
            key =  str(value)[str(value).index('.')+1:]            
            self.assertTrue(key in returned_division_machine_dict,"did not find %s"%key)                    
        self.assertEquals(returned_division_machine_dict['division_machine_name'],'test_machine')
        self.assertEquals(returned_division_machine_dict['abbreviation'],'AAA')
        self.assertEquals(returned_division_machine_dict['player']['player_id'],1)
        self.assertEquals(returned_division_machine_dict['team']['team_id'],1)
        
