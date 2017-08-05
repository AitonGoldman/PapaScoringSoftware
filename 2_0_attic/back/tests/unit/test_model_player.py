import unittest
from td_types import ImportedTables
from util import db_util
from td_unit_test_base import TdUnitTestBase

class ModelPlayerTD(TdUnitTestBase):
    def setUp(self):        
        self.db_handle = db_util.create_db_handle_no_app()        
        self.tables = ImportedTables(self.db_handle)
        self.role = self.create_role("new_role")
        self.create_single_division_tournament()
        self.create_division_machine()
        self.player = self.create_player(1)

    def test_player_auth(self):
        self.assertTrue(self.player.is_authenticated())   
        self.assertTrue(self.player.is_active())   
        self.assertFalse(self.player.is_anonymous())           
        
    def test_to_dict_simple(self):                 
        simple_dict_with_roles = self.player.to_dict_simple()        
        for value in self.player.__table__.columns:
            key =  str(value)[str(value).index('.')+1:]            
            self.assertTrue(key in simple_dict_with_roles,"oops - did not find %s" % key)        
        self.assertTrue('roles' in simple_dict_with_roles)
        self.assertEquals(len(simple_dict_with_roles['roles']),1)
        self.assertEquals(simple_dict_with_roles['linked_division_name'],'test_tournament')
        self.assertEquals(simple_dict_with_roles['division_machine']['division_machine_id'],1)
