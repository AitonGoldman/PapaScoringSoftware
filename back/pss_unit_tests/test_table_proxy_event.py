import unittest
from mock import MagicMock
from pss_unit_test_base import PssUnitTestBase
from flask_sqlalchemy import SQLAlchemy


class TablesProxyEventTest(PssUnitTestBase):        
    def setUp(self):        
        self.sqlalchemy_pss_user=self.initialize_single_mock_pss_user(self.tables_proxy)
        self.sqlalchemy_event=self.initialize_single_mock_event(self.tables_proxy,True)

    def test_get_event_by_eventname(self):                
        self.set_mock_single_event_query(self.tables_proxy,self.sqlalchemy_event)        
        return_value = self.tables_proxy.get_event_by_eventname('whatever')
        self.assertEquals(return_value,self.sqlalchemy_event)        
        filter_by = self.tables_proxy.Events.query.filter_by
        self.assertTrue('name' in filter_by.call_args[1])
        self.assertEquals(filter_by.call_args[1]['name'],'whatever')
        
    def test_get_pss_by_username(self):                
        self.set_mock_single_user_query(self.tables_proxy,self.sqlalchemy_pss_user)        
        return_value = self.tables_proxy.get_user_by_username('whatever')
        self.assertEquals(return_value,self.sqlalchemy_pss_user)        
        filter_by = self.tables_proxy.PssUsers.query.filter_by
        self.assertTrue('username' in filter_by.call_args[1])
        self.assertEquals(filter_by.call_args[1]['username'],'whatever')
        
    def test_create_event(self):        
        self.sqlalchemy_pss_user.pss_user_id=1 
        self.sqlalchemy_event.event_id=1
        event_input_info={
            'name':'test_event'            
        }
        return_value = self.tables_proxy.create_event(self.sqlalchemy_pss_user,event_input_info)
        self.assertEquals(self.sqlalchemy_event.event_id,1)
        self.assertEquals(self.sqlalchemy_event.name,'test_event')
        self.assertEquals(self.sqlalchemy_event.event_creator_pss_user_id,1)

        
