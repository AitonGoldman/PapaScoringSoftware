import unittest
from td_types import ImportedTables
from util import db_util

class ModelDivisionTD(unittest.TestCase):
    def setUp(self):        
        self.db_handle = db_util.create_db_handle_no_app()        
        self.tables = ImportedTables(self.db_handle)
        self.tournament = self.tables.Tournament(
            tournament_id=1,
            tournament_name='test_tournament',
            single_division=True
        )
        self.division = self.tables.Division(
            division_name='a',
            number_of_scores_per_entry=1,                        
            tournament_id=1,
            tournament=self.tournament
        )
        #self.db_handle.session.add(self.division)
        self.division_dict = {'division_name':'a',
                              'active':False,
                              'number_of_scores_per_entry':1,
                              'scoring_type':'HERB',
                              'team_tournament':False,
                              'division_id':None,
                              'meta_division_id':None,
                              'local_price':None,
                              'use_stripe':None,
                              'stripe_sku':None,
                              'finals_player_selection_type':None,
                              'finals_num_qualifiers':None,
                              'finals_num_qualifiers_ppo_a':None,
                              'finals_num_qualifiers_ppo_b':None,
                              'finals_challonge_name_ppo_a':None,
                              'finals_challonge_name_ppo_b':None,
                              'finals_num_players_per_group':None,
                              'finals_num_games_per_match':None,
                              'tournament_id':1,
                              'tournament_name':'test_tournament',
                              'single_division':True
        }
    
            
    def test_to_dict_simple(self):
        for value in self.division.__table__.columns:
            key =  str(value)[str(value).index('.')+1:]            
            self.assertTrue(key in self.division_dict)
        
    def test_to_dict_tournament_with_single_divisions(self):                
        self.division.tournament.single_division = True                
        simple_dict = self.division.to_dict_simple()
        self.assertEquals(simple_dict['tournament_name'],'test_tournament')
        self.assertEquals(simple_dict['single_division'], True)

    def test_to_dict_tournament_with_multiple_divisions(self):                
        self.division.tournament.single_division = False
        simple_dict = self.division.to_dict_simple()
        self.assertEquals(simple_dict['tournament_name'],'test_tournament, a')
        self.assertEquals(simple_dict['single_division'], False)
        
        

        
