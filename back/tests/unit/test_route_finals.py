import unittest
from routes.utils import fetch_entity
from mock import MagicMock
from routes.finals import initialize_division_final,create_simplified_division_results,remove_missing_final_player,create_division_final_players,get_tiebreakers_for_division,get_important_tiebreakers_for_division,record_tiebreaker_results,generate_brackets,resolve_unimportant_ties,calculate_points_for_game,calculate_points_for_match,calculate_tiebreakers,resolve_tiebreakers,record_scores
from util import db_util
from td_types import ImportedTables
import json

def generate_test_match(with_ties=False,with_scores=True,without_players=False,half_completed=False):
    final_player_ids=[None,None,None,None]
    if without_players:
        final_player_ids[0]=None        
        final_player_ids[1]=None        
        final_player_ids[2]=None        
        final_player_ids[3]=None        
    else:
        final_player_ids[0]=9        
        final_player_ids[1]=17
        final_player_ids[2]=18
        final_player_ids[3]=24

    test_match_dict = {
        "completed":False,
        "expected_num_tiebreaker_winners": None,
        "final_match_game_results":[],
        "final_match_player_results": [
            {
                'final_player_id':final_player_ids[0],
                'needs_tiebreaker':False,
                'papa_points_sum':None,
                'winner':None,
                'won_tiebreaker':None
            },
            {
                'final_player_id': final_player_ids[1],
                'needs_tiebreaker':False,
                'papa_points_sum':None,
                'winner':None,
                'won_tiebreaker':None
            },
            {
                'final_player_id':final_player_ids[2],
                'needs_tiebreaker':False,
                'papa_points_sum':None,
                'winner':None,
                'won_tiebreaker':None
            },
            {
                'final_player_id':final_player_ids[3],
                'needs_tiebreaker':False,
                'papa_points_sum':None,
                'winner':None,
                'won_tiebreaker':None
            }


                
            ]
    }
    if with_ties:
        test_match_dict['final_match_game_results']=[
            generate_test_game_result(fill_in_scores_and_points=True,scores=[4,1,2,0]),                
            generate_test_game_result(fill_in_scores_and_points=True,scores=[4,0,1,2]),
            generate_test_game_result(fill_in_scores_and_points=True,scores=[0,4,2,1])
    ]
    else:        
        test_match_dict['final_match_game_results']=[
            generate_test_game_result(fill_in_scores_and_points=with_scores),                
            generate_test_game_result(fill_in_scores_and_points=with_scores)
        ]
        if half_completed is False:
            test_match_dict['final_match_game_results'].append(generate_test_game_result(fill_in_scores_and_points=with_scores))

    return test_match_dict

