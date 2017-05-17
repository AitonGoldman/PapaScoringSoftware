import unittest
from td_types import ImportedTables
from util import db_util
from td_unit_test_base import TdUnitTestBase

class ModelDivisionFinalPlayerTD(TdUnitTestBase):
    def setUp(self):        
        self.db_handle = db_util.create_db_handle_no_app()        
        self.tables = ImportedTables(self.db_handle)        
        self.division_final_players = self.create_division_final_players()
        self.simple_dict = self.division_final_players[0].to_dict_simple()        
        
    def test_to_dict_simple(self):                 
        for value in self.division_final_players[0].__table__.columns:
            key =  str(value)[str(value).index('.')+1:]            
            self.assertTrue(key in self.simple_dict,"oops - did not find %s" % key)        
    def test_relationships(self):
        self.assertTrue('player' in self.simple_dict)
        self.assertEquals(self.simple_dict['player']['player_id'],1)
       
 
