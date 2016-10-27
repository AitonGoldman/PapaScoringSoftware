import unittest
from td_types import ImportedTables
from util import db_util

class ModelUserTD(unittest.TestCase):
    def setUp(self):        
        self.db_handle = db_util.create_db_handle_no_app()        
        self.tables = ImportedTables(self.db_handle)
        self.user_with_roles = self.tables.User(
            username='test_user_with_roles')
        self.role = self.tables.Role()
        self.role.name = "new_role"
        self.user_with_roles.roles=[self.role]        
        self.user_with_roles.roles=[self.role]        
        self.user = self.tables.User(
            username='test_user')        
        self.user_with_roles.user_id=1
        
    def test_crypt_password(self):                 
        password=self.user.crypt_password('password_test')
        self.assertTrue(password != "password_test")   
        self.user.password=self.user.crypt_password('password_test')
        self.assertTrue(self.user.verify_password('password_test'))
        self.assertFalse(self.user.verify_password('password_not_test'))

    def test_user_auth(self):
        self.assertTrue(self.user.is_authenticated())   
        self.assertTrue(self.user.is_active())   
        self.assertFalse(self.user.is_anonymous())           
        
    def test_to_dict_simple(self):         
        user_dict = {'username':'test_user_with_roles','user_id':1, 'roles':['new_role']}
        self.user.password=self.user.crypt_password('password_two')
        simple_dict = self.user_with_roles.to_dict_simple()
        self.assertDictEqual(user_dict,simple_dict)
