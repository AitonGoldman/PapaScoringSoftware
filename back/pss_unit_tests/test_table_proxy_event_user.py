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
                
    def test_create_event_user(self):        
        self.set_mock_single_query(self.tables_proxy,'Events',self.sqlalchemy_event)        
        return_value = self.tables_proxy.create_event_user(self.sqlalchemy_pss_user,1,[1])
        self.assertEquals(return_value,self.sqlalchemy_event_user)
        self.assertEquals(return_value.event_id,1)                                                        

    def test_create_event_user_with_password(self):        
        self.set_mock_single_query(self.tables_proxy,'Events',self.sqlalchemy_event)        
        return_value = self.tables_proxy.create_event_user(self.sqlalchemy_pss_user,1,password='1234')        
        return_value.crypt_password.assert_called_once_with('1234')

    def test_update_event_user_roles(self):
        self.sqlalchemy_event.event_id=1
        self.sqlalchemy_event_role.event_role_id=1
        self.set_mock_single_query(self.tables_proxy,'EventRoles',self.sqlalchemy_event_role)        
        self.tables_proxy.update_event_user_roles([1],1,self.sqlalchemy_pss_user)
        self.assertEquals(self.sqlalchemy_pss_user.event_roles[0].event_role_id,1)
        
