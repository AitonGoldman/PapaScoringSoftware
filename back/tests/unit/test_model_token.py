import unittest
from td_types import ImportedTables
from util import db_util
from td_unit_test_base import TdUnitTestBase

class ModelTokenTD(TdUnitTestBase):
    def setUp(self):        
        self.db_handle = db_util.create_db_handle_no_app()        
        self.tables = ImportedTables(self.db_handle)
        self.create_token()
                
    def test_to_dict_simple(self):
        simple_dict=self.token.to_dict_simple()
        for value in self.token.__table__.columns:
            key =  str(value)[str(value).index('.')+1:]            
            self.assertTrue(key in simple_dict,"did not find %s"%key)            
