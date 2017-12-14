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
        self.mock_event_role_mappings=self.initialize_multiple_mocks(self.tables_proxy,'EventRoleMappings',2)
        self.mock_event_role=self.initialize_single_mock(self.tables_proxy,'EventRoles')        
        
    def test_create_event_user_route(self):
        self.tables_proxy=MagicMock()
        self.mock_pss_event.event_id=1
        self.tables_proxy.get_event_by_event_id.return_value=self.mock_pss_event
        self.tables_proxy.get_user_by_id.return_value=None
        self.tables_proxy.get_user_by_username.return_value=None
        self.tables_proxy.update_event_user_roles.return_value=self.mock_pss_users[0]
        self.tables_proxy.create_user.return_value=self.mock_pss_users[0]
        
        mock_request=MockRequest('{"event_role_ids":["1"],"event_users":[{"first_name":"poop_first","last_name":"poop_last"}]}')
        pss_users_added_to_event = pss_user.create_event_user_route(mock_request,self.tables_proxy,1)
        self.assertTrue(len(pss_users_added_to_event)==1)
        self.assertEquals(pss_users_added_to_event[0],self.mock_pss_users[0])        
        self.assertEquals( self.tables_proxy.update_event_user_roles.call_count,1)
        
    def test_create_event_user_route_with_existing_user(self):        
        self.mock_pss_users[0].pss_user_id=None        
        self.mock_pss_users[1].pss_user_id=5        
        self.tables_proxy=MagicMock()
        self.tables_proxy.get_event_by_event_id.return_value=self.mock_pss_event
        self.tables_proxy.get_user_by_id.return_value=self.mock_pss_users[1]
        self.tables_proxy.get_user_by_username.return_value=None
        self.tables_proxy.update_event_user_roles.side_effect=self.mock_pss_users
        self.tables_proxy.create_user.return_value=self.mock_pss_users[0]
        mock_request=MockRequest('{"event_role_ids":["1"],"event_users":[{"first_name":"poop_first","last_name":"poop_last"},{"pss_user_id":"5","first_name":"poop2_first","last_name":"poop2_last"}]}')
        pss_users_added_to_event = pss_user.create_event_user_route(mock_request,self.tables_proxy,1)
        self.assertTrue(len(pss_users_added_to_event)==2)        
        self.assertEquals(pss_users_added_to_event[0].pss_user_id,None)
        self.assertEquals(pss_users_added_to_event[1].pss_user_id,5)
        self.assertEquals( self.tables_proxy.update_event_user_roles.call_count,2)

    def test_edit_event_user_event_role_mapping_route(self):
        self.mock_event_role.event_role_id=2 
        self.mock_pss_users[0].pss_user_id=5    
        self.tables_proxy=MagicMock()
        self.tables_proxy.get_event_by_event_id.return_value=self.mock_pss_event
        self.tables_proxy.get_user_by_id.return_value=self.mock_pss_users[0]        
        self.tables_proxy.update_event_user_roles.return_value=MagicMock()                
        mock_request=MockRequest('{"event_role_ids":["2"],"event_user":{"pss_user_id":"5","first_name":"poop_first","last_name":"poop_last"}}')
        new_pss_user = pss_user.update_event_user_roles_route(mock_request,self.tables_proxy,1)
        self.assertEquals( self.tables_proxy.update_event_user_roles.call_count,1)
        self.assertEquals( self.mock_pss_users[0],new_pss_user)
        
        
