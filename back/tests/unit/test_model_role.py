import unittest
from td_types import ImportedTables
from util import db_util

class ModelRoleTD(unittest.TestCase):
    def setUp(self):        
        self.db_handle = db_util.create_db_handle_no_app()        
        self.tables = ImportedTables(self.db_handle)
        self.user_with_roles = self.tables.User(
            username='test_user_with_roles')
        self.role = self.tables.Role()
        self.role.name = "new_role"
        self.role.role_id = 1
                
    def test_to_dict_simple(self):        
        simple_dict = self.role.to_dict_simple()
        for value in self.role.__table__.columns:
            key =  str(value)[str(value).index('.')+1:]            
            self.assertTrue(key in simple_dict,"oops - did not find %s" % key)
        
