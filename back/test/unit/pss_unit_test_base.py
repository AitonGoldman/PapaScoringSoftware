import unittest
from pss_models import ImportedTables
from lib.DbInfo import DbInfo
from mock import MagicMock
from flask_sqlalchemy import SQLAlchemy

class PssUnitTestBase(unittest.TestCase):    
    def __init__(self,*args, **kwargs):
        super(PssUnitTestBase, self).__init__(*args, **kwargs)                        
        self.db_handle = SQLAlchemy()
        #FIXME : need constants for these strings
        self.tables = ImportedTables(self.db_handle,'test_app','test_pss_amin_app')        
        self.mock_app = MagicMock()                
    def create_mock_role(self,role_name):
        mock_role = MagicMock()
        mock_role.name = role_name
        return mock_role   
    def create_mock_user(self,role_names,is_pss_admin_user=True):
        mock_user = MagicMock()        
        mock_user.roles=[]
        mock_user.event_roles=[]
        for role_name in role_names:
            mock_role = self.create_mock_role(role_name)
            if is_pss_admin_user:
                mock_user.roles.append(mock_role)
            else:
                mock_user.event_roles.append(mock_role)
                
        mock_user.verify_password.return_value=True            
        return mock_user

