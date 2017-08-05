import unittest
from td_types import ImportedTables
from util import db_util
from td_unit_test_base import TdUnitTestBase

class ModelDivisionFinalTD(TdUnitTestBase):
    def setUp(self):        
        self.db_handle = db_util.create_db_handle_no_app()        
        self.tables = ImportedTables(self.db_handle)        
        self.division_final = self.create_division_final(use_division_final_players=True)
        self.simple_dict = self.division_final.to_dict_simple()        
        
    def test_to_dict_simple(self):                 
        for value in self.division_final.__table__.columns:
            key =  str(value)[str(value).index('.')+1:]            
            self.assertTrue(key in self.simple_dict,"oops - did not find %s" % key)        
    def test_relationships(self):
        self.assertTrue('qualifiers' in self.simple_dict)
        self.assertTrue(len(self.simple_dict['qualifiers']) == 2)
        self.assertEquals(self.simple_dict['qualifiers'][0]['player_id'],1)
       
 
