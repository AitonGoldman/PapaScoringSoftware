import unittest
from td_types import ImportedTables
from util import db_util
from td_unit_test_base import TdUnitTestBase
class ModelDivisionTD(TdUnitTestBase):
    def setUp(self):        
        self.db_handle = db_util.create_db_handle_no_app()        
        self.tables = ImportedTables(self.db_handle)
        self.create_single_division_tournament()                
            
    def test_to_dict_simple(self):
        simple_dict = self.division.to_dict_simple()
        for value in self.division.__table__.columns:
            key =  str(value)[str(value).index('.')+1:]            
            self.assertTrue(key in simple_dict)
        
    def test_to_dict_tournament_with_single_divisions(self):                
        self.division.tournament.single_division = True                
        simple_dict = self.division.to_dict_simple()
        self.assertEquals(simple_dict['tournament_name'],'test_tournament')
        self.assertEquals(simple_dict['single_division'], True)

    def test_to_dict_tournament_with_multiple_divisions(self):                
        self.division.tournament.single_division = False
        simple_dict = self.division.to_dict_simple()
        self.assertEquals(simple_dict['tournament_name'],'test_tournament, all')
        self.assertEquals(simple_dict['single_division'], False)
        
        

        
