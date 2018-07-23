import unittest
from mock import MagicMock
from pss_unit_test_base import PssUnitTestBase
from flask_sqlalchemy import SQLAlchemy


class TablesProxyEventRoles(PssUnitTestBase):        
    def setUp(self):                
        self.sqlalchemy_event_role=self.initialize_single_mock_event_role(self.tables_proxy,True)

    def test_get_event_by_eventname(self):                        
        return_value = self.tables_proxy.create_role('whatever')
        self.assertEquals(return_value,self.sqlalchemy_event_role)
        
