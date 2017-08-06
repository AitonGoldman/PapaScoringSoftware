import unittest
from pss_models import ImportedTables
from lib import db_util
from mock import MagicMock

class PssUnitTestBase(unittest.TestCase):    
    def __init__(self,*args, **kwargs):
        super(PssUnitTestBase, self).__init__(*args, **kwargs)
        self.db_handle = db_util.create_db_handle_no_app()        
        self.tables = ImportedTables(self.db_handle,'test_app','test_pss_amin_app')        
        self.mock_app = MagicMock()                

