import unittest
from td_types import ImportedTables
from util import db_util
from td_unit_test_base import TdUnitTestBase
class ModelAuditLogTD(TdUnitTestBase):
    def setUp(self):        
        self.db_handle = db_util.create_db_handle_no_app()        
        self.tables = ImportedTables(self.db_handle)
        self.create_single_division_tournament()
        self.create_division_machine()
        self.player = self.create_player()
        self.create_team()
        self.create_token()
        self.create_audit_log()    
            
    def test_to_dict_simple(self):
        simple_dict = self.audit_log.to_dict_simple()
        for value in self.audit_log.__table__.columns:
            key =  str(value)[str(value).index('.')+1:]            
            self.assertTrue(key in simple_dict,"%s is not in dict" % key)
        
        

        
