import unittest
from td_types import ImportedTables
from util import db_util

class ModelTournamentTD(unittest.TestCase):
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
        simple_dict = self.tournament.to_dict_simple()
        for value in self.tournament.__table__.columns:
            key =  str(value)[str(value).index('.')+1:]            
            self.assertTrue(key in simple_dict,"oops - did not find %s" % key)        

        
