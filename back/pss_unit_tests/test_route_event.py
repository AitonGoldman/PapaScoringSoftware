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
        self.sqlalchemy_pss_user=self.initialize_single_mock_pss_user(self.tables_proxy)
        self.sqlalchemy_event=self.initialize_single_mock_event(self.tables_proxy,True)
        self.sqlalchemy_pss_user.events = []
        
    def test_event_create(self):                                
        self.sqlalchemy_pss_user.pss_user_id=1
        self.sqlalchemy_event.event_id=1
        mock_request=MockRequest('{"name":"test_event"}')
        self.set_mock_single_event_query(self.tables_proxy,None)
        new_event = event.pss_event_create_route(mock_request,self.tables_proxy,self.sqlalchemy_pss_user)
        self.assertEquals(new_event.name,"test_event")
        self.assertEquals(new_event.event_id,1)

    def test_event_create_fails_with_duplicate_name(self):                                
        self.sqlalchemy_pss_user.pss_user_id=1
        self.sqlalchemy_event.event_id=1
        mock_request=MockRequest('{"name":"test_event"}')
        self.set_mock_single_event_query(self.tables_proxy,self.sqlalchemy_event)        
        with self.assertRaises(BadRequest) as cm:        
            event.pss_event_create_route(mock_request,self.tables_proxy,self.sqlalchemy_pss_user)
                        
    def test_event_edit(self):                
        self.set_mock_single_event_query(self.tables_proxy,self.sqlalchemy_event)
        self.sqlalchemy_event.event_id=1
        self.sqlalchemy_event.name="old_event_name"
        self.set_mock_multiple_event_query(self.tables_proxy,[None, self.sqlalchemy_event])
        mock_request=MockRequest('{"event_id":1,"name":"new_test_event"}')
        new_event = event.pss_event_edit_route(mock_request,self.tables_proxy)
        self.assertEquals(new_event.name,"new_test_event")
        self.assertEquals(new_event.event_id,1)

    def test_event_edit_fails_with_duplicate_name(self):                
        self.set_mock_single_event_query(self.tables_proxy,self.sqlalchemy_event)
        self.sqlalchemy_event.event_id=1
        self.sqlalchemy_event.name="old_event_name"
        self.set_mock_single_event_query(self.tables_proxy, self.sqlalchemy_event)
        mock_request=MockRequest('{"event_id":1,"name":"new_test_event"}')
        with self.assertRaises(BadRequest) as cm:        
            new_event = event.pss_event_edit_route(mock_request,self.tables_proxy)
