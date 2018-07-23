import unittest
from td_types import ImportedTables
from util import db_util
from td_unit_test_base import TdUnitTestBase

class ModelTournamentTD(TdUnitTestBase):
    def setUp(self):        
        self.db_handle = db_util.create_db_handle_no_app()        
        self.tables = ImportedTables(self.db_handle)
        self.create_multi_division_tournament()
        self.create_single_division_tournament()

    def test_to_dict_simple(self):                 
        simple_dict = self.tournament.to_dict_simple()
        for value in self.tournament.__table__.columns:
            key =  str(value)[str(value).index('.')+1:]            
            self.assertTrue(key in simple_dict,"oops - did not find %s" % key)        

    def test_division_relationship(self):            
        simple_dict = self.tournament.to_dict_simple()        
        self.assertIsNotNone(simple_dict['divisions'])        
        self.assertEquals(simple_dict['active'],True)        
        self.assertEquals(len(simple_dict['divisions']),1)
        
        
        
