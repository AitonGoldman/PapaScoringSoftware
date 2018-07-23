import unittest
from mock import MagicMock
from pss_unit_test_base import PssUnitTestBase
from flask_sqlalchemy import SQLAlchemy
from pss_models_v2 import Tournaments, Events, MultiDivisionTournaments

class TablesProxyTournamentTest(PssUnitTestBase):        
    def setUp(self):                
        self.sqlalchemy_multi_div_tournament=self.initialize_single_sqlalchemy(self.tables_proxy,"MultiDivisionTournaments",MultiDivisionTournaments.generate_multi_division_tournaments_class,True)        
        self.sqlalchemy_event=self.initialize_single_sqlalchemy(self.tables_proxy,"Events",Events.generate_events_class,True)        

    def test_get_tournament_by_tournament_id(self):                
        self.sqlalchemy_tournament=self.initialize_single_sqlalchemy(self.tables_proxy,"Tournaments",Tournaments.generate_tournaments_class,True)        
        self.set_mock_single_query(self.tables_proxy,"Tournaments",self.sqlalchemy_tournament)        
        return_value = self.tables_proxy.get_tournament_by_tournament_id(1)
        self.assertEquals(return_value,self.sqlalchemy_tournament)        
        filter_by = self.tables_proxy.Tournaments.query.filter_by
        self.assertTrue('tournament_id' in filter_by.call_args[1])
        self.assertEquals(filter_by.call_args[1]['tournament_id'],1)
                
    def test_create_tournament(self):
        self.sqlalchemy_tournament=self.initialize_single_sqlalchemy(self.tables_proxy,"Tournaments",Tournaments.generate_tournaments_class,True)                
        self.sqlalchemy_tournament.tournament_id=1
        self.set_mock_single_query(self.tables_proxy,"Events",self.sqlalchemy_event)        
        tournament_input_info={
            'tournament_name':'test_tournament'            
        }
        return_value = self.tables_proxy.create_tournament(tournament_input_info,2)
        self.assertEquals(self.sqlalchemy_tournament.tournament_id,1)
        self.assertEquals(self.sqlalchemy_tournament.event_id,2)        
        self.assertEquals(self.sqlalchemy_tournament.tournament_name,'test_tournament')

    def test_create_multi_division_tournament(self):                
        self.sqlalchemy_multi_div_tournaments=self.initialize_multiple_sqlalchemy(self.tables_proxy,"Tournaments",Tournaments.generate_tournaments_class,4,True)
        self.set_mock_single_query(self.tables_proxy,"Events",self.sqlalchemy_event)        
        tournament_input_info={
            'queuing':True            
        }
        return_value = self.tables_proxy.create_multi_division_tournament("test_multi",4,tournament_input_info,2)        
        self.assertEquals(len(return_value),4)
        for i in range(0,4):
            self.assertEquals(self.sqlalchemy_multi_div_tournaments[i],return_value[i])                        
            self.assertEquals(return_value[i].queuing,True)                        
            self.assertEquals(return_value[i].multi_division_tournament,self.sqlalchemy_multi_div_tournament)
            self.assertEquals(return_value[i].event_id,2)        
            
        
    def test_edit_tournament(self):                
        self.sqlalchemy_tournament=self.initialize_single_sqlalchemy(self.tables_proxy,"Tournaments",Tournaments.generate_tournaments_class,True)                
        self.sqlalchemy_tournament.tournament_id=1
        self.set_mock_single_query(self.tables_proxy,"Tournaments",self.sqlalchemy_tournament)        
        tournament_input_info={
            'tournament_id':'1',
            'tournament_name':'test_tournament_new'            
        }
        return_value = self.tables_proxy.edit_tournament(tournament_input_info)                
        self.assertEquals(self.sqlalchemy_tournament.tournament_name,'test_tournament_new')
        

        
