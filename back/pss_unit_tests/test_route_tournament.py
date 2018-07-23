import unittest
from mock import MagicMock
from pss_unit_test_base import PssUnitTestBase,MockRequest
from routes_v2 import tournament
from werkzeug.exceptions import BadRequest,Unauthorized

class RoutePssUserTest(PssUnitTestBase):            

    def setUp(self):
        self.mock_tournaments=self.initialize_multiple_mocks(self.tables_proxy,'Tournaments',2)        
        
    def test_create_tournament(self):
        self.tables_proxy=MagicMock()        
        self.tables_proxy.create_tournament.return_value=self.mock_tournaments[0]        
        mock_request=MockRequest('{"multi_division_tournament":false,"tournament":""}')
        new_tournament = tournament.create_tournament_route(mock_request,self.tables_proxy,1)        
        self.assertEquals(new_tournament[0],self.mock_tournaments[0])        
        self.assertEquals(self.tables_proxy.create_tournament.call_count,1)
        self.assertEquals(self.tables_proxy.create_multi_division_tournament.call_count,0)

    def test_create_multi_division_tournament(self):
        self.tables_proxy=MagicMock()        
        self.tables_proxy.create_multi_division_tournament.return_value=self.mock_tournaments        
        mock_request=MockRequest('{"multi_division_tournament":true,"multi_division_tournament_name":"test_tournament","division_count":"2","tournament":""}')
        new_tournament = tournament.create_tournament_route(mock_request,self.tables_proxy,1)        
        self.assertEquals(new_tournament[0],self.mock_tournaments[0])        
        self.assertEquals(new_tournament[1],self.mock_tournaments[1])         
        self.assertEquals(self.tables_proxy.create_tournament.call_count,0)
        self.assertEquals(self.tables_proxy.create_multi_division_tournament.call_count,1)
        
    def test_edit_tournament(self):
        self.tables_proxy=MagicMock()        
        self.tables_proxy.edit_tournament.return_value=self.mock_tournaments[0]        
        self.mock_app=MagicMock()
        self.mock_app.table_proxy=self.tables_proxy
        mock_request=MockRequest('{}')
        edited_tournament = tournament.edit_tournament_route(mock_request,self.mock_app,1)        
        self.assertEquals(edited_tournament,self.mock_tournaments[0])                
        self.assertEquals(self.tables_proxy.clear_stripe_prices_from_tournament.call_count,1)

    def test_edit_tournament_with_stripe(self):
        self.tables_proxy=MagicMock()        
        self.stripe_proxy=MagicMock()
        self.mock_app=MagicMock()
        self.mock_app.stripe_proxy=self.stripe_proxy
        self.mock_app.table_proxy=self.tables_proxy        
        self.tables_proxy.edit_tournament.return_value=self.mock_tournaments[0]        
        mock_request=MockRequest('{"use_stripe":true}')
        edited_tournament = tournament.edit_tournament_route(mock_request,self.mock_app,1)                
        self.assertEquals(edited_tournament,self.mock_tournaments[0])                
        self.assertEquals(self.mock_app.stripe_proxy.set_tournament_stripe_prices.call_count,1)
        
