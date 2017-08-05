import unittest
from td_types import ImportedTables
from util import db_util
from td_unit_test_base import TdUnitTestBase

class ModelDivisionMachineTD(TdUnitTestBase):
    def setUp(self):        
        self.db_handle = db_util.create_db_handle_no_app()        
        self.tables = ImportedTables(self.db_handle)
        tournaments = self.create_multiple_single_div_tournaments('test_tournament',2)
        
        self.meta_division = self.tables.MetaDivision(
            meta_division_name='test_meta_division'
        )
        self.meta_division.divisions = [tournaments[0].divisions[0],tournaments[1].divisions[0]]        
               
    def test_to_dict_simple(self):
        returned_meta_division_dict = self.meta_division.to_dict_simple()        
        for value in self.meta_division.__table__.columns:
            key =  str(value)[str(value).index('.')+1:]            
            self.assertTrue(key in returned_meta_division_dict,"did not find %s"%key)        
    
        self.assertEquals(returned_meta_division_dict['divisions'][0]['division_id'],0)
        self.assertEquals(returned_meta_division_dict['divisions'][1]['division_id'],1)
