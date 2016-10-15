import unittest
from app.util import db_util
from mock import MagicMock
from flask_sqlalchemy import SQLAlchemy
from app.util.pg_info import PgInfo

class UtilDbUtilTD(unittest.TestCase):
    def setUp(self):
        pass
    def test_generate_db_url(self):        
        sqlite_url = db_util.generate_db_url('test',use_sqlite=True)
        pg_info = PgInfo(pg_username='user',pg_password='password')
        postgres_url = db_util.generate_db_url('test',pg_info=pg_info)
        self.assertEqual(sqlite_url,'sqlite:////tmp/test.db')
        self.assertEqual(postgres_url,'postgresql://%s:%s@localhost/test' % ('user','password'))
    def test_generate_db_url_with_no_db_name(self):
        with self.assertRaises(Exception):
            db_util.generate_db_url(None)
    def test_create_db_handle_no_app(self):
        db_handle = db_util.create_db_handle_no_app()        
        self.assertTrue(type(db_handle) is SQLAlchemy)
        pass
    def test_check_table_exists(self):
        db_handle_with_role = MagicMock()
        db_handle_without_role = MagicMock()

        db_handle_with_role.metadata.tables = {'role': None}        
        db_handle_without_role.metadata.tables = {}
        self.assertTrue(db_util.check_table_exists(db_handle_with_role))
        self.assertFalse(db_util.check_table_exists(db_handle_without_role))
    def test_create_TD_tables(self):
        db_handle = MagicMock()
        db_handle_drop_tables = MagicMock()
        db_util.create_TD_tables(db_handle)
        self.assertTrue(db_handle.create_all.call_count == 1)
        self.assertTrue(db_handle.drop_all.call_count == 0)        
        db_util.create_TD_tables(db_handle_drop_tables, drop_tables=True)
        self.assertTrue(db_handle_drop_tables.create_all.call_count == 1)
        self.assertTrue(db_handle_drop_tables.drop_all.call_count == 1)
    
        
