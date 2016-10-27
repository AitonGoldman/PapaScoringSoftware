import unittest
from mock import MagicMock
from sqlalchemy_utils import database_exists
from util import db_util, td_config
from util.db_info import DbInfo
from flask import Flask
import td_integration_test_base
class UtilDbUtilTD(td_integration_test_base.TdIntegrationDispatchTestBase):
    def test_create_db_and_tables_sqlite(self):
        dummy_app = Flask('dummy_app')
        td_config.assign_loaded_configs_to_app(dummy_app)
        db_url = 'sqlite:////%s' % self.poop_db_file_name
        self.assertFalse(hasattr(dummy_app,'tables'),
                         "Found ImportedTables in app when we should not have")
        db_util.create_db_and_tables(dummy_app,
                                     self.poop_db_name,
                                     DbInfo({'DB_TYPE':'sqlite'}))
        self.assertTrue(database_exists(db_url),
                        "Database %s does not exist" % self.poop_db_name)            
        self.assertTrue(hasattr(dummy_app,'tables'),
                        "No ImportedTables in app when there should be")

        new_user = dummy_app.tables.User(username='testuser')
        dummy_app.tables.db_handle.session.add(new_user)
        dummy_app.tables.db_handle.session.commit()
        self.assertIsNotNone(dummy_app.tables.User.query.filter_by(user_id=new_user.user_id).first(),
                             "Could not find user in newly created DB")
        db_util.create_db_and_tables(dummy_app,self.poop_db_name,
                                     DbInfo({'DB_TYPE':'sqlite'}),
                                     drop_tables=True)        
        self.assertTrue(database_exists(db_url),
                        "Database %s does not exist" % self.poop_db_name)            
        self.assertTrue(hasattr(dummy_app,'tables'),
                        "No ImportedTables in app when there should be")
        self.assertIsNone(dummy_app.tables.User.query.filter_by(user_id=new_user.user_id).first(),
                             "Found user in newly created DB when we should not have")
        del dummy_app

    #FIXME : this should actually do something
    def test_create_db_and_tables_postgres(self):
        pass
        
