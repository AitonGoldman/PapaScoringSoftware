import unittest
from td_types import ImportedTables
from util import db_util

class ModelMachineTD(unittest.TestCase):
    def setUp(self):        
        self.db_handle = db_util.create_db_handle_no_app()        
        self.tables = ImportedTables(self.db_handle)
        self.machine = self.tables.Machine(
            machine_name='test_machine'
        )
        #self.db_handle.session.add(self.division)
        self.machine_dict = {'machine_name':'test_machine',
                             'machine_id':'1',
                             'search_name':None,
                             'abbreviation':None,
                             'year':None
        }
    
            
    def test_to_dict_simple(self):
        for value in self.machine.__table__.columns:
            key =  str(value)[str(value).index('.')+1:]            
            self.assertTrue(key in self.machine_dict,"did not find %s"%key)        

        
