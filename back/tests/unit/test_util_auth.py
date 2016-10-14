import unittest
from app.types import ImportedTables
from app.util import db_util
from app.util import auth
from flask import Flask
from flask_principal import Identity
from flask_login import login_user,LoginManager
from mock import MagicMock

class UtilAuthTD(unittest.TestCase):    
    def setUp(self):
        self.app = Flask("dummy")
        self.app.secret_key='poop'
        LoginManager().init_app(self.app)
        self.db_handle = db_util.create_db_handle_no_app()        
        self.tables = ImportedTables(self.db_handle)
        self.app.tables = self.tables
        self.user_with_roles = self.tables.User()
        self.role = self.tables.Role()
        self.role.name = "new_role"
        self.user_with_roles.roles=[self.role]        
        self.id = Identity('dummy')        
        
    def test_on_identity_loaded_callback(self):         
        with self.app.test_request_context():                                        
            login_user(self.user_with_roles)
            self.assertIsNone(getattr(self.id,'user',None))            
            on_identity_loaded_callback = auth.generate_identity_loaded(self.app)            
            self.assertEqual(len(self.id.provides),0)            
            on_identity_loaded_callback(None,self.id)
            self.assertEqual(len(self.id.provides),2)
            self.assertIsNotNone(self.id.user)

    def test_generate_user_loader(self):                 
        self.app.tables=MagicMock()
        self.app.tables.User.query.get.return_value=self.user_with_roles
        with self.app.test_client() as c:            
            user_loader = auth.generate_user_loader(self.app)
            returned_user = user_loader(1)
            self.assertEquals(returned_user,self.user_with_roles)