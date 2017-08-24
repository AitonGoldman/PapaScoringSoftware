import unittest
from mock import MagicMock
from pss_unit_test_base import PssUnitTestBase
from lib.flask_lib import app_build
from lib import CustomJsonEncoder
from flask import Flask
from flask_principal import Principal
from lib.PssConfig import PssConfig
from routes import token
from lib import roles_constants,orm_factories
import json
from werkzeug.exceptions import BadRequest,Unauthorized

class RouteTokenTest(PssUnitTestBase):
    def setUp(self):
        self.mock_request = MagicMock()        
        self.mock_tables = MagicMock()
        self.mock_event = MagicMock()
        self.mock_pss_config = MagicMock()
        self.mock_app.tables = self.mock_tables
        
    def test_calculate_list_of_tickets_and_prices_for_player(self):
        mock_tournament = MagicMock()
        mock_player = MagicMock()
        mock_tournament.minimum_number_of_tickets_allowed=1
        mock_tournament.number_of_unused_tickets_allowed=15
        mock_tournament.ticket_increment_for_each_purchase=1
        mock_tournament.number_of_tickets_for_discount=None
        mock_tournament.use_stripe=False
        mock_tournament.manually_set_price=3
        mock_tournament.discount_price=None

        expected_ticket_and_price_list=[{ 'amount':0, 'price':0 }, { 'amount':1, 'price':3 },
                                        { 'amount':2, 'price':6 }, { 'amount':3, 'price':9 },
                                        { 'amount':4, 'price':12 }, { 'amount':5, 'price':15 },
                                        { 'amount':6, 'price':18 }, { 'amount':7, 'price':21 },
                                        { 'amount':8, 'price':24 }, { 'amount':9, 'price':27 },
                                        { 'amount':10, 'price':30 }, { 'amount':11, 'price':33 },
                                        { 'amount':12, 'price':36 }, { 'amount':13, 'price':39 },
                                        { 'amount':14, 'price':42 }, { 'amount':15, 'price':45 }]
        returned_ticket_and_price_list=token.calculate_list_of_tickets_and_prices_for_player(0,
                                                                                             mock_player,
                                                                                             self.mock_app,
                                                                                             tournament=mock_tournament)
                
        self.assertEquals(returned_ticket_and_price_list,expected_ticket_and_price_list)

        expected_ticket_and_price_list=expected_ticket_and_price_list[:15]
        returned_ticket_and_price_list=token.calculate_list_of_tickets_and_prices_for_player(1,
                                                                                             mock_player,
                                                                                             self.mock_app,
                                                                                             tournament=mock_tournament)
        self.assertEquals(returned_ticket_and_price_list,expected_ticket_and_price_list)

        expected_ticket_and_price_list=expected_ticket_and_price_list[0:1]
        returned_ticket_and_price_list=token.calculate_list_of_tickets_and_prices_for_player(15,
                                                                                             mock_player,
                                                                                             self.mock_app,
                                                                                             tournament=mock_tournament)
        self.assertEquals(returned_ticket_and_price_list,expected_ticket_and_price_list)
        
    def test_calculate_list_of_tickets_and_prices_for_player_with_discount(self):
        mock_tournament = MagicMock()
        mock_player = MagicMock()
        mock_tournament.minimum_number_of_tickets_allowed=1
        mock_tournament.number_of_unused_tickets_allowed=15
        mock_tournament.ticket_increment_for_each_purchase=1
        mock_tournament.number_of_tickets_for_discount=3
        mock_tournament.use_stripe=False
        mock_tournament.manually_set_price=3
        mock_tournament.discount_price=8

        expected_ticket_and_price_list=[{ 'amount':0, 'price':0 }, { 'amount':1, 'price':3 },
                                        { 'amount':2, 'price':6 }, { 'amount':3, 'price':8 },
                                        { 'amount':4, 'price':11 }, { 'amount':5, 'price':14 },
                                        { 'amount':6, 'price':16 }, { 'amount':7, 'price':19 },
                                        { 'amount':8, 'price':22 }, { 'amount':9, 'price':24 },
                                        { 'amount':10, 'price':27 }, { 'amount':11, 'price':30 },
                                        { 'amount':12, 'price':32 }, { 'amount':13, 'price':35 },
                                        { 'amount':14, 'price':38 }, { 'amount':15, 'price':40 }]
        returned_ticket_and_price_list=token.calculate_list_of_tickets_and_prices_for_player(0,
                                                                                             mock_player,
                                                                                             self.mock_app,
                                                                                             tournament=mock_tournament)
                
        self.assertEquals(returned_ticket_and_price_list,expected_ticket_and_price_list)

        mock_tournament.use_stripe=True
        mock_tournament.discount_stripe_price=9
        mock_tournament.stripe_price=4

        expected_ticket_and_price_list=[{ 'amount':0, 'price':0 }, { 'amount':1, 'price':4 },
                                        { 'amount':2, 'price':8 }, { 'amount':3, 'price':9 },
                                        { 'amount':4, 'price':13 }, { 'amount':5, 'price':17 },
                                        { 'amount':6, 'price':18 }, { 'amount':7, 'price':22 },
                                        { 'amount':8, 'price':26 }, { 'amount':9, 'price':27 },
                                        { 'amount':10, 'price':31 }, { 'amount':11, 'price':35 },
                                        { 'amount':12, 'price':36 }, { 'amount':13, 'price':40 },
                                        { 'amount':14, 'price':44 }, { 'amount':15, 'price':45 }]

        
        returned_ticket_and_price_list=token.calculate_list_of_tickets_and_prices_for_player(0,
                                                                                             mock_player,
                                                                                             self.mock_app,
                                                                                             tournament=mock_tournament)
        self.assertEquals(returned_ticket_and_price_list,expected_ticket_and_price_list)
         
    def test_calculate_list_of_tickets_and_prices_for_player_with_increment_of_two_and_minimum_ticket_of_two(self):
        mock_tournament = MagicMock()
        mock_player = MagicMock()
        mock_tournament.minimum_number_of_tickets_allowed=2
        mock_tournament.number_of_unused_tickets_allowed=15
        mock_tournament.ticket_increment_for_each_purchase=1
        mock_tournament.number_of_tickets_for_discount=8
        mock_tournament.use_stripe=False
        mock_tournament.manually_set_price=3
        mock_tournament.discount_price=22
        expected_ticket_and_price_list=[{ 'amount':0, 'price':0 }, 
                                        { 'amount':2, 'price':6 }, { 'amount':3, 'price':9 },
                                        { 'amount':4, 'price':12 }, { 'amount':5, 'price':15 },
                                        { 'amount':6, 'price':18 }, { 'amount':7, 'price':21 },
                                        { 'amount':8, 'price':22 }, { 'amount':9, 'price':25 },
                                        { 'amount':10, 'price':28 }, { 'amount':11, 'price':31 },
                                        { 'amount':12, 'price':34 }, { 'amount':13, 'price':37 },
                                        { 'amount':14, 'price':40 }, { 'amount':15, 'price':43 }]
        returned_ticket_and_price_list=token.calculate_list_of_tickets_and_prices_for_player(0,
                                                                                             mock_player,
                                                                                             self.mock_app,
                                                                                             tournament=mock_tournament)
        
        self.assertEquals(returned_ticket_and_price_list,expected_ticket_and_price_list)

        mock_tournament.number_of_unused_tickets_allowed=16
        mock_tournament.ticket_increment_for_each_purchase=2
        expected_ticket_and_price_list=[{ 'amount':0, 'price':0 }, 
                                        { 'amount':2, 'price':6 }, 
                                        { 'amount':4, 'price':12 }, 
                                        { 'amount':6, 'price':18 }, 
                                        { 'amount':8, 'price':22 }, 
                                        { 'amount':10, 'price':28 },
                                        { 'amount':12, 'price':34 },
                                        { 'amount':14, 'price':40 },
                                        { 'amount':16, 'price':44 }]
        
        returned_ticket_and_price_list=token.calculate_list_of_tickets_and_prices_for_player(0,
                                                                                             mock_player,
                                                                                             self.mock_app,
                                                                                             tournament=mock_tournament)
        self.assertEquals(returned_ticket_and_price_list,expected_ticket_and_price_list)
 

    
    
