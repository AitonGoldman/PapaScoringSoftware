import unittest
from mock import MagicMock
from pss_unit_test_base import PssUnitTestBase
from flask_sqlalchemy import SQLAlchemy


class TablesProxyEventUserTest(PssUnitTestBase):        
    def setUp(self):        
        self.sqlalchemy_pss_user=self.initialize_single_mock(self.tables_proxy,'PssUsers')
        self.sqlalchemy_event=self.initialize_single_mock(self.tables_proxy,'Events')
        self.sqlalchemy_event_role=self.initialize_single_mock(self.tables_proxy,'EventRoles')
        self.sqlalchemy_event_user=self.initialize_single_mock(self.tables_proxy,'EventUsers')
        self.sqlalchemy_event_role_mapping=self.initialize_single_mock(self.tables_proxy,'EventRoleMappings')
                
    def test_update_event_user_roles(self):        
        self.sqlalchemy_pss_user.pss_user_id=1
        self.sqlalchemy_event.event_id=1
        self.sqlalchemy_event_role.event_role_id=1
        self.sqlalchemy_event_role_mapping.event_role_id=2
        self.sqlalchemy_pss_user.event_roles.append(self.sqlalchemy_event_role_mapping)        
        self.set_mock_single_query(self.tables_proxy,'EventRoles',self.sqlalchemy_event_role)
        self.set_mock_all_query(self.tables_proxy,'EventRoleMappings',[[self.sqlalchemy_event_role_mapping]])                
        self.tables_proxy.update_event_user_roles([1],1,self.sqlalchemy_pss_user)
        self.assertEquals(self.sqlalchemy_pss_user.event_roles[0].event_role_id,1)        
        self.tables_proxy.db_handle.session.delete.call_count
