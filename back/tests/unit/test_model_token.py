import unittest
from td_types import ImportedTables
from util import db_util

class ModelTokenTD(unittest.TestCase):
    def setUp(self):        
        self.db_handle = db_util.create_db_handle_no_app()        
        self.tables = ImportedTables(self.db_handle)
        self.token = self.tables.Token(
            token_id=1,
            player_id=1,
            division_id=1,
            team_id=1,
            metadivision_id=1,
            paid_for=False,
            used=False
        )        
        self.token_dict = {'token_id':'1',
                           'division_id':'1',                                      
                           'team_id':'1',
                           'player_id':'1',
                           'metadivision_id':'1',
                           'paid_for':False,
                           'used':False
        }
    
            
    def test_to_dict_simple(self):
        for value in self.token.__table__.columns:
            key =  str(value)[str(value).index('.')+1:]            
            self.assertTrue(key in self.token_dict,"did not find %s"%key)            
