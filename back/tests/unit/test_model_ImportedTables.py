import unittest
from mock import MagicMock
from util import db_util
#import util.db_util
from td_types import ImportedTables
from flask_sqlalchemy import SQLAlchemy


class ModelImportedTablesTD(unittest.TestCase):

    def setUp(self):
        self.db_handle = db_util.create_db_handle_no_app()        
        self.tables = ImportedTables(self.db_handle)

    def test_ImportedTables(self):
        self.assertTrue(hasattr(self.tables,'Role'))
        self.assertTrue(self.tables.Role.__name__ == 'Role')

        self.assertTrue(hasattr(self.tables,'User'))
        self.assertTrue(self.tables.User.__name__ == 'User')

        self.assertTrue(hasattr(self.tables,'db_handle'))
        self.assertTrue(type(self.tables.db_handle) is SQLAlchemy)
        
        self.assertTrue(hasattr(self.tables,'Tournament'))
        self.assertTrue(self.tables.Tournament.__name__ == 'Tournament')

        self.assertTrue(hasattr(self.tables,'Division'))
        self.assertTrue(self.tables.Division.__name__ == 'Division')
        
        
