import unittest
from routes.utils import fetch_entity
from mock import MagicMock
from routes.finals import initialize_division_final,create_simplified_division_results,remove_missing_final_player,create_division_final_players,get_tiebreakers_for_division,record_tiebreaker_results
from util import db_util
from td_types import ImportedTables

class RouteFinalsTD(unittest.TestCase):    
    def setUp(self):
        self.mock_app = MagicMock()
        self.db_handle = db_util.create_db_handle_no_app()        
        self.tables = ImportedTables(self.db_handle)        
        self.tables.DivisionFinal.query = MagicMock()
        #self.tables.DivisionFinal.query.filter_by.return_value.all.return_value.qualifiers.__getitem__.return_value=99
        
        
        self.mock_app.tables = self.tables
        self.mock_app.tables.db_handle = MagicMock()
        self.division_results = [
            [
                0, 
                {
                    "ifpa_ranking": 10, 
                    "player_id": 1, 
                    "player_name": "Bowen Kerins", 
                    "sum": 512
                }
            ], 
            [
                1, 
                {
                    "ifpa_ranking": 7, 
                    "player_id": 223, 
                    "player_name": "Cayle George", 
                    "sum": 503
                }
            ], 
            [
                2, 
                {
                    "ifpa_ranking": 1, 
                    "player_id": 517, 
                    "player_name": "Keith Elwin", 
                    "sum": 497
                }
            ], 
            [
                3, 
                {
                    "ifpa_ranking": 6, 
                    "player_id": 121, 
                    "player_name": "Robert Gagno", 
                    "sum": 493
                }
            ], 
            [
                3, 
                {
                    "ifpa_ranking": 3, 
                    "player_id": 298, 
                    "player_name": "Jorian Engelbrektsson", 
                    "sum": 493
                }
            ], 
            [
                5, 
                {
                    "ifpa_ranking": 12, 
                    "player_id": 300, 
                    "player_name": "Kevin Birrell", 
                    "sum": 491
                }
            ], 
            [
                6, 
                {
                    "ifpa_ranking": 30, 
                    "player_id": 178, 
                    "player_name": "Joshua Henderson", 
                    "sum": 490
                }
            ]
        ]

        self.final_players = [
            {'adjusted_seed': None, 'overall_rank': None, 'final_player_id': None, 'initial_seed': 0, 'team_id': None, 'player_id': 1, 'removed': None, 'division_final_id': None, 'type':'result'},
            {'adjusted_seed': None, 'overall_rank': None, 'final_player_id': None, 'initial_seed': 1, 'team_id': None, 'player_id': 223, 'removed': None, 'division_final_id': None, 'type':'result'},
            {'adjusted_seed': None, 'overall_rank': None, 'final_player_id': None, 'initial_seed': 2, 'team_id': None, 'player_id': 517, 'removed': None, 'division_final_id': None, 'type':'result'},
            {'adjusted_seed': None, 'overall_rank': None, 'final_player_id': None, 'initial_seed': 3, 'team_id': None, 'player_id': 121, 'removed': None, 'division_final_id': None, 'type':'result'},
            {'adjusted_seed': None, 'overall_rank': None, 'final_player_id': None, 'initial_seed': 3, 'team_id': None, 'player_id': 298, 'removed': None, 'division_final_id': None, 'type':'result'},
            {'adjusted_seed': None, 'overall_rank': None, 'final_player_id': None, 'initial_seed': 5, 'team_id': None, 'player_id': 300, 'removed': None, 'division_final_id': None, 'type':'result'},
            {'adjusted_seed': None, 'overall_rank': None, 'final_player_id': None, 'initial_seed': 6, 'team_id': None, 'player_id': 178, 'removed': None, 'division_final_id': None, 'type':'result'}
        ]
        self.tiebreaker_results = [
            {
                'final_player_id':4,
                'initial_seed':3,
                'player_name':'player_test4',
                'player_score':1
            },
            {
                'final_player_id':5,
                'initial_seed':3,
                'player_name':'player_test5',
                'player_score':2
            }                
        ]

    def test_remove_missing_final_player(self):        
        pruned_final_player_list = remove_missing_final_player(self.final_players,self.mock_app)
        self.assertEquals(len(pruned_final_player_list),7)
        self.final_players[0]['removed']=True
        pruned_final_player_list = remove_missing_final_player(self.final_players,self.mock_app)
        self.assertEquals(len(pruned_final_player_list),7)        
        self.assertEquals(pruned_final_player_list[0]['player_id'],1)
        self.assertEquals(pruned_final_player_list[0]['removed'],True)
        self.assertEquals(pruned_final_player_list[1]['removed'],None)

    def test_remove_missing_final_player_with_simplified_list(self):                        
        self.final_players[0]['removed']=True
        simplified_results = create_simplified_division_results(self.final_players,3,self.mock_app)
        pruned_final_player_list = remove_missing_final_player(simplified_results,self.mock_app)
        self.assertEquals(len(pruned_final_player_list),7)        
        self.assertEquals(pruned_final_player_list[3]['type'],'result')
        self.assertEquals(pruned_final_player_list[0]['player_id'],1)
        self.assertEquals(pruned_final_player_list[0]['removed'],True)
        self.assertEquals(pruned_final_player_list[1]['removed'],None)
        
    def test_initialize_division_final(self):                
        self.tables.DivisionFinal.query.filter_by.return_value.all.return_value=None
        division_final = initialize_division_final(1,"test_division",self.division_results,self.mock_app)
        self.assertEquals(division_final.division_id,1)
        self.assertEquals(len(division_final.qualifiers),7)
        self.assertEquals(division_final.qualifiers[0].initial_seed,0)

    def test_initialize_division_final_with_existing_division_final(self):                
        existing_division_final = self.tables.DivisionFinal()
        self.tables.DivisionFinal.query.filter_by.return_value.all.return_value=existing_division_final
        division_final = initialize_division_final(1,"test_division",self.division_results,self.mock_app)
        self.assertEquals(division_final,existing_division_final)

    def test_create_division_final_players(self):
        division_final = self.tables.DivisionFinal()
        division_final.qualifiers=[]
        
        create_division_final_players(division_final,self.division_results,self.mock_app)
        self.assertEquals(len(division_final.qualifiers),7)

    def test_create_simplified_division_results(self):                    
        simplified_division_results = create_simplified_division_results(self.final_players, 4, self.mock_app)
        self.assertEquals(len(simplified_division_results),8)        
        self.assertEquals(simplified_division_results[5]['type'],"divider")
        self.final_players[5]['removed']=True
        self.final_players[6]['initial_seed']=self.final_players[6]['initial_seed']-1        
        simplified_division_results = create_simplified_division_results(self.final_players, 6, self.mock_app)          
        self.assertEquals(len(simplified_division_results),8)        
        self.assertEquals(simplified_division_results[7]['type'],"divider")
        
    def test_create_division_final_players(self):
        division_final = self.tables.DivisionFinal()
        division_final.qualifiers=[]
        create_division_final_players(division_final,self.division_results,self.mock_app)
        self.assertEquals(len(division_final.qualifiers),7)        
        self.assertEquals(division_final.qualifiers[0].initial_seed,0)
        
    def test_get_tiebreakers_for_division(self):
        division_final = self.tables.DivisionFinal()
        division_final.division_final_id=1
        division_final_players = create_division_final_players(division_final,self.division_results,self.mock_app)        
        for index,final_player in enumerate(division_final_players):
            division_final_players[index].final_player_id=index+1
            division_final_players[index].player_name="test player"+str(index+1)
            
        tiebreakers = get_tiebreakers_for_division(division_final_players,6)        
        self.assertEquals(len(tiebreakers[0]),2)
        self.assertEquals(tiebreakers[0][0]['final_player_id'],4)    
        self.assertEquals(tiebreakers[0][1]['final_player_id'],5)    

    def test_set_tiebreaker_results_for_division(self):
        division_final = self.tables.DivisionFinal()
        division_final.division_final_id=1
        division_final_players = create_division_final_players(division_final,self.division_results,self.mock_app)        
 
        for index,final_player in enumerate(division_final_players):
            division_final_players[index].final_player_id=index+1
            division_final_players[index].player_name="test player"+str(index+1)                            
        
        record_tiebreaker_results(division_final_players,self.tiebreaker_results,self.mock_app)        
        self.assertEquals(division_final.qualifiers[4].initial_seed,3)        
        self.assertEquals(division_final.qualifiers[3].initial_seed,4)        
        