def generate_test_game_result(fill_in_scores_and_points=False,scores=None,without_players=False):
    final_player_ids=[None,None,None,None]    
    if without_players:
        final_player_ids[0]=None        
        final_player_ids[1]=None        
        final_player_ids[2]=None        
        final_player_ids[3]=None        
    else:
        final_player_ids[0]=9        
        final_player_ids[1]=17
        final_player_ids[2]=18
        final_player_ids[3]=24
        
    game_result = {
        "completed": False, 
        "division_final_match_game_player_results": [
            {
                "division_final_match_game_player_result_id": 1, 
                "division_final_match_game_result_id": 1, 
                "final_player": {
                    "adjusted_seed": 9, 
                    "division_final_id": 1, 
                    "final_player_id": 9, 
                    "initial_seed": 8, 
                    "overall_rank": None, 
                    "player_id": 108, 
                    "player_name": "Una Beddard9", 
                    "removed": None, 
                    "team_id": None
                }, 
                "final_player_id": final_player_ids[0],
                "papa_points": None, 
                "play_order": None, 
                "score": None
            }, 
            {
                "division_final_match_game_player_result_id": 2, 
                "division_final_match_game_result_id": 1, 
                "final_player": {
                    "adjusted_seed": 16, 
                    "division_final_id": 1, 
                    "final_player_id": 17, 
                    "initial_seed": 16, 
                    "overall_rank": None, 
                    "player_id": 116, 
                    "player_name": "Brad Agtarap17", 
                    "removed": None, 
                    "team_id": None
                }, 
                "final_player_id":final_player_ids[1], 
                "papa_points": None, 
                "play_order": None, 
                "score": None
            }, 
            {
                "division_final_match_game_player_result_id": 3, 
                "division_final_match_game_result_id": 1, 
                "final_player": {
                    "adjusted_seed": 17, 
                    "division_final_id": 1, 
                    "final_player_id": 18, 
                    "initial_seed": 16, 
                    "overall_rank": None, 
                    "player_id": 117, 
                    "player_name": "Dorothea Alvidrez18", 
                    "removed": None, 
                    "team_id": None
                }, 
                "final_player_id":final_player_ids[2],
                "papa_points": None, 
                "play_order": None, 
                "score": None
            }, 
            {
                "division_final_match_game_player_result_id": 4, 
                "division_final_match_game_result_id": 1, 
                "final_player": {
                    "adjusted_seed": 24, 
                    "division_final_id": 1, 
                    "final_player_id": 24, 
                    "initial_seed": 24, 
                    "overall_rank": None, 
                    "player_id": 123, 
                    "player_name": "Nathanael Balsiger24", 
                    "removed": None, 
                    "team_id": None
                }, 
                "final_player_id":final_player_ids[3],
                "papa_points": None, 
                "play_order": None, 
                "score": None
            }
        ], 
        "division_final_match_game_result_id": 1, 
        "division_final_match_id": 1, 
        "division_machine_id": None, 
        "division_machine_string": None, 
        "ready_to_be_completed": False
    }
    if without_players:
        return game_result        
    if fill_in_scores_and_points and scores is None:
        game_result['division_final_match_game_player_results'][0]['score']=0
        game_result['division_final_match_game_player_results'][0]['papa_points']=0
        game_result['division_final_match_game_player_results'][1]['score']=1
        game_result['division_final_match_game_player_results'][1]['papa_points']=1
        game_result['division_final_match_game_player_results'][2]['score']=2
        game_result['division_final_match_game_player_results'][2]['papa_points']=2
        game_result['division_final_match_game_player_results'][3]['score']=4
        game_result['division_final_match_game_player_results'][3]['papa_points']=4
    if fill_in_scores_and_points and scores:
        game_result['division_final_match_game_player_results'][0]['score']=scores[0]        
        game_result['division_final_match_game_player_results'][1]['score']=scores[1]        
        game_result['division_final_match_game_player_results'][2]['score']=scores[2]        
        game_result['division_final_match_game_player_results'][3]['score']=scores[3]
        sorted_game_results = sorted(game_result['division_final_match_game_player_results'], key= lambda e: e['score'])    
        sorted_game_results[0]['papa_points']=0
        sorted_game_results[1]['papa_points']=1
        sorted_game_results[2]['papa_points']=2
        sorted_game_results[3]['papa_points']=4
        game_result['division_final_match_game_player_results']=sorted_game_results
    return game_result

