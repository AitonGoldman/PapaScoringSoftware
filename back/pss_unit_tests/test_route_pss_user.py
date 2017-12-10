import unittest
from mock import MagicMock
from pss_unit_test_base import PssUnitTestBase,MockRequest
from routes_v2 import pss_user
from werkzeug.exceptions import BadRequest,Unauthorized

class RoutePssUserTest(PssUnitTestBase):            

    def setUp(self):
        self.mock_pss_users=self.initialize_multiple_mocks(self.tables_proxy,'PssUsers',2)        
        self.mock_pss_event_user=self.initialize_single_mock(self.tables_proxy,'EventUsers')        
        self.mock_pss_event=self.initialize_single_mock(self.tables_proxy,'Events')        
        self.mock_event_role_mapping=self.initialize_single_mock(self.tables_proxy,'EventRoleMappings')
        self.mock_event_role=self.initialize_single_mock(self.tables_proxy,'EventRoles')        
        
    def test_create_event_user_route(self):
        self.set_mock_single_query(self.tables_proxy,"Events",self.mock_pss_event)
        self.set_mock_single_query(self.tables_proxy,"PssUsers",None)
        self.set_mock_single_query(self.tables_proxy,"EventRoles",self.mock_event_role)
        mock_request=MockRequest('{"event_role_ids":["1"],"event_users":[{"first_name":"poop_first","last_name":"poop_last"}]}')
        pss_users_added_to_event = pss_user.create_event_user_route(mock_request,self.tables_proxy,1)
        self.assertTrue(len(pss_users_added_to_event)==1)
        self.assertTrue(len(pss_users_added_to_event[0].event_roles)==1)

    def test_create_event_user_route_with_existing_user(self):
        self.mock_event_role.event_role_id=2        
        self.mock_pss_users[0].pss_user_id=5        
        self.mock_pss_users[1].pss_user_id=None        
        
        self.set_mock_single_query(self.tables_proxy,"Events",self.mock_pss_event)
        self.set_mock_multiple_query(self.tables_proxy,"PssUsers",[self.mock_pss_users[0],None])
        self.set_mock_single_query(self.tables_proxy,"EventRoles",self.mock_event_role)
        mock_request=MockRequest('{"event_role_ids":["1"],"event_users":[{"pss_user_id":"5","first_name":"poop_first","last_name":"poop_last"},{"first_name":"poop2_first","last_name":"poop2_last"}]}')
        pss_users_added_to_event = pss_user.create_event_user_route(mock_request,self.tables_proxy,1)
        self.assertTrue(len(pss_users_added_to_event)==2)
        self.assertEquals(pss_users_added_to_event[0].pss_user_id,5)
        self.assertEquals(pss_users_added_to_event[0].event_roles[0].event_role_id,2)        
        self.assertEquals(pss_users_added_to_event[1].pss_user_id,None)
        self.assertEquals(pss_users_added_to_event[0].event_roles[0].event_role_id,2)        
        
        
        
