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

def generate_mock_tournament(tournament_id=None,meta_tournament_id=None):
    mock_tournament = MagicMock()        
    mock_tournament.number_of_tickets_for_discount=None
    if tournament_id:
        mock_tournament.tournament_name="test tournament"
    if meta_tournament_id:
        mock_tournament.meta_tournament_name="test meta tournament"
        
    mock_tournament.team_tournament=False
    mock_tournament.minimum_number_of_tickets_allowed=1
    mock_tournament.number_of_unused_tickets_allowed=15
    mock_tournament.ticket_increment_for_each_purchase=1
    mock_tournament.use_stripe=False
    mock_tournament.manually_set_price=3
    mock_tournament.ifpa_rank_restriction=None
    if tournament_id:
        mock_tournament.tournament_id=tournament_id
    if meta_tournament_id:
        mock_tournament.meta_tournament_id=meta_tournament_id
    return mock_tournament

class RouteTokenTest(PssUnitTestBase):
    def setUp(self):
        self.mock_request = MagicMock()        
        self.mock_tables = MagicMock()
        self.mock_event = MagicMock()
        self.mock_pss_config = MagicMock()
        self.mock_app.tables = self.mock_tables
        self.mock_token_purchase = MagicMock()
        self.mock_token_purchase_summary = MagicMock()
        self.mock_token = MagicMock()                
        self.mock_tournament_machine=MagicMock()
        self.mock_tournament=generate_mock_tournament(tournament_id=1)        
        self.mock_meta_tournament=generate_mock_tournament(meta_tournament_id=1)        
    
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
     

    #FIXME : split into seperate tests
    def test_insert_tokens_into_db(self):
        self.mock_player = self.create_mock_player(roles_constants.PSS_PLAYER)

        self.mock_tournament_machine.player_id=None        
        self.mock_player.player_id=1
#        self.mock_player.ifpa_ranking=9999
        self.mock_player.event_player.team_id=None

        self.mock_tables.TournamentMachines.query.filter_by().first.retrun_value=MagicMock()
        self.mock_tables.Tokens.return_value = self.mock_token
        self.mock_tables.TokenPurchases.return_value = self.mock_token_purchase
        self.mock_tables.TokenPurchaseSummaries.return_value = self.mock_token_purchase_summary                        
        self.mock_tables.TournamentMachines.query.filter_by().first.return_value=None        

        mock_tournaments_dict={1:self.mock_tournament,2:self.mock_tournament}
        mock_list_of_tournament_tokens=[{'tournament_id':1,'token_count':1}]
        purchase_summary = token.insert_tokens_into_db(mock_list_of_tournament_tokens,mock_tournaments_dict,'tournament',self.mock_player,self.mock_app,self.mock_token_purchase)

        self.assertEquals(len(purchase_summary),1)
        self.assertEquals(purchase_summary[0][1],1)
        self.assertEquals(purchase_summary[0][2]['amount'],1)
        self.assertEquals(purchase_summary[0][2]['price'],3)
        self.assertEquals(self.mock_token_purchase_summary.tournament_id,1)
        self.assertEquals(self.mock_token_purchase_summary.token_count,1)
        self.assertEquals(self.mock_token.paid_for,True)        
        self.assertEquals(self.mock_token.comped,False)        
        self.assertEquals(self.mock_token.player_id,1)        
        self.assertEquals(self.mock_token.tournament_id,1)
        self.assertEquals(self.mock_token_purchase.tokens.append.call_count,1)


    def test_insert_tokens_into_db_with_meta_tournament(self):
        self.mock_player = self.create_mock_player(roles_constants.PSS_PLAYER)

        self.mock_tournament_machine.player_id=None        
        self.mock_player.player_id=1
