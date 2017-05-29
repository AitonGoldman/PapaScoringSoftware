import unittest
from routes.utils import fetch_entity
from mock import MagicMock
from util import db_util
from td_types import ImportedTables
from routes.token import get_total_tokens_for_player


class RouteTokenTD(unittest.TestCase):    
    def setUp(self):
        self.mock_app = MagicMock()
        self.db_handle = db_util.create_db_handle_no_app()        
        self.tables = ImportedTables(self.db_handle)        
        self.tables.Token.query = MagicMock()        
        self.tables.Team.query = MagicMock()        
        self.tables.Division.query = MagicMock()        
        self.mock_app.tables = self.tables
        self.mock_app.tables.db_handle = MagicMock()

    def generate_tokens(self,number_of_tokens,
                        player_id=None, division_id=None,
                        meta_division_id=None,team_id=None,
                        voided=False,used=False):
        results = []
        for token_index in range(number_of_tokens):            
            results.append(self.mock_app.tables.Token())
            results[token_index].division_id=division_id
            results[token_index].team_id=team_id
            results[token_index].metadivision_id=meta_division_id
            results[token_index].player_id=player_id
            if voided:
                results[token_index].voided=True
            if used:
                results[token_index].used=True
                
        return results
    
    def check_total_tokens_count(self, totals):
        self.assertEquals(totals['divisions'][0],0)
        self.assertEquals(totals['divisions'][1],5)        
        self.assertEquals(totals['divisions'][3],0)
        self.assertEquals(totals['divisions'][4],5)
        self.assertEquals(totals['metadivisions'][1],5)        
        
    def test_get_total_tokens_for_player(self):
        player_tokens=self.generate_tokens(5,division_id=1,player_id=1)
        meta_division_tokens = self.generate_tokens(5,meta_division_id=1,player_id=1)
        player_tokens=player_tokens+meta_division_tokens
        team_tokens=self.generate_tokens(5,division_id=4,team_id=1)
        
        self.mock_app.tables.Team.players = MagicMock()
        team = self.mock_app.tables.Team(team_id=1)
        divisions = [self.mock_app.tables.Division(division_id=division_index) for division_index in range(5)]

        divisions[2].meta_division_id=1
        
        totals =  get_total_tokens_for_player(self.mock_app,player_tokens,divisions,team_tokens)        
        self.check_total_tokens_count(totals)
        
        player_tokens=self.generate_tokens(5,division_id=1,
                                           player_id=1,voided=True)
        meta_division_tokens = self.generate_tokens(5,meta_division_id=1,
                                                    player_id=1,voided=True)
        player_tokens=player_tokens+meta_division_tokens        
        team_tokens=self.generate_tokens(5,division_id=4,
                                         team_id=1,voided=True)
        totals =  get_total_tokens_for_player(self.mock_app,player_tokens,divisions,team_tokens)        
        self.check_total_tokens_count(totals)

        player_tokens=self.generate_tokens(5,division_id=1,
                                           player_id=1,used=True)
        meta_division_tokens = self.generate_tokens(5,meta_division_id=1,
                                                    player_id=1,used=True)
        player_tokens=player_tokens+meta_division_tokens
        team_tokens=self.generate_tokens(5,division_id=4,team_id=1,used=True)
        totals =  get_total_tokens_for_player(self.mock_app,player_tokens,divisions,team_tokens)        
        self.check_total_tokens_count(totals)                                 
        
        
