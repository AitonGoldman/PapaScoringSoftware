import unittest
from td_types import ImportedTables
from util import db_util

class ModelUserTD(unittest.TestCase):
    def setUp(self):        
        self.db_handle = db_util.create_db_handle_no_app()        
        self.tables = ImportedTables(self.db_handle)
        self.tournament = self.tables.Tournament(
            tournament_name='test_tournament',
            team_tournament=False,
            active=False,
            single_division=False,
            scoring_type="HERB"
        )        
    def test_to_dict_simple(self):         
        tournament_dict = {'tournament_name':'test_tournament','team_tournament':False, 'active':False, 'single_division':False, 'scoring_type':'HERB', 'start_date':None,'end_date':None,'tournament_id':None}
        
        simple_dict = self.tournament.to_dict_simple()
        self.assertDictEqual(tournament_dict,simple_dict)

        
