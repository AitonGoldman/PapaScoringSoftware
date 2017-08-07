import unittest
from pss_models import ImportedTables
from lib.DbInfo import DbInfo
from mock import MagicMock
from flask_sqlalchemy import SQLAlchemy

class PssUnitTestBase(unittest.TestCase):    
    def __init__(self,*args, **kwargs):
        super(PssUnitTestBase, self).__init__(*args, **kwargs)                        
        self.db_handle = SQLAlchemy()
        self.tables = ImportedTables(self.db_handle,'test_app','test_pss_amin_app')        
        self.mock_app = MagicMock()                

