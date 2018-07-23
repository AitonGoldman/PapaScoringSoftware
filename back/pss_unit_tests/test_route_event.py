import unittest
from mock import MagicMock
from pss_unit_test_base import PssUnitTestBase,MockRequest
from pss_models_v2.Events import generate_events_class
from pss_models_v2.PssUsers import generate_pss_users_class

from flask_sqlalchemy import SQLAlchemy
from routes_v2 import event
from werkzeug.exceptions import BadRequest,Unauthorized

class RouteEventTest(PssUnitTestBase):            

    def setUp(self):
        #self.mock_pss_user=self.initialize_single_mock(self.tables_proxy,'PssUsers')
        #self.sqlalchemy_event=self.initialize_single_mock_event(self.tables_proxy,True)
        #self.mock_pss_user.events = []
        self.mock_pss_user=self.initialize_single_mock(self.tables_proxy,"PssUsers")
        self.mock_event=self.initialize_single_mock(self.tables_proxy,"Events")
        
    def test_event_create(self):                                                
        mock_request=MockRequest('{"name":"test_event"}')
        self.tables_proxy=MagicMock()
        self.tables_proxy.get_event_by_eventname.return_value=None
        self.tables_proxy.create_event.return_value=self.mock_event        
        new_event = event.pss_event_create_route(mock_request,self.tables_proxy,self.mock_pss_user)
        self.assertEquals(new_event,self.mock_event)
        self.assertEquals(self.tables_proxy.create_event.call_count,1)

    def test_event_create_fails_with_duplicate_name(self):                                
        self.tables_proxy=MagicMock()
        self.mock_event='test_event'
        self.tables_proxy.get_event_by_eventname.return_value=self.mock_event                
        mock_request=MockRequest('{"name":"test_event"}')        
        with self.assertRaises(BadRequest) as cm:        
            event.pss_event_create_route(mock_request,self.tables_proxy,self.mock_pss_user)
                        
    def test_event_edit(self):                
        self.tables_proxy=MagicMock() 
        self.mock_event.name="new_test_event"
        self.tables_proxy.get_event_by_eventname.return_value=None
        self.tables_proxy.edit_event.return_value=self.mock_event        
        mock_request=MockRequest('{"event_id":1,"name":"new_test_event"}')
        new_event = event.pss_event_edit_route(mock_request,self.tables_proxy)
        self.assertEquals(new_event.name,"new_test_event")
        self.assertEquals(new_event,self.mock_event)        

    def test_event_edit_fails_with_duplicate_name(self):                
        self.tables_proxy=MagicMock() 
        self.mock_event.name="new_test_event"
        self.tables_proxy.get_event_by_eventname.return_value=self.mock_event        
        mock_request=MockRequest('{"event_id":1,"name":"new_test_event"}')
        with self.assertRaises(BadRequest) as cm:        
            new_event = event.pss_event_edit_route(mock_request,self.tables_proxy)