#        self.mock_player.ifpa_ranking=9999
        self.mock_player.event_player.team_id=None

        self.mock_tables.TournamentMachines.query.filter_by().first.retrun_value=MagicMock()
        self.mock_tables.Tokens.return_value = self.mock_token
        self.mock_tables.TokenPurchases.return_value = self.mock_token_purchase
        self.mock_tables.TokenPurchaseSummaries.return_value = self.mock_token_purchase_summary                        
        self.mock_tables.TournamentMachines.query.filter_by().first.return_value=None                
        
        mock_tournaments_dict={1:self.mock_meta_tournament,2:self.mock_meta_tournament}
        mock_list_of_tournament_tokens=[{'meta_tournament_id':1,'token_count':1}]
        purchase_summary = token.insert_tokens_into_db(mock_list_of_tournament_tokens,mock_tournaments_dict,'meta_tournament',self.mock_player,self.mock_app,self.mock_token_purchase)

        self.assertEquals(len(purchase_summary),1)
        self.assertEquals(purchase_summary[0][1],1)
        self.assertEquals(purchase_summary[0][2]['amount'],1)
        self.assertEquals(purchase_summary[0][2]['price'],3)
        self.assertEquals(self.mock_token_purchase_summary.meta_tournament_id,1)
        self.assertEquals(self.mock_token_purchase_summary.token_count,1)
        self.assertEquals(self.mock_token.paid_for,True)        
        self.assertEquals(self.mock_token.comped,False)        
        self.assertEquals(self.mock_token.player_id,1)        
        self.assertEquals(self.mock_token.meta_tournament_id,1)
        self.assertEquals(self.mock_token_purchase.tokens.append.call_count,1)

    def test_insert_tokens_into_db_with_mulitple_tokens(self):        
        self.mock_player = self.create_mock_player(roles_constants.PSS_PLAYER)
        self.mock_player.event_player.team_id=None
        self.mock_tournament_machine.player_id=None        
        self.mock_player.player_id=1

        self.mock_tables.TournamentMachines.query.filter_by().first.retrun_value=MagicMock()
        self.mock_tables.Tokens.return_value = self.mock_token
        self.mock_tables.TokenPurchases.return_value = self.mock_token_purchase
        self.mock_tables.TokenPurchaseSummaries.return_value = self.mock_token_purchase_summary                        
        self.mock_tables.TournamentMachines.query.filter_by().first.return_value=None                
        mock_tournaments_dict={1:self.mock_tournament,2:self.mock_tournament}
        mock_list_of_tournament_tokens=[{'tournament_id':1,'token_count':1},{'tournament_id':2,'token_count':2}]
        purchase_summary = token.insert_tokens_into_db(mock_list_of_tournament_tokens,mock_tournaments_dict,'tournament',self.mock_player,self.mock_app,self.mock_token_purchase)
        self.assertEquals(len(purchase_summary),2)

        self.assertEquals(purchase_summary[0][1],1)
        self.assertEquals(purchase_summary[0][2]['amount'],1)
        self.assertEquals(purchase_summary[0][2]['price'],3)

        self.assertEquals(purchase_summary[1][1],2)
        self.assertEquals(purchase_summary[1][2]['amount'],2)
        self.assertEquals(purchase_summary[1][2]['price'],6)
        
    def test_insert_tokens_into_db_for_teams(self):
        self.mock_player = self.create_mock_player(roles_constants.PSS_PLAYER)
        self.mock_player.event_player.team_id=1
        self.mock_tournament.team_tournament=True
        self.mock_tournament_machine.player_id=None        
        self.mock_player.player_id=1
#        self.mock_player.ifpa_ranking=9999
        
        self.mock_tables.TournamentMachines.query.filter_by().first.retrun_value=MagicMock()
        self.mock_tables.Tokens.return_value = self.mock_token
        self.mock_tables.TokenPurchases.return_value = self.mock_token_purchase
        self.mock_tables.TokenPurchaseSummaries.return_value = self.mock_token_purchase_summary                        
        self.mock_tables.TournamentMachines.query.filter_by().first.return_value=None        

        mock_tournaments_dict={1:self.mock_tournament,2:self.mock_tournament}
        mock_list_of_tournament_tokens=[{'tournament_id':1,'token_count':1}]
        purchase_summary = token.insert_tokens_into_db(mock_list_of_tournament_tokens,mock_tournaments_dict,'tournament',self.mock_player,self.mock_app,self.mock_token_purchase)

        self.assertEquals(len(purchase_summary),1)
        self.assertEquals(purchase_summary[0][1],1)
        self.assertEquals(purchase_summary[0][2]['amount'],1)
        self.assertEquals(purchase_summary[0][2]['price'],3)
        self.assertEquals(self.mock_token_purchase_summary.tournament_id,1)
        self.assertEquals(self.mock_token_purchase_summary.token_count,1)
        self.assertEquals(self.mock_token.paid_for,True)
        self.assertEquals(self.mock_token.team_id,1)                
        self.assertEquals(self.mock_token.comped,False)        
        self.assertEquals(self.mock_token.player_id,1)        
        self.assertEquals(self.mock_token.tournament_id,1)
        self.assertEquals(self.mock_token_purchase.tokens.append.call_count,1)

    def test_insert_tokens_into_db_for_team_tournament_when_player_is_not_in_team(self):
        self.mock_player = self.create_mock_player(roles_constants.PSS_PLAYER)
        self.mock_player.event_player.team_id=None
        self.mock_tournament.team_tournament=True
        self.mock_tournament_machine.player_id=None        
        self.mock_player.player_id=1
