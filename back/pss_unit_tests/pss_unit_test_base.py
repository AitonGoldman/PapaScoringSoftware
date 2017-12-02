import unittest
from flask_sqlalchemy import SQLAlchemy
from mock import MagicMock
from lib_v2.TableProxy import TableProxy


class MockRequest():
    def __init__(self,data):
        self.data=data

class PssUnitTestBase(unittest.TestCase):    
    def __init__(self,*args, **kwargs):
        super(PssUnitTestBase, self).__init__(*args, **kwargs)                        
        self.tables_proxy = TableProxy()        
        self.tables_proxy.db_handle=MagicMock()
    
    def set_mock_single_user_query(self,tables_proxy,pss_user_to_return):
        tables_proxy.PssUsers.query.filter_by().first.return_value=pss_user_to_return
        
