import unittest
from mock import MagicMock
from pss_unit_test_base import PssUnitTestBase,MockRequest
from pss_models_v2.PssUsers import generate_pss_users_class
from flask_sqlalchemy import SQLAlchemy
from routes_v2 import auth
from werkzeug.exceptions import BadRequest,Unauthorized

class RouteAuthTest(PssUnitTestBase):        
    BAD_CRYPT_PASSWORD="$6$rounds=100000$zvtKLLYyw7v5gGK6$zYSOyslGbz3mLFRfAN/9dCwqvvvT6yO1K1j8J7JB0DchX1ln.juSSIU5GWt3pbfCUTjaA7VJemktG9eQIvFMM."

    def setUp(self):
        self.mock_pss_user=self.initialize_single_mock(self.tables_proxy,'PssUsers')        
        self.mock_pss_user.password_crypt="$6$rounds=100000$zvtKLLYyw7v5gGK6$zYSOyslGbz3mLFRfAN/9dCwqvvvT6yO1K1j8J7JB0DchX1ln.juSSIU5GWt3pbfCUTjgA7VJemktG9eQIvFMM."
        
    def test_pss_login_route_for_event_creator(self):                
        mock_request=MockRequest('{"username":"test_user","password":"password"}')        
        self.mock_pss_user.event_creator=True        
        self.tables_proxy.get_user_by_username=MagicMock()
        self.tables_proxy.get_user_by_username.return_value=self.mock_pss_user
        
        pss_user_found = auth.pss_login_route(mock_request,self.tables_proxy,True)
        self.assertEquals(self.mock_pss_user,pss_user_found)

    def test_pss_login_route_for_event_creator_with_bad_input(self):                
        mock_request=MockRequest('{"username":"test_user","password":"password"}')
        self.mock_pss_user.event_creator=True
                
        self.tables_proxy.get_user_by_username=MagicMock()
        self.tables_proxy.get_user_by_username.return_value=None

        with self.assertRaises(Unauthorized) as cm:        
            auth.pss_login_route(mock_request,self.tables_proxy,True)
            
        self.mock_pss_user.password_crypt=self.BAD_CRYPT_PASSWORD        
        with self.assertRaises(Unauthorized) as cm:        
            auth.pss_login_route(mock_request,self.tables_proxy,True)
            
        self.mock_pss_user.event_creator=False                
        self.tables_proxy.get_user_by_username.return_value=self.mock_pss_user
        with self.assertRaises(Unauthorized) as cm:        
            auth.pss_login_route(mock_request,self.tables_proxy,True)


            
        
    