#        self.mock_player.ifpa_ranking=9999
        
        self.mock_tables.TournamentMachines.query.filter_by().first.retrun_value=MagicMock()
        self.mock_tables.Tokens.return_value = self.mock_token
        self.mock_tables.TokenPurchases.return_value = self.mock_token_purchase
        self.mock_tables.TokenPurchaseSummaries.return_value = self.mock_token_purchase_summary                        
        self.mock_tables.TournamentMachines.query.filter_by().first.return_value=None        

        mock_tournaments_dict={1:self.mock_tournament,2:self.mock_tournament}
        mock_list_of_tournament_tokens=[{'tournament_id':1,'token_count':1}]
        purchase_summary = token.insert_tokens_into_db(mock_list_of_tournament_tokens,mock_tournaments_dict,'tournament',self.mock_player,self.mock_app,self.mock_token_purchase)

        self.assertEquals(len(purchase_summary),0)
        
    def test_insert_tokens_into_db_with_discounts(self):
        self.mock_player = self.create_mock_player(roles_constants.PSS_PLAYER)
        self.mock_tournament.number_of_tickets_for_discount=3
        self.mock_tournament.discount_price=8
        
        self.mock_tournament_machine.player_id=None        
        self.mock_player.player_id=1
#        self.mock_player.ifpa_ranking=9999
        self.mock_player.event_player.team_id=None
        
        self.mock_tables.TournamentMachines.query.filter_by().first.retrun_value=MagicMock()
        self.mock_tables.Tokens.return_value = self.mock_token
        self.mock_tables.TokenPurchases.return_value = self.mock_token_purchase
        self.mock_tables.TokenPurchaseSummaries.return_value = self.mock_token_purchase_summary                        
        self.mock_tables.TournamentMachines.query.filter_by().first.return_value=None        

        mock_tournaments_dict={1:self.mock_tournament,2:self.mock_tournament}
        mock_list_of_tournament_tokens=[{'tournament_id':1,'token_count':11}]
        purchase_summary = token.insert_tokens_into_db(mock_list_of_tournament_tokens,mock_tournaments_dict,'tournament',self.mock_player,self.mock_app,self.mock_token_purchase)

        self.assertEquals(self.mock_token_purchase_summary.token_count,11)
        self.assertEquals(self.mock_token_purchase.tokens.append.call_count,11)

        
    def test_insert_tokens_into_db_that_is_player_initiated(self):
        self.mock_player = self.create_mock_player(roles_constants.PSS_PLAYER)

        self.mock_tournament_machine.player_id=None        
        self.mock_player.player_id=1