class RouteFinalsTD(unittest.TestCase):    
    def setUp(self):
        self.mock_app = MagicMock()
        self.db_handle = db_util.create_db_handle_no_app()        
        self.tables = ImportedTables(self.db_handle)        
        self.tables.DivisionFinal.query = MagicMock()
        self.tables.DivisionFinalPlayer.query = MagicMock()
        self.tables.DivisionFinalMatchPlayerResult.query = MagicMock()
        self.tables.DivisionFinalMatch.query = MagicMock()
        
                
        #self.tables.DivisionFinal.query.filter_by.return_value.all.return_value.qualifiers.__getitem__.return_value=99
        
        
        self.mock_app.tables = self.tables
        self.mock_app.tables.db_handle = MagicMock()
        self.generated_brackets_match_game_dict = generate_test_game_result()                           
        
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
            {'adjusted_seed': None, 'overall_rank': None, 'final_player_id': 1, 'initial_seed': 0, 'team_id': None, 'player_name': 'player 1', 'player_id': 1, 'removed': None, 'division_final_id': None, 'type':'result'},
            {'adjusted_seed': None, 'overall_rank': None, 'final_player_id': 2, 'initial_seed': 1, 'team_id': None, 'player_id': 223, 'player_name': 'player 223', 'removed': None, 'division_final_id': None, 'type':'result'},
            {'adjusted_seed': None, 'overall_rank': None, 'final_player_id': 3, 'initial_seed': 2, 'team_id': None, 'player_id': 517, 'player_name': 'player 517', 'removed': None, 'division_final_id': None, 'type':'result'},
            {'adjusted_seed': None, 'overall_rank': None, 'final_player_id': 4, 'initial_seed': 3, 'team_id': None, 'player_id': 121, 'player_name': 'player 121', 'removed': None, 'division_final_id': None, 'type':'result'},
            {'adjusted_seed': None, 'overall_rank': None, 'final_player_id': 5, 'initial_seed': 3, 'team_id': None, 'player_id': 298, 'player_name': 'player 298', 'removed': None, 'division_final_id': None, 'type':'result'},
            {'adjusted_seed': None, 'overall_rank': None, 'final_player_id': 6, 'initial_seed': 5, 'team_id': None, 'player_id': 300, 'player_name': 'player 300', 'removed': None, 'division_final_id': None, 'type':'result'},
            {'adjusted_seed': None, 'overall_rank': None, 'final_player_id': 7, 'initial_seed': 6, 'team_id': None, 'player_id': 178, 'player_name': 'player 178', 'removed': None, 'division_final_id': None, 'type':'result'}
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

    def generate_results(self,number_of_players):
        results = []
        for index in range(number_of_players):
            result = []            
            result.append(index)
            result.append({
                'ifpa_ranking':index,
                'player_id':index+1,
                'player_name':'player %s'%(index+1),
                'sum':100-index
            })
            results.append(result)            
        return results
    
    def generate_final_players(self,number_of_players):
        final_players = []        
        for index in range(number_of_players):
            final_player = {}
            final_player['adjusted_seed']=None
            final_player['overall_rank']=None
            final_player['final_player_id']=index+1
            final_player['initial_seed']=index
            final_player['team_id']=None
            final_player['player_name']="player %s"%(index+1)
            final_player['player_id']=index+1
            final_player['removed']=None
            final_player['division_final_id']=None
            final_player['type']='result'
            final_players.append(final_player)
        return final_players
    
    def test_remove_missing_final_player(self):        
        pruned_final_player_list = remove_missing_final_player(self.final_players,self.mock_app)
        self.assertEquals(len(pruned_final_player_list),7)
        self.final_players[0]['removed']=True
        pruned_final_player_list = remove_missing_final_player(self.final_players,self.mock_app)
        self.assertEquals(len(pruned_final_player_list),7)        
        self.assertEquals(pruned_final_player_list[0]['player_id'],1)
        self.assertEquals(pruned_final_player_list[0]['removed'],True)
        self.assertEquals(pruned_final_player_list[1]['removed'],None)

    def test_generate_brackets(self):                                
        division_final = self.tables.DivisionFinal()
        final_results = self.generate_results(30)
        final_players = self.generate_final_players(30)
        
        create_division_final_players(division_final,final_results,self.mock_app)
        for index,final_player in enumerate(division_final.qualifiers):
            division_final.qualifiers[index].final_player_id=index+1
            division_final.qualifiers[index].player_name="test player"+str(index+1)
        
        self.mock_app.tables.DivisionFinalPlayer.query.filter_by.return_value.all.return_value=division_final.qualifiers
        #final_players_from_db = self.generate_final_players(30)

        for player in final_players:
            player['reranked_seed']=player['initial_seed']            
        final_players[0]['reranked_seed']=4
        simplified_results = create_simplified_division_results(final_players,7,self.mock_app)        
        results = generate_brackets(self.mock_app,1,simplified_results,7)        
        #self.assertTrue(results[3]['reranked_seed']!=results[4]['reranked_seed'])                
        #self.assertTrue(results[3]['reranked_seed']==3 or results[3]['reranked_seed']==4)        
        
    def test_resolve_unimportant_ties(self):                        
        for player in self.final_players:
            player['reranked_seed']=player['initial_seed']            
        #self.final_players[0]['removed']=True
        simplified_results = create_simplified_division_results(self.final_players,7,self.mock_app)
        results = resolve_unimportant_ties(simplified_results,7)        
        self.assertTrue(results[3]['reranked_seed']!=results[4]['reranked_seed'])                
        self.assertTrue(results[3]['reranked_seed']==3 or results[3]['reranked_seed']==4)        
        
    def test_remove_missing_final_player_with_simplified_list(self):                        
        for player in self.final_players:
            player['reranked_seed']=player['initial_seed']            
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
        for player in self.final_players:
            player['reranked_seed']=player['initial_seed']            
        simplified_division_results = create_simplified_division_results(self.final_players, 4, self.mock_app)
        self.assertEquals(len(simplified_division_results),8)        
        self.assertEquals(simplified_division_results[5]['type'],"divider")
        self.final_players[5]['removed']=True
        self.final_players[6]['initial_seed']=self.final_players[6]['initial_seed']-1        
        self.final_players[6]['reranked_seed']=self.final_players[6]['initial_seed']-1         
        simplified_division_results = create_simplified_division_results(self.final_players, 6, self.mock_app)          
        self.assertEquals(len(simplified_division_results),8)        
        self.assertEquals(simplified_division_results[7]['type'],"divider")
        
    def test_create_division_final_players(self):
        division_final = self.tables.DivisionFinal()
        division_final.qualifiers=[]
        create_division_final_players(division_final,self.division_results,self.mock_app)
        self.assertEquals(len(division_final.qualifiers),7)        
        self.assertEquals(division_final.qualifiers[0].initial_seed,0)

    def test_get_important_tiebreakers_for_division(self):
        division_final = self.tables.DivisionFinal()
        division_final.division_final_id=1
        division_final_players = create_division_final_players(division_final,self.division_results,self.mock_app)        
        for index,final_player in enumerate(division_final_players):
            division_final_players[index].final_player_id=index+1
            division_final_players[index].player_name="test player"+str(index+1)
        division_final_players[6].initial_seed=5
        important_tiebreaker_ranks = get_important_tiebreakers_for_division(division_final_players,6,{'qualifying':3})
        self.assertEquals(important_tiebreaker_ranks['qualifying'],3)                
        important_tiebreaker_ranks = get_important_tiebreakers_for_division(division_final_players,6,{'qualifying':4})        
        self.assertTrue('qualifying' not in important_tiebreaker_ranks)                
        important_tiebreaker_ranks = get_important_tiebreakers_for_division(division_final_players,6,{'bye':3})
        self.assertEquals(important_tiebreaker_ranks['bye'],3)                
        important_tiebreaker_ranks = get_important_tiebreakers_for_division(division_final_players,6,{'bye':4})
        self.assertTrue('bye' not in important_tiebreaker_ranks)                
        
        important_tiebreaker_ranks = get_important_tiebreakers_for_division(division_final_players,7,{'qualifying':5,'bye':3})
        self.assertEquals(important_tiebreaker_ranks['bye'],3)
        self.assertEquals(important_tiebreaker_ranks['qualifying'],5)                        
        important_tiebreaker_ranks = get_important_tiebreakers_for_division(division_final_players,7,{'qualifying':6,'bye':4})

        self.assertTrue('bye' not in important_tiebreaker_ranks)                        
        self.assertEquals(important_tiebreaker_ranks['qualifying'],5)                        
        
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
        
        results = record_tiebreaker_results(division_final_players,self.tiebreaker_results,self.mock_app)        
        self.assertEquals(division_final.qualifiers[4].initial_seed,3)        
        self.assertEquals(division_final.qualifiers[3].initial_seed,4)        
        self.assertEquals(results[0]['initial_seed'],4)        
        
    def test_calculate_points_for_game_without_enough_scores(self):        
        calculate_points_for_game(self.generated_brackets_match_game_dict)
        self.assertEquals(self.generated_brackets_match_game_dict['division_final_match_game_player_results'][0]['papa_points'],None)
        self.assertEquals(self.generated_brackets_match_game_dict['division_final_match_game_player_results'][1]['papa_points'],None)
        self.assertEquals(self.generated_brackets_match_game_dict['division_final_match_game_player_results'][2]['papa_points'],None)
        self.assertEquals(self.generated_brackets_match_game_dict['division_final_match_game_player_results'][3]['papa_points'],None)
        self.assertEquals(self.generated_brackets_match_game_dict['completed'],False)                        

        self.generated_brackets_match_game_dict['division_final_match_game_player_results'][0]['score']=126
        self.generated_brackets_match_game_dict['division_final_match_game_player_results'][1]['score']=125
        self.generated_brackets_match_game_dict['division_final_match_game_player_results'][2]['score']=124        
        calculate_points_for_game(self.generated_brackets_match_game_dict)        
        self.assertEquals(self.generated_brackets_match_game_dict['division_final_match_game_player_results'][0]['papa_points'],None)
        self.assertEquals(self.generated_brackets_match_game_dict['division_final_match_game_player_results'][1]['papa_points'],None)
        self.assertEquals(self.generated_brackets_match_game_dict['division_final_match_game_player_results'][2]['papa_points'],None)
        self.assertEquals(self.generated_brackets_match_game_dict['division_final_match_game_player_results'][3]['papa_points'],None)
        self.assertEquals(self.generated_brackets_match_game_dict['completed'],False)                        

    def test_calculate_points_for_game_with_enough_scores(self):                
        self.generated_brackets_match_game_dict['division_final_match_game_player_results'][0]['score']=126
        self.generated_brackets_match_game_dict['division_final_match_game_player_results'][1]['score']=125
        self.generated_brackets_match_game_dict['division_final_match_game_player_results'][2]['score']=124        
        self.generated_brackets_match_game_dict['division_final_match_game_player_results'][3]['score']=123        
        calculate_points_for_game(self.generated_brackets_match_game_dict)        
        self.assertEquals(self.generated_brackets_match_game_dict['division_final_match_game_player_results'][0]['final_player_id'],24)
        self.assertEquals(self.generated_brackets_match_game_dict['division_final_match_game_player_results'][0]['papa_points'],0)
        self.assertEquals(self.generated_brackets_match_game_dict['division_final_match_game_player_results'][1]['final_player_id'],18)
        self.assertEquals(self.generated_brackets_match_game_dict['division_final_match_game_player_results'][1]['papa_points'],1)
        self.assertEquals(self.generated_brackets_match_game_dict['division_final_match_game_player_results'][2]['final_player_id'],17)
        self.assertEquals(self.generated_brackets_match_game_dict['division_final_match_game_player_results'][2]['papa_points'],2)
        self.assertEquals(self.generated_brackets_match_game_dict['division_final_match_game_player_results'][3]['final_player_id'],9)
        self.assertEquals(self.generated_brackets_match_game_dict['division_final_match_game_player_results'][3]['papa_points'],4)

        self.assertEquals(self.generated_brackets_match_game_dict['completed'],True)                        
        
    def test_calculate_points_for_match_uncompleted(self):                
        test_match_dict = generate_test_match(half_completed=True)        
        calculate_points_for_match(test_match_dict)                        
        self.assertEquals(test_match_dict['completed'],False)
        self.assertEquals(test_match_dict['final_match_player_results'][0]['papa_points_sum'],0)
        self.assertEquals(test_match_dict['final_match_player_results'][1]['papa_points_sum'],2)
        self.assertEquals(test_match_dict['final_match_player_results'][2]['papa_points_sum'],4)
        self.assertEquals(test_match_dict['final_match_player_results'][3]['papa_points_sum'],8)

    def test_calculate_points_for_match_with_enough_scores(self):                
        test_match_dict = generate_test_match()        
        calculate_points_for_match(test_match_dict)                        
        self.assertEquals(test_match_dict['completed'],True)
        self.assertEquals(test_match_dict['final_match_player_results'][0]['papa_points_sum'],0)
        self.assertEquals(test_match_dict['final_match_player_results'][1]['papa_points_sum'],3)
        self.assertEquals(test_match_dict['final_match_player_results'][2]['papa_points_sum'],6)
        self.assertEquals(test_match_dict['final_match_player_results'][3]['papa_points_sum'],12)
        self.assertEquals(test_match_dict['final_match_player_results'][0]['winner'],False)
        self.assertEquals(test_match_dict['final_match_player_results'][1]['winner'],False)
        self.assertEquals(test_match_dict['final_match_player_results'][2]['winner'],True)
        self.assertEquals(test_match_dict['final_match_player_results'][3]['winner'],True)
        
    def test_calculate_tiebreakers(self):                
        test_match_dict = generate_test_match(with_ties=True)        
        calculate_points_for_match(test_match_dict)
        tiebreaker_final_player_ids=calculate_tiebreakers(test_match_dict)
        #print tiebreaker_final_player_ids
        self.assertEquals(test_match_dict['completed'],False)
        self.assertEquals(test_match_dict['expected_num_tiebreaker_winners'],1)
        self.assertEquals(test_match_dict['final_match_player_results'][0]['needs_tiebreaker'],False)
        self.assertEquals(test_match_dict['final_match_player_results'][1]['needs_tiebreaker'],True)
        self.assertEquals(test_match_dict['final_match_player_results'][2]['needs_tiebreaker'],True)
        self.assertEquals(test_match_dict['final_match_player_results'][3]['needs_tiebreaker'],False)

    def test_calculate_tiebreakers_report_only(self):                
        test_match_dict = generate_test_match(with_ties=True)                
        test_match_dict['final_match_player_results'][0]['papa_points_sum']=8
        test_match_dict['final_match_player_results'][1]['papa_points_sum']=5
        test_match_dict['final_match_player_results'][2]['papa_points_sum']=5
        test_match_dict['final_match_player_results'][3]['papa_points_sum']=4
        tiebreaker_final_player_ids=calculate_tiebreakers(test_match_dict,report_only=True)        
        self.assertEquals(len(tiebreaker_final_player_ids),2)
        self.assertEquals(tiebreaker_final_player_ids[0],17)
        self.assertEquals(tiebreaker_final_player_ids[1],18)
        self.assertEquals(test_match_dict['completed'],False)
        self.assertEquals(test_match_dict['expected_num_tiebreaker_winners'],None)
        self.assertEquals(test_match_dict['final_match_player_results'][0]['needs_tiebreaker'],False)
        self.assertEquals(test_match_dict['final_match_player_results'][1]['needs_tiebreaker'],False)
        self.assertEquals(test_match_dict['final_match_player_results'][2]['needs_tiebreaker'],False)
        self.assertEquals(test_match_dict['final_match_player_results'][3]['needs_tiebreaker'],False)
        
    def test_calculate_points_for_match_with_ties(self):                
        test_match_dict = generate_test_match(with_ties=True)        
        calculate_points_for_match(test_match_dict)                        
        self.assertEquals(test_match_dict['completed'],False)
        self.assertEquals(test_match_dict['final_match_player_results'][0]['papa_points_sum'],8)
        self.assertEquals(test_match_dict['final_match_player_results'][1]['papa_points_sum'],5)
        self.assertEquals(test_match_dict['final_match_player_results'][2]['papa_points_sum'],5)
        self.assertEquals(test_match_dict['final_match_player_results'][3]['papa_points_sum'],3)
        self.assertEquals(test_match_dict['final_match_player_results'][0]['winner'],None)
        self.assertEquals(test_match_dict['final_match_player_results'][1]['winner'],None)
        self.assertEquals(test_match_dict['final_match_player_results'][2]['winner'],None)
        self.assertEquals(test_match_dict['final_match_player_results'][3]['winner'],None)
 
    def test_calculate_points_for_match_without_players(self):                
        test_match_dict = generate_test_match(without_players=True)        
        calculate_points_for_match(test_match_dict)                        
        self.assertEquals(test_match_dict['completed'],False)
        self.assertEquals(test_match_dict['final_match_player_results'][0]['papa_points_sum'],None)
        self.assertEquals(test_match_dict['final_match_player_results'][1]['papa_points_sum'],None)
        self.assertEquals(test_match_dict['final_match_player_results'][2]['papa_points_sum'],None)
        self.assertEquals(test_match_dict['final_match_player_results'][3]['papa_points_sum'],None)
 

    def test_resolve_tiebreakers(self):
        tiebreaker_scores_dict={
            "expected_num_tiebreaker_winners":2,
            "division_final_match_id":1,
            "scores":[
                {
                    "final_player_id":9,
                    "score":1
                },
                {
                    "final_player_id":24,
                    "score":2                    
                }
            ]
        }
        self.tables.DivisionFinalMatchPlayerResult.query.filter_by.return_value = MagicMock()
        division_final_match_player_results = [
            self.tables.DivisionFinalMatchPlayerResult(
                final_player_id=9
            ),
            self.tables.DivisionFinalMatchPlayerResult(
                final_player_id=24
            )            
        ]
        self.tables.DivisionFinalMatchPlayerResult.query.filter_by.return_value.all.return_value = division_final_match_player_results
        division_final_match = self.tables.DivisionFinalMatch()
        self.tables.DivisionFinalMatch.query.filter_by.return_value.first.return_value = division_final_match
        
        resolve_tiebreakers(tiebreaker_scores_dict,self.mock_app)
        
        self.assertEquals(division_final_match_player_results[1].won_tiebreaker,True)
        self.assertEquals(division_final_match_player_results[0].won_tiebreaker,False)
        self.assertEquals(division_final_match.completed,True)

    def test_resolve_tiebreakers_with_3_ties(self):
        tiebreaker_scores_dict={
            "expected_num_tiebreaker_winners":2,
            "division_final_match_id":1,
            "scores":[
                {
                    "final_player_id":9,
                    "score":1
                },
                {
                    "final_player_id":24,
                    "score":2                    
                },
                {
                    "final_player_id":17,
                    "score":3                    
                }                
            ]
        }
        self.tables.DivisionFinalMatchPlayerResult.query.filter_by.return_value = MagicMock()
        division_final_match_player_results = [
            self.tables.DivisionFinalMatchPlayerResult(
                final_player_id=9
            ),
            self.tables.DivisionFinalMatchPlayerResult(
                final_player_id=24
            ),
            self.tables.DivisionFinalMatchPlayerResult(
                final_player_id=17
            )            
        ]
        self.tables.DivisionFinalMatchPlayerResult.query.filter_by.return_value.all.return_value = division_final_match_player_results

        division_final_match = self.tables.DivisionFinalMatch()
        self.tables.DivisionFinalMatch.query.filter_by.return_value.first.return_value = division_final_match        
        resolve_tiebreakers(tiebreaker_scores_dict,self.mock_app)
        
        self.assertEquals(division_final_match_player_results[0].won_tiebreaker,False)
        self.assertEquals(division_final_match_player_results[1].won_tiebreaker,True)
        self.assertEquals(division_final_match_player_results[2].won_tiebreaker,True)
        self.assertEquals(division_final_match.completed,True)

        division_final_match = self.tables.DivisionFinalMatch()
        self.tables.DivisionFinalMatch.query.filter_by.return_value.first.return_value = division_final_match        
        tiebreaker_scores_dict["expected_num_tiebreaker_winners"]=1
        resolve_tiebreakers(tiebreaker_scores_dict,self.mock_app)
        self.assertEquals(division_final_match_player_results[0].won_tiebreaker,False)
        self.assertEquals(division_final_match_player_results[1].won_tiebreaker,False)
        self.assertEquals(division_final_match_player_results[2].won_tiebreaker,True)
        self.assertEquals(division_final_match.completed,True)
        
    def test_record_scores_half_completed(self):        
        game_player_results = [
            self.mock_app.tables.DivisionFinalMatchGamePlayerResult(
                division_final_match_game_player_result_id=1
            ),
            self.mock_app.tables.DivisionFinalMatchGamePlayerResult(
                division_final_match_game_player_result_id=2
            ),
            self.mock_app.tables.DivisionFinalMatchGamePlayerResult(
                division_final_match_game_player_result_id=3
            ),
            self.mock_app.tables.DivisionFinalMatchGamePlayerResult(
                division_final_match_game_player_result_id=4
            )
        ]
        
        game_result = self.mock_app.tables.DivisionFinalMatchGameResult(
            division_final_match_game_player_results=game_player_results
        )

        self.generated_brackets_match_game_dict['division_final_match_game_player_results'][0]['score']=126
        self.generated_brackets_match_game_dict['division_final_match_game_player_results'][1]['score']=125
        self.generated_brackets_match_game_dict['division_machine_string']="new machine"
        
        record_scores(self.generated_brackets_match_game_dict,game_result,self.mock_app)
        self.assertEquals(game_result.division_machine_string,'new machine')        
        self.assertEquals(game_player_results[0].score,126)
        self.assertEquals(game_player_results[1].score,125)
        self.assertEquals(game_player_results[2].score,None)
        self.assertEquals(game_player_results[3].score,None)

    def test_record_scores_completed(self):        
        game_player_results = [
            self.mock_app.tables.DivisionFinalMatchGamePlayerResult(
                division_final_match_game_player_result_id=1
            ),
            self.mock_app.tables.DivisionFinalMatchGamePlayerResult(
                division_final_match_game_player_result_id=2
            ),
            self.mock_app.tables.DivisionFinalMatchGamePlayerResult(
                division_final_match_game_player_result_id=3
            ),
            self.mock_app.tables.DivisionFinalMatchGamePlayerResult(
                division_final_match_game_player_result_id=4
            )
        ]
        
        game_result = self.mock_app.tables.DivisionFinalMatchGameResult(
            division_final_match_game_player_results=game_player_results
        )

        self.generated_brackets_match_game_dict['division_final_match_game_player_results'][0]['score']=126
        self.generated_brackets_match_game_dict['division_final_match_game_player_results'][1]['score']=125
        self.generated_brackets_match_game_dict['division_final_match_game_player_results'][2]['score']=124
        self.generated_brackets_match_game_dict['division_final_match_game_player_results'][3]['score']=123
        
        self.generated_brackets_match_game_dict['division_machine_string']="new machine"
        
        record_scores(self.generated_brackets_match_game_dict,game_result,self.mock_app)
        self.assertEquals(game_result.division_machine_string,'new machine')        
        self.assertEquals(game_player_results[0].score,126)
        self.assertEquals(game_player_results[1].score,125)
        self.assertEquals(game_player_results[2].score,124)
        self.assertEquals(game_player_results[3].score,123)
        
        