#        self.mock_player.ifpa_ranking=9999
        self.mock_player.event_player.team_id=None

        self.mock_tables.TournamentMachines.query.filter_by().first.retrun_value=MagicMock()        
        self.mock_tables.Tokens.return_value = self.mock_token
        self.mock_tables.TokenPurchases.return_value = self.mock_token_purchase
        self.mock_tables.TokenPurchaseSummaries.return_value = self.mock_token_purchase_summary                        
        self.mock_tables.TournamentMachines.query.filter_by().first.return_value=None        

        mock_tournaments_dict={1:self.mock_tournament,2:self.mock_tournament}
        mock_list_of_tournament_tokens=[{'tournament_id':1,'token_count':1}]
        purchase_summary = token.insert_tokens_into_db(mock_list_of_tournament_tokens,
                                                       mock_tournaments_dict,
                                                       'tournament',
                                                       self.mock_player,
                                                       self.mock_app,
                                                       self.mock_token_purchase,
                                                       player_initiated=True)

        self.assertEquals(len(purchase_summary),1)
        self.assertEquals(self.mock_token_purchase.stripe_purchase,True)
        self.assertEquals(self.mock_token.paid_for,False)        
   
    def test_verify_tournament_and_meta_tournament_request_counts_are_valid(self):
        self.mock_player = self.create_mock_player(roles_constants.PSS_PLAYER)

        self.mock_tournament_machine.player_id=None        
        self.mock_player.player_id=1
        self.mock_player.event_player.team_id=None

        mock_query = MagicMock()
        mock_query.filter_by().count.return_value=1
        self.mock_tables.Tokens.query.filter_by.return_value = mock_query
        mock_tournaments_dict={1:self.mock_tournament,2:self.mock_tournament}
        input_data={}
        input_data['tournament_token_counts']=[{'tournament_id':1,'token_count':0}]
        token.verify_tournament_and_meta_tournament_request_counts_are_valid(input_data, self.mock_player,
                                                                             "tournament", mock_tournaments_dict,
                                                                             self.mock_app)

        input_data['tournament_token_counts']=[{'tournament_id':1,'token_count':1}]
        token.verify_tournament_and_meta_tournament_request_counts_are_valid(input_data, self.mock_player,
                                                                             "tournament", mock_tournaments_dict,
                                                                             self.mock_app)
        
        input_data['tournament_token_counts']=[{'tournament_id':1,'token_count':15}]
        with self.assertRaises(Exception) as cm:                
            token.verify_tournament_and_meta_tournament_request_counts_are_valid(input_data, self.mock_player,
                                                                                 "tournament", mock_tournaments_dict,
                                                                                 self.mock_app)
        self.assertEquals(cm.exception.description,"Fuck off, Ass Wipe")

        self.mock_tables.TournamentMachines.query.filter_by().first.retrun_value=MagicMock()
        
        input_data['tournament_token_counts']=[{'tournament_id':1,'token_count':14}]
        with self.assertRaises(Exception) as cm:                
            token.verify_tournament_and_meta_tournament_request_counts_are_valid(input_data, self.mock_player,
                                                                                 "tournament", mock_tournaments_dict,
                                                                                 self.mock_app)
        self.assertEquals(cm.exception.description,"Fuck off, Ass Wipe")
        
        self.mock_tournament.ifpa_rank_restriction=500
        self.mock_player.event_player.ifpa_ranking=1
        input_data['tournament_token_counts']=[{'tournament_id':1,'token_count':1}]
        with self.assertRaises(Exception) as cm:                
            token.verify_tournament_and_meta_tournament_request_counts_are_valid(input_data, self.mock_player,
                                                                                 "tournament", mock_tournaments_dict,
                                                                                 self.mock_app)
        self.assertEquals(cm.exception.description,"Ifpa restrictions have been violated")
        

    def test_purchase_tickets_route(self):
        self.mock_player = self.create_mock_player(roles_constants.PSS_PLAYER)
        self.mock_audit_log = MagicMock()
        self.mock_audit_log.__table__ = MagicMock()
        
        self.mock_tournament_machine.player_id=None        
        self.mock_player.player_id=1
        self.mock_player.event_player.team_id=None
        #self.mock_meta_tournament.meta_tournament_name='mock meta tournament'
        mock_query = MagicMock()
        mock_query.filter_by().count.return_value=1
        self.mock_tables.Tokens.query.filter_by.return_value = mock_query
        mock_tournaments_dict={1:self.mock_tournament,2:self.mock_tournament}
        
        input_data={}
        input_data['tournament_token_counts']=[{'tournament_id':1,'token_count':2}]
        input_data['meta_tournament_token_counts']=[{'meta_tournament_id':1,'token_count':2}]

        self.mock_tables.MetaTournaments.query.all.return_value=[self.mock_meta_tournament]
        self.mock_tables.Tournaments.query.filter_by().all.return_value=[self.mock_tournament]

        self.mock_tables.TournamentMachines.query.filter_by().first.retrun_value=MagicMock()        
        self.mock_tables.Tokens.return_value = self.mock_token
        self.mock_tables.AuditLogs.return_value = self.mock_audit_log
        
        self.mock_tables.TokenPurchases.return_value = self.mock_token_purchase
        self.mock_tables.TokenPurchaseSummaries.return_value = self.mock_token_purchase_summary                        
        self.mock_tables.TournamentMachines.query.filter_by().first.return_value=None        
        mock_request = MagicMock()
        mock_request.data = json.dumps(input_data)
        
        token_purchase, purchase_summary = token.purchase_tickets_route(mock_request,self.mock_player,self.mock_app)
        self.assertEquals(len(purchase_summary),2)
        self.assertEquals(self.mock_token_purchase.total_cost,12)
        self.assertEquals(self.mock_token_purchase.completed_purchase,True)

        token_purchase, purchase_summary = token.purchase_tickets_route(mock_request,self.mock_player,self.mock_app,player_initiated=True)        
        self.assertEquals(self.mock_token_purchase.completed_purchase,False)

        
        input_data['comped']=True
        mock_request.data = json.dumps(input_data)
        token_purchase, purchase_summary = token.purchase_tickets_route(mock_request,self.mock_player,self.mock_app)        
        self.assertEquals(self.mock_token.comped,True)
        
        
        
        pass
    #FIXME : test to check names of tournaments in summary results?
