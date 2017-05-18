from random import shuffle
from ranking import Ranking
from blueprints import admin_login_blueprint,admin_manage_blueprint
from flask import jsonify,current_app,request
import json
from werkzeug.exceptions import BadRequest,Conflict
from util import db_util
from util.permissions import Admin_permission, Desk_permission, Scorekeeper_permission
from flask_login import login_required,current_user
from routes.utils import fetch_entity
from routes.results import get_division_results
import os
from orm_creation import create_player,create_user,RolesEnum
import random
import collections
from flask_restless.helpers import to_dict

def generate_rank_matchup_dict(match_ups):
    if match_ups is None:
        return {}
    return_dict = {
        'player_one':match_ups[0],
        'player_two':match_ups[1]
    }
    if len(match_ups) > 2:        
        return_dict['player_three']=match_ups[2]
        return_dict['player_four']=match_ups[3]
    return return_dict

# def get_finals_players_with_seed(seed, division_final_id):
#     db = db_util.app_db_handle(current_app)
#     tables = db_util.app_db_tables(current_app)
#     return tables.FinalsPlayer.query.filter_by(adjusted_seed=seed,division_final_id=division_final_id).all()        
    
# def fill_in_player_match_results(player_string,
#                                  match_template,
#                                  new_finals_match_player_result,
#                                  division_final_id):
#     db = db_util.app_db_handle(current_app)
#     tables = db_util.app_db_tables(current_app)
#     if player_string in match_template:
#         #player_Xs = tables.FinalsPlayer.query.filter_by(initial_seed=match_template[player_string]).all()
#         player_Xs = get_finals_players_with_seed(match_template[player_string],division_final_id)
#         if len(player_Xs) > 1:                                
#             pass
#         if len(player_Xs)==0:
#             player_X_id = None
#         else:
#             player_X_id = player_Xs[0].finals_player_id        
#         new_finals_match_player_result.finals_player_id=player_X_id        
#         db.session.commit()
        
# @admin_manage_blueprint.route('/finals/finals_match_game_result/<finals_match_game_result_id>/game_name/<game_name>',
#                               methods=['PUT'])
# @login_required
# @Scorekeeper_permission.require(403)
# def route_set_finals_match_result_game(finals_match_game_result_id,game_name):
#     db = db_util.app_db_handle(current_app)
#     tables = db_util.app_db_tables(current_app)
#     finals_match_game_result = fetch_entity(tables.FinalsMatchGameResult,finals_match_game_result_id)
#     finals_match_game_result.division_machine_string = game_name
#     db.session.commit()
#     return jsonify({'data':'success'})


# @admin_manage_blueprint.route('/finals/finals_match_game_result/<finals_match_game_result_id>',
#                               methods=['PUT'])
# @login_required
# @Scorekeeper_permission.require(403)
# def route_update_finals_match_game_result(finals_match_game_result_id):
#     db = db_util.app_db_handle(current_app)
#     tables = db_util.app_db_tables(current_app)
#     input_data = json.loads(request.data)        
#     players_in_game = [game_result['finals_player_id'] for game_result in input_data['finals_match_game_player_results']]
#     dupe_list = [item for item, count in collections.Counter(players_in_game).items() if count > 1 and item is not None]
#     print dupe_list
#     if len(dupe_list) > 0:
#        raise BadRequest('poop')
        
#     for idx,game_player_result in enumerate(input_data['finals_match_game_player_results']):
#         game_player_result_id = game_player_result['finals_match_game_player_result_id']
#         game_player_result_model = fetch_entity(tables.FinalsMatchGamePlayerResult,game_player_result_id)
#         #game_player_result_model.play_order = idx
#         if 'finals_player_id' in game_player_result:            
#             game_player_result_model.finals_player_id = game_player_result['finals_player_id']
#             if 'score' in game_player_result and game_player_result['score'] is not None:
#                 game_player_result_model.score = str(game_player_result['score']).replace(",","")
#         db.session.commit()
#     number_scores_recorded_on_game = len(tables.FinalsMatchGamePlayerResult.query.filter_by(finals_match_game_result_id=input_data['finals_match_game_result_id']).filter(tables.FinalsMatchGamePlayerResult.score != None).all())    
#     finals_match_game_result=tables.FinalsMatchGameResult.query.filter_by(finals_match_game_result_id=input_data['finals_match_game_result_id']).first()
#     if number_scores_recorded_on_game == 4:        
#         finals_match_game_result.ready_to_be_completed=True
#         db.session.commit()
#     if 'division_machine_string' in input_data:
#         finals_match_game_result.division_machine_string=input_data['division_machine_string']
#         db.session.commit()                        
#     if input_data['completed'] is True:
#         sorted_player_results = sorted(finals_match_game_result.finals_match_game_player_results, key=lambda player_result: player_result.score)
#         papa_points = [0,1,2,4]
#         for idx,finals_match_game_player_result in enumerate(sorted_player_results):
#             finals_match_game_player_result.papa_points=papa_points[idx]
        
#         finals_match_game_result.completed=True
#         db.session.commit()
#         for idx,finals_match_game_player_result in enumerate(sorted_player_results):            
#             finals_match_player_result = tables.FinalsMatchPlayerResult.query.filter_by(finals_player_id=finals_match_game_player_result.finals_player_id).join(tables.DivisionFinalMatch).filter_by(division_final_match_id=finals_match_game_result.division_final_match_id).first()
#             if finals_match_player_result.papa_points_sum:
#                 finals_match_player_result.papa_points_sum=finals_match_player_result.papa_points_sum+papa_points[idx]            
#             else:                        
#                 finals_match_player_result.papa_points_sum=papa_points[idx]
#         db.session.commit()
        
#     return jsonify({})

# @admin_manage_blueprint.route('/finals/finals_match_game_player_result/<finals_match_game_player_result_id>/finals_player/<finals_player_id>/play_order/<play_order>',
#                               methods=['PUT'])
# @login_required
# @Scorekeeper_permission.require(403)
# def route_set_finals_match_game_player_result_player(finals_match_game_player_result_id,finals_player_id,play_order):
#     db = db_util.app_db_handle(current_app)
#     tables = db_util.app_db_tables(current_app)
#     finals_match_game_player_result = fetch_entity(tables.FinalsMatchGamePlayerResult,finals_match_game_player_result_id)
#     finals_match_game_player_result.finals_player_id = finals_player_id
#     finals_match_game_player_result.play_order = play_order
#     db.session.commit()
#     return jsonify({'data':'success'})

# @admin_manage_blueprint.route('/finals/finals_match_game_player_result/<finals_match_game_player_result_id>/score/<score>',
#                               methods=['PUT'])
# @login_required
# @Scorekeeper_permission.require(403)
# def route_set_finals_match_game_player_result_score(finals_match_game_player_result_id,score):
#     db = db_util.app_db_handle(current_app)
#     tables = db_util.app_db_tables(current_app)
#     finals_match_game_player_result = fetch_entity(tables.FinalsMatchGamePlayerResult,finals_match_game_player_result_id)
#     finals_match_game_result = fetch_entity(tables.FinalsMatchGameResult,finals_match_game_player_result.finals_match_game_result_id)
    
#     finals_match_game_player_result.score = score    
#     db.session.commit()
#     number_scores_recorded_on_game = len(tables.FinalsMatchGamePlayerResult.query.filter_by(finals_match_game_result_id=finals_match_game_player_result.finals_match_game_result_id).all())
#     if number_scores_recorded_on_game == 4:
#         finals_match_game_result.ready_to_be_completed=True
#         db.session.commit()        
#     return jsonify({'data':'success'})

# @admin_manage_blueprint.route('/finals/division_final_round/<division_final_round_id>/completed',
#                               methods=['PUT'])
# @login_required
# @Scorekeeper_permission.require(403)
# def route_set_division_final_round_completed(division_final_round_id):
#     db = db_util.app_db_handle(current_app)
#     tables = db_util.app_db_tables(current_app)
#     division_final_round = fetch_entity(tables.DivisionFinalRound,division_final_round_id)
#     next_round=str(int(division_final_round.round_number)+1)
#     division_final_next_round = tables.DivisionFinalRound.query.filter_by(division_final_id=division_final_round.division_final_id,round_number=next_round).first()
#     division_final_round.completed=True

#     final_rank_lookup = {
#         4:0,
#         3:4,
#         2:8,
#         1:16 
#     }
#     offset = final_rank_lookup[int(division_final_round.round_number)]
#     num_of_rounds = len(tables.DivisionFinalRound.query.filter_by(division_final_id=division_final_round.division_final_id).all())
#     if int(division_final_round.round_number) != num_of_rounds:
#         round_losers = tables.FinalsMatchPlayerResult.query.filter_by(winner=False).join(tables.DivisionFinalMatch).filter_by(division_final_round_id=division_final_round.division_final_round_id).order_by(tables.FinalsMatchPlayerResult.papa_points_sum).all()
#     else:
#         round_losers = tables.FinalsMatchPlayerResult.query.join(tables.DivisionFinalMatch).filter_by(division_final_round_id=division_final_round.division_final_round_id).order_by(tables.FinalsMatchPlayerResult.papa_points_sum).all()
#     sorted_finals_match_player_losers_results = sorted(round_losers,key= lambda e: e.papa_points_sum,reverse=True)
#     ranked_finals_match_player_losers_results = list(Ranking(sorted_finals_match_player_losers_results, key= lambda pp: pp.papa_points_sum))    
#     for loser in ranked_finals_match_player_losers_results:
#         loser[1].finals_player.overall_rank=loser[0]+1+offset
#         db.session.commit()            
#     if division_final_next_round is None:
#         return jsonify({'data':'success'})    
#     db.session.commit()
#     list_of_winners=[]
#     next_round_id = division_final_next_round.division_final_round_id
#     next_round_finals_match_player_results = tables.FinalsMatchPlayerResult.query.filter(tables.FinalsMatchPlayerResult.finals_player_id!=None).join(tables.DivisionFinalMatch).filter_by(division_final_round_id=next_round_id).all()
#     for player in next_round_finals_match_player_results:
#         finals_player = tables.FinalsPlayer.query.filter_by(finals_player_id=player.finals_player_id).first()
#         list_of_winners.append([player.finals_player_id,finals_player.adjusted_seed])
#         player.finals_player_id=None
#     winners = tables.FinalsMatchPlayerResult.query.filter_by(winner=True).join(tables.DivisionFinalMatch).filter_by(division_final_round_id=division_final_round.division_final_round_id).all()
#     for winner in winners:
#         finals_player = tables.FinalsPlayer.query.filter_by(finals_player_id=winner.finals_player_id).first()
#         list_of_winners.append([winner.finals_player_id,finals_player.adjusted_seed])
#     sorted_finals_player_list = sorted(list_of_winners, key= lambda e: e[1],reverse=True)
#     halfway_idx = (len(sorted_finals_player_list)/2)
#     sorted_finals_player_list_a = sorted_finals_player_list[:halfway_idx]
#     sorted_finals_player_list_b = sorted_finals_player_list[halfway_idx:]
#     for match in tables.DivisionFinalMatch.query.filter_by(division_final_round_id=division_final_next_round.division_final_round_id).order_by(tables.DivisionFinalMatch.division_final_match_id).all():
#         players_to_add = []
#         players_to_add.append(sorted_finals_player_list_a.pop())
#         players_to_add.append(sorted_finals_player_list_a.pop(0))
#         players_to_add.append(sorted_finals_player_list_b.pop())
#         players_to_add.append(sorted_finals_player_list_b.pop(0))
#         for idx,final_match_player_result in enumerate(match.finals_match_player_results):
#             final_match_player_result.finals_player_id=players_to_add[idx][0]
#         db.session.commit()
#         #for finals_match_game_result in match.finals_match_game_results:
#         #    for idx,finals_match_game_player_result in enumerate(finals_match_game_result.finals_match_game_player_results):
#         #        finals_match_game_player_result.finals_player_id=players_to_add[idx][0]        
#     db.session.commit()
#     return jsonify({})
    
# @admin_manage_blueprint.route('/finals/finals_match_game_result/<finals_match_game_result_id>/completed',
#                               methods=['PUT'])
# @login_required
# @Scorekeeper_permission.require(403)
# def route_set_finals_match_game_player_result_completed(finals_match_game_result_id):    
    
#     db = db_util.app_db_handle(current_app)
#     tables = db_util.app_db_tables(current_app)
#     finals_match_game_result = fetch_entity(tables.FinalsMatchGameResult,finals_match_game_result_id)
#     finals_match_game_result.completed = True
#     sorted_player_results = sorted(finals_match_game_result.finals_match_game_player_results, key=lambda player_result: player_result.score)
#     papa_points = [0,1,2,4]
#     for idx,finals_match_game_player_result in enumerate(sorted_player_results):
#         finals_match_game_player_result.papa_points=papa_points[idx]
#     db.session.commit()    
#     for idx,finals_match_game_player_result in enumerate(sorted_player_results):
#         print "poop2"
#         finals_match_player_result = tables.FinalsMatchPlayerResult.query.filter_by(finals_player_id=finals_match_game_player_result.finals_player_id).join(tables.DivisionFinalMatch).join(tables.FinalsMatchGameResult).filter_by(division_final_match_id=finals_match_game_result.division_final_match_id).first()
#         if finals_match_player_result.papa_points_sum:
#             finals_match_player_result.papa_points_sum=finals_match_player_result.papa_points_sum+papa_points[idx]            
#         else:                        
#             finals_match_player_result.papa_points_sum=papa_points[idx]
#     db.session.commit()
#     return jsonify({'data':'success'})

# @admin_manage_blueprint.route('/finals/division_final_match/<division_final_match_id>/tie_breaker_machine/<division_final_match_tiebreaker_machine_name>',
#                               methods=['PUT'])
# @login_required
# @Scorekeeper_permission.require(403)
# def route_set_division_final_match_tie_breaker_machine(division_final_match_id,division_final_match_tiebreaker_machine_name):
#     db = db_util.app_db_handle(current_app)
#     tables = db_util.app_db_tables(current_app)
#     division_final_match = fetch_entity(tables.DivisionFinalMatch,division_final_match_id)
#     division_final_match.tiebreaker_division_machine_name = division_final_match_tiebreaker_machine_name
#     db.session.commit()
#     pass

# @admin_manage_blueprint.route('/finals/tie_breaker_results/division_final_match',
#                               methods=['PUT'])
# @login_required
# @Scorekeeper_permission.require(403)
# def route_set_division_final_match_tiebreaker_results():
#     db = db_util.app_db_handle(current_app)
#     tables = db_util.app_db_tables(current_app)
#     input_data = json.loads(request.data)    
#     division_final_match = fetch_entity(tables.DivisionFinalMatch,input_data['division_final_match_id'])
#     for finals_player in input_data['data']:
#         print "%s %s" % (division_final_match.division_final_match_id,finals_player[0])
#         finals_match_player_result = tables.FinalsMatchPlayerResult.query.filter_by(division_final_match_id=division_final_match.division_final_match_id,finals_player_id=finals_player[0]).first()
#         finals_match_player_result.won_tiebreaker=finals_player[1]
#         db.session.commit()
#     papa_points_sum,sorted_player_results = get_papa_points_sorted_list_of_match_players(division_final_match)
#     finals_match_player_results_has_tie = tables.FinalsMatchPlayerResult.query.filter_by(division_final_match_id=division_final_match.division_final_match_id,needs_tiebreaker=True).all()
#     finals_match_player_results_tie_winners = tables.FinalsMatchPlayerResult.query.filter_by(division_final_match_id=division_final_match.division_final_match_id,won_tiebreaker=True).all()
#     top_sorted_finals_match_player_results = tables.FinalsMatchPlayerResult.query.filter_by(division_final_match_id=division_final_match.division_final_match_id,finals_player_id=sorted_player_results[0]).first()
#     finals_players_ids = [finals_result.finals_player_id for finals_result in finals_match_player_results_has_tie]    
#     if len(finals_match_player_results_has_tie) == 2:
#         top_sorted_finals_match_player_results.winner=True        
#         finals_match_player_results_tie_winners[0].winner=True
#         db.session.commit()
        
#     if len(finals_match_player_results_has_tie) == 3 and sorted_player_results[0] not in finals_players_ids:
#         top_sorted_finals_match_player_results.winner=True                
#         finals_match_player_results_tie_winners[0].winner=True        
#         db.session.commit()        

#     if len(finals_match_player_results_has_tie) == 3 and sorted_player_results[0] in finals_players_ids:        
#         finals_match_player_results_tie_winners[0].winner=True        
#         finals_match_player_results_tie_winners[1].winner=True        
#         db.session.commit()
#     for finals_match_player_result in finals_match_player_results_has_tie:
#         if finals_match_player_result.winner is not True:
#             finals_match_player_result.winner=False    
#     division_final_match.completed=True
#     db.session.commit()
#     return jsonify({'data':'success'})

# def get_papa_points_sorted_list_of_match_players(division_final_match):
#     papa_points_sum = {}
#     for finals_player_result in division_final_match.finals_match_player_results:        
#         papa_points_sum[finals_player_result.finals_player_id]=0        
#     for finals_match_game_result in division_final_match.finals_match_game_results:
#         for finals_match_game_player_result in finals_match_game_result.finals_match_game_player_results:            
#             papa_points_sum[finals_match_game_player_result.finals_player_id] = papa_points_sum[finals_match_game_player_result.finals_player_id] + finals_match_game_player_result.papa_points
#     sorted_player_results = sorted(papa_points_sum, key=lambda player_result_id: papa_points_sum[player_result_id],reverse=True)
#     return papa_points_sum,sorted_player_results

# @admin_manage_blueprint.route('/finals/division_final_match/<division_final_match_id>/completed',
#                               methods=['PUT'])
# @login_required
# @Scorekeeper_permission.require(403)
# def route_set_division_final_match_completed(division_final_match_id):
#     db = db_util.app_db_handle(current_app)
#     tables = db_util.app_db_tables(current_app)
#     division_final_match = fetch_entity(tables.DivisionFinalMatch,division_final_match_id)

#     # papa_points_sum = {}
#     # for finals_player_result in division_final_match.finals_match_player_results:        
#     #     papa_points_sum[finals_player_result.finals_player_id]=0        
#     # for finals_match_game_result in division_final_match.finals_match_game_results:
#     #     for finals_match_game_player_result in finals_match_game_result.finals_match_game_player_results:            
#     #         papa_points_sum[finals_match_game_player_result.finals_player_id] = papa_points_sum[finals_match_game_player_result.finals_player_id] + finals_match_game_player_result.papa_points
#     # sorted_player_results = sorted(papa_points_sum, key=lambda player_result_id: papa_points_sum[player_result_id],reverse=True)
#     papa_points_sum,sorted_player_results = get_papa_points_sorted_list_of_match_players(division_final_match)
#     for idx,sum in enumerate(sorted_player_results):        
#         # if idx == 1 and papa_points_sum[sorted_player_results[idx-1]] == papa_points_sum[sorted_player_results[idx]]:            
#         #     division_final_match.has_tiebreaker=True
#         #     db.session.commit()
#         if idx == 2 and papa_points_sum[sorted_player_results[idx-1]] == papa_points_sum[sorted_player_results[idx]]:            
#             division_final_match.has_tiebreaker=True
#             db.session.commit()            
            
#     for finals_player_result in division_final_match.finals_match_player_results:        
#         finals_player_result.papa_points_sum = papa_points_sum[finals_player_result.finals_player_id]
#     db.session.commit()
#     if division_final_match.has_tiebreaker is False:
#         division_final_match.completed = True
#         db.session.commit()
#         for finals_player_result in division_final_match.finals_match_player_results:        
#             if finals_player_result.finals_player_id == sorted_player_results[0] or finals_player_result.finals_player_id == sorted_player_results[1]:
#                 finals_player_result.winner = True
#             else:
#                 finals_player_result.winner = False                
#         db.session.commit()
#         return jsonify({'data':'success'})
#     mark_finals_match_player_results_that_need_tiebreaker(division_final_match)
#     return jsonify({'data':'success'})

# def mark_finals_match_player_results_that_need_tiebreaker(division_final_match):
#     db = db_util.app_db_handle(current_app)
#     tables = db_util.app_db_tables(current_app)
#     sorted_finals_match_player_results = sorted(division_final_match.finals_match_player_results,key= lambda e: e.papa_points_sum,reverse=True)
#     ranked_finals_match_player_results = list(Ranking(sorted_finals_match_player_results, key= lambda pp: pp.papa_points_sum))    
#     if ranked_finals_match_player_results[1][0] == ranked_finals_match_player_results[2][0]:        
#         ranked_finals_match_player_results[1][1].needs_tiebreaker=True
#         ranked_finals_match_player_results[2][1].needs_tiebreaker=True
#         division_final_match.expected_num_tiebreaker_winners=1
#         if ranked_finals_match_player_results[1][0] == ranked_finals_match_player_results[0][0]:
#             division_final_match.expected_num_tiebreaker_winners=2            
#             ranked_finals_match_player_results[0][1].needs_tiebreaker=True                            
#         if ranked_finals_match_player_results[1][0] == ranked_finals_match_player_results[3][0]:
#             ranked_finals_match_player_results[3][1].needs_tiebreaker=True                                            
#     db.session.commit()

# @admin_manage_blueprint.route('/finals/finals_match_game_result/<finals_match_game_result_id>',
#                               methods=['GET'])
# def route_get_finals_match_game_result(finals_match_game_result_id):
#     db = db_util.app_db_handle(current_app)
#     tables = db_util.app_db_tables(current_app)
#     finals_match_game_result = fetch_entity(tables.FinalsMatchGameResult,finals_match_game_result_id)
#     #players = {finals_player.finals_player_id:finals_player.to_dict_simple() for finals_player in tables.FinalsPlayer.query.join(tables.FinalsMatchGamePlayerResult).filter_by(finals_match_game_result_id=finals_match_game_result_id).all()}    
#     return jsonify({'data':finals_match_game_result.to_dict_simple()})

# @admin_manage_blueprint.route('/finals/division_final/<division_final_id>',
#                               methods=['GET'])
# def route_get_final(division_final_id):
#     db = db_util.app_db_handle(current_app)
#     tables = db_util.app_db_tables(current_app)
#     final = fetch_entity(tables.DivisionFinal,division_final_id)
#     return jsonify({'data':final.to_dict_simple()})

# @admin_manage_blueprint.route('/finals/division_final',
#                               methods=['GET'])
# def route_get_all_finals():
#     db = db_util.app_db_handle(current_app)
#     tables = db_util.app_db_tables(current_app)
#     finals = tables.DivisionFinal.query.all()
#     return jsonify({'data':{division_final.division_final_id:division_final.to_dict_simple() for division_final in finals}})

    
# @admin_manage_blueprint.route('/finals/division_finals_match/<division_finals_match_id>',
#                               methods=['GET'])
# def route_get_finals_match_game_result_players(division_finals_match_id):
#     db = db_util.app_db_handle(current_app)
#     tables = db_util.app_db_tables(current_app)
#     division_finals_match = fetch_entity(tables.DivisionFinalMatch,division_finals_match_id)    
#     return jsonify({'data':division_finals_match.to_dict_simple()})


# @admin_manage_blueprint.route('/finals/division/<division_id>/extra_name_info/<extra_name_info>',methods=['POST'])
# @login_required
# @Scorekeeper_permission.require(403)
# def route_create_finals(division_id,extra_name_info):
#     db = db_util.app_db_handle(current_app)
#     tables = db_util.app_db_tables(current_app)
#     input_data = json.loads(request.data)    
#     division = fetch_entity(tables.Division, division_id)         
#     bracket_template_4_player_groups_24_players = [
#         {
#             'round':1,
#             'matches':[
#                 generate_rank_matchup_dict([9,16,17,24]),
#                 generate_rank_matchup_dict([10,15,18,23]),
#                 generate_rank_matchup_dict([11,14,19,22]),
#                 generate_rank_matchup_dict([12,13,20,21])            
#             ]
#         },
#         {
#             'round':2,
#             'matches':[
#                 generate_rank_matchup_dict([1,8, None, None]),
#                 generate_rank_matchup_dict([2,7, None, None]),
#                 generate_rank_matchup_dict([3,6, None, None]),
#                 generate_rank_matchup_dict([4,5, None, None])                            
#             ]
#         },
#         {
#             'round':3,
#             'matches':[
#                 generate_rank_matchup_dict([None,None, None, None]),
#                 generate_rank_matchup_dict([None,None, None, None])                            
#             ]
#         },
#         {
#             'round':4,
#             'matches':[
#                 generate_rank_matchup_dict([None,None, None, None])                                            
#             ]
#         }
#     ]

#     bracket_template_4_player_groups_16_players = [
#         {
#             'round':1,
#             'matches':[
#                 generate_rank_matchup_dict([1,8,9,16]),
#                 generate_rank_matchup_dict([2,7,10,15]),
#                 generate_rank_matchup_dict([3,6,11,14]),
#                 generate_rank_matchup_dict([4,5,12,13])            
#             ]
#         },
#         {
#             'round':2,
#             'matches':[
#                 generate_rank_matchup_dict([None,None, None, None]),
#                 generate_rank_matchup_dict([None,None, None, None]), 
#             ]
#         },
#         {
#             'round':3,
#             'matches':[
#                 generate_rank_matchup_dict([None,None, None, None])                
#             ]
#         }
#     ]
    
#     bracket_template_4_player_groups_8_players = [
#         {
#             'round':1,
#             'matches':[
#                 generate_rank_matchup_dict([1,8,4,5]),                                
#                 generate_rank_matchup_dict([2,7,3,6])            
#             ]
#         },
#         {
#             'round':2,
#             'matches':[
#                 generate_rank_matchup_dict([None,None, None, None]),                
#             ]
#         }
#     ]    
    
#     new_final = tables.DivisionFinal(
#         division_id=division_id
#     )
#     if extra_name_info and extra_name_info != "none":
#         new_final.extra_name_info=extra_name_info
#     db.session.add(new_final)
#     db.session.commit()

#     # need to add adjusted_seed to finals player
#     # set initial_seed on finals player
#     # look for finals player with adjusted_seed = initial_seed 
#     # if we don't find one, then adjusted_seed = initial seed
#     # if we do find one...
#     ## repeat the following until we find a None : if we find one, look for finals player with adjusted_seed + 1
#     ## set adjusted_seed to initial_seed + x 
#     for finals_player in input_data:
#         new_finals_player = tables.FinalsPlayer(
#             #player_id=finals_player[0],
#             initial_seed=finals_player[1],
#             division_final_id=new_final.division_final_id
#         )
#         if division.team_tournament:
#             new_finals_player.team_id=finals_player[0]
#         else:
#             new_finals_player.player_id=finals_player[0]
#         existing_player_seed = tables.FinalsPlayer.query.filter_by(initial_seed=int(finals_player[1]),division_final_id=new_final.division_final_id).all()
#         if len(existing_player_seed) > 0:
#             new_finals_player.adjusted_seed=int(finals_player[1])+len(existing_player_seed)
#         else:
#             new_finals_player.adjusted_seed=int(finals_player[1])
#         db.session.add(new_finals_player)
#         db.session.commit()

#     if division.finals_player_selection_type == 'papa':
#         if division.finals_num_qualifiers == 24:
#             bracket_template_for_division = bracket_template_4_player_groups_24_players
#         if division.finals_num_qualifiers == 16:
#             bracket_template_for_division = bracket_template_4_player_groups_16_players
#         if division.finals_num_qualifiers == 8:
#             bracket_template_for_division = bracket_template_4_player_groups_8_players            
#     else:
#         if extra_name_info == "A":
#             if division.finals_num_qualifiers_ppo_a == 24:
#                 bracket_template_for_division = bracket_template_4_player_groups_24_players
#             if division.finals_num_qualifiers_ppo_a == 16:
#                 bracket_template_for_division = bracket_template_4_player_groups_16_players
#         if extra_name_info == "B":
#             if division.finals_num_qualifiers_ppo_b == 24:
#                 bracket_template_for_division = bracket_template_4_player_groups_24_players
#             if division.finals_num_qualifiers_ppo_b == 16:
#                 bracket_template_for_division = bracket_template_4_player_groups_16_players

#     for round in bracket_template_for_division:
#         new_round = tables.DivisionFinalRound(
#             round_number=round['round']
#         )        
#         db.session.add(new_round)
#         new_final.division_final_rounds.append(new_round)
#         db.session.commit()
#         for match_template in round['matches']:
#             new_match = tables.DivisionFinalMatch(
#                 number_of_games = division.finals_num_games_per_match                
#             )
#             db.session.add(new_match)
#             new_round.division_final_matches.append(new_match)
#             db.session.commit()
#             new_finals_match_player_results=[]
#             for player_x in range(4):
#                 new_finals_match_player_results.append(tables.FinalsMatchPlayerResult())
#                 db.session.add(new_finals_match_player_results[player_x])
#                 db.session.commit()
#             fill_in_player_match_results('player_one', match_template, new_finals_match_player_results[0],new_final.division_final_id)
#             fill_in_player_match_results('player_two', match_template, new_finals_match_player_results[1],new_final.division_final_id)
#             fill_in_player_match_results('player_three', match_template, new_finals_match_player_results[2],new_final.division_final_id)
#             fill_in_player_match_results('player_four', match_template, new_finals_match_player_results[3],new_final.division_final_id)

#             #if round['round'] != 1:
#             #    return jsonify(new_final.to_dict_simple())        
#             for finals_match_player_result in new_finals_match_player_results:
#                 db.session.add(finals_match_player_result)
#                 new_match.finals_match_player_results.append(finals_match_player_result)
#                 db.session.commit()
#             for game_x in range(division.finals_num_games_per_match):
#                 new_finals_match_game_results = tables.FinalsMatchGameResult()
#                 db.session.add(new_finals_match_game_results)
#                 db.session.commit()
#                 new_match.finals_match_game_results.append(new_finals_match_game_results)
#                 play_order_idx = 0
#                 for player_position_string,value in match_template.iteritems():                    
#                     player_Xs = get_finals_players_with_seed(match_template[player_position_string],new_final.division_final_id)
#                     if len(player_Xs) > 1:
#                         raise BadRequest('oops - need code to deal with ties')
#                     new_finals_match_game_player_result = tables.FinalsMatchGamePlayerResult(
#                         #finals_player_id=player_Xs[0].finals_player_id
#                         play_order = play_order_idx
#                     )
#                     play_order_idx = play_order_idx+1
#                     #if round['round'] == 1:
#                         #new_finals_match_game_player_result.finals_player_id=player_Xs[0].finals_player_id
#                     db.session.add(new_finals_match_game_player_result)                    
#                     db.session.commit()
#                     new_finals_match_game_results.finals_match_game_player_results.append(new_finals_match_game_player_result)
#                     db.session.commit()
                    
#             #     pass
#     return jsonify(new_final.to_dict_simple())        


bracket_template_4_player_groups_24_players = [
    {
        'round':1,
        'matches':[
            generate_rank_matchup_dict([9,16,17,24]),
            generate_rank_matchup_dict([10,15,18,23]),
            generate_rank_matchup_dict([11,14,19,22]),
            generate_rank_matchup_dict([12,13,20,21])            
        ]
    },
    {
        'round':2,
        'matches':[
            generate_rank_matchup_dict([1,8, None, None]),
            generate_rank_matchup_dict([2,7, None, None]),
            generate_rank_matchup_dict([3,6, None, None]),
            generate_rank_matchup_dict([4,5, None, None])                            
        ]
    },
    {
        'round':3,
        'matches':[
            generate_rank_matchup_dict([None,None, None, None]),
            generate_rank_matchup_dict([None,None, None, None])                            
        ]
    },
    {
        'round':4,
        'matches':[
            generate_rank_matchup_dict([None,None, None, None])                                            
        ]
    }
]

bracket_template_4_player_groups_16_players = [
    {
        'round':1,
        'matches':[
            generate_rank_matchup_dict([1,8,9,16]),
            generate_rank_matchup_dict([2,7,10,15]),
            generate_rank_matchup_dict([3,6,11,14]),
            generate_rank_matchup_dict([4,5,12,13])            
        ]
    },
    {
        'round':2,
        'matches':[
            generate_rank_matchup_dict([None,None, None, None]),
            generate_rank_matchup_dict([None,None, None, None]), 
        ]
    },
    {
        'round':3,
        'matches':[
            generate_rank_matchup_dict([None,None, None, None])                
        ]
    }
]

bracket_template_4_player_groups_8_players = [
    {
        'round':1,
        'matches':[
            generate_rank_matchup_dict([1,8,4,5]),                                
            generate_rank_matchup_dict([2,7,3,6])            
        ]
    },
    {
        'round':2,
        'matches':[
            generate_rank_matchup_dict([None,None, None, None]),                
        ]
    }
]    


@admin_manage_blueprint.route('/finals/division_final/division_id/<division_final_id>',
                              methods=['DELETE'])
@login_required
@Admin_permission.require(403)
def route_delete_division_final_rounds(division_final_id):
    division_final = current_app.tables.DivisionFinal.query.filter_by(division_final_id=division_final_id).first()
    if division_final:
        current_app.tables.db_handle.session.delete(division_final)        
        current_app.tables.db_handle.session.commit()
        return jsonify({'data':None})
    else:
        return jsonify({'data':None})

@admin_manage_blueprint.route('/finals/division_final/division_id/<division_final_id>/round_count',
                              methods=['GET'])
def route_get_division_final_round_count(division_final_id):
    division_final_rounds = current_app.tables.DivisionFinalRound.query.filter_by(division_final_id=division_final_id).all()
    if len(division_final_rounds) > 0:                
        return jsonify({'data':len([division_final_round.to_dict_simple() for division_final_round in division_final_rounds])})
    else:
        return jsonify({'data':None})
    

@admin_manage_blueprint.route('/finals/division_final/division_id/<division_id>',
                              methods=['GET'])
def route_get_division_final(division_id):
    division_final = current_app.tables.DivisionFinal.query.filter_by(division_id=division_id).first()
    if division_final:
        return jsonify({'data':division_final.to_dict_simple()})
    else:
        return jsonify({'data':None})
 

@admin_manage_blueprint.route('/finals/division_final/division_id/<division_id>',
                              methods=['POST'])
@login_required
@Admin_permission.require(403)
def route_initialize_division_final(division_id):
    division_id=int(division_id)
    division = fetch_entity(current_app.tables.Division,division_id)
    division_results = get_division_results(division_id,return_json=False)
    division_results =  division_results['data']['ranked_player_list'][division_id]
    division_final = initialize_division_final(division_id, division.division_name, division_results, current_app)            
    return jsonify({'data':division_final.to_dict_simple()})    
    

@admin_manage_blueprint.route('/finals/division_final/division_id/<division_final_id>/tiebreakers',
                              methods=['POST'])
@login_required
@Scorekeeper_permission.require(403)
def route_record_tiebreaker_results(division_final_id):
    tiebreaker_results = json.loads(request.data)        
    division_final = fetch_entity(current_app.tables.DivisionFinal,division_final_id)
    tiebreaker_results_with_new_ranks = record_tiebreaker_results(division_final.qualifiers,tiebreaker_results,current_app)
    return jsonify({'data':tiebreaker_results_with_new_ranks})


@admin_manage_blueprint.route('/finals/division_final/division_id/<division_final_id>/rounds',
                              methods=['POST'])
@login_required
@Scorekeeper_permission.require(403)
def route_generate_brackets(division_final_id):
    division_final = fetch_entity(current_app.tables.DivisionFinal,division_final_id)
    division = fetch_entity(current_app.tables.Division,division_final.division_id)    
    rollcall_list = json.loads(request.data)#['data']    
    final_rounds = generate_brackets(current_app,division_final_id, rollcall_list,division.finals_num_qualifiers)    
    final_rounds_dicts = [final_round.to_dict_simple() for final_round in final_rounds]
    return jsonify({'data':to_dict(final_rounds_dicts)})


@admin_manage_blueprint.route('/finals/division_final/division_id/<division_final_id>/qualifiers',
                              methods=['GET','PUT'])
@login_required
@Scorekeeper_permission.require(403)
def route_get_or_change_division_final_qualifiers(division_final_id):
    division_final = fetch_entity(current_app.tables.DivisionFinal,division_final_id)
    division = fetch_entity(current_app.tables.Division,division_final.division_id)
    if request.data:
        rollcall_list = json.loads(request.data)#['data']
    else:
        sorted_player_list = sorted([division_final_player.to_dict_simple() for division_final_player in division_final.qualifiers],
                                    key= lambda e: e['initial_seed'])
        for index,player in enumerate(sorted_player_list):
            sorted_player_list[index]['removed']=False
            sorted_player_list[index]['reranked_seed']=sorted_player_list[index]['initial_seed']
        rollcall_list = create_simplified_division_results(sorted_player_list,
                                                           division.finals_num_qualifiers,
                                                           current_app)            
    
    modified_rollcall_list = remove_missing_final_player(rollcall_list, current_app)    
    divided_rollcall_list = create_simplified_division_results(modified_rollcall_list,division.finals_num_qualifiers, current_app)
    return jsonify({'data':divided_rollcall_list})

@admin_manage_blueprint.route('/finals/division_final/division_id/<division_final_id>/tiebreakers',
                              methods=['GET'])
@login_required
def route_get_tiebreakers(division_final_id):
    division_final = fetch_entity(current_app.tables.DivisionFinal,division_final_id)
    division = fetch_entity(current_app.tables.Division,division_final.division_id)    
    tiebreakers = get_tiebreakers_for_division(division_final.qualifiers,division.finals_num_qualifiers)
    return jsonify({'data':{'tiebreakers':tiebreakers}})

@admin_manage_blueprint.route('/finals/division_final/division_id/<division_final_id>/tiebreakers/important',
                              methods=['GET'])
@login_required
def route_get_important_tiebreakers(division_final_id):
    division_final = fetch_entity(current_app.tables.DivisionFinal,division_final_id)
    division = fetch_entity(current_app.tables.Division,division_final.division_id)    
    important_tiebreakers = get_important_tiebreakers_for_division(division_final.qualifiers,
                                                         division.finals_num_qualifiers,
                                                         get_important_ranks_for_tiebreakers(division.finals_num_qualifiers))
    return jsonify({'data':{'important_tiebreakers':important_tiebreakers}})


def resolve_unimportant_ties(division_final_player_list,num_qualifiers):
    tiebreaker_counts = {}    
    division_final_player_list = [player for player in division_final_player_list if player['type']=='result']
    for potential_tiebreaker_rank in range(0,num_qualifiers):
        tie_breaker_count = len(
            [final_player for final_player in division_final_player_list if final_player['reranked_seed'] == potential_tiebreaker_rank]
        )
        tiebreaker_counts[potential_tiebreaker_rank]=tie_breaker_count    
    shuffle(division_final_player_list)
    for player in division_final_player_list:
        if player['reranked_seed'] < num_qualifiers and tiebreaker_counts[player['reranked_seed']] > 1:
            tiebreaker_counts[player['reranked_seed']]=tiebreaker_counts[player['reranked_seed']]-1
            player['reranked_seed']=player['reranked_seed']+tiebreaker_counts[player['reranked_seed']]            
    return sorted(division_final_player_list, key= lambda e: e['reranked_seed'],reverse=False)

def generate_division_final_match_game_result(app,number_of_games=3,number_of_players=4,commit=False):
    division_final_match_game_results=[]    
    for game_index in range(number_of_games):
        division_final_match_game_player_results=[]        
        for player_index in range(number_of_players):        
            division_final_match_game_player_result=app.tables.DivisionFinalMatchGamePlayerResult()        
            division_final_match_game_player_results.append(division_final_match_game_player_result)        
        division_final_match_game_result=app.tables.DivisionFinalMatchGameResult()
        division_final_match_game_result.division_final_match_game_player_results=division_final_match_game_player_results
        division_final_match_game_results.append(division_final_match_game_result)        
        if commit:
            app.tables.db_handle.session.add(division_final_match_game_result)
    if commit:
        app.tables.db_handle.session.commit()
    return division_final_match_game_results

def generate_division_final_match_player_results(app,number_of_players=4,commit=False):
    division_final_match_player_results=[]
    for index in range(number_of_players):        
        division_final_match_player_result=app.tables.DivisionFinalMatchPlayerResult()        
        division_final_match_player_results.append(division_final_match_player_result)
        if commit:
            app.tables.db_handle.session.add(division_final_match_player_result)        
    if commit:
        app.tables.db_handle.session.commit()
    return division_final_match_player_results

def generate_division_final_matches(app,number_of_matches, commit=False):
    division_final_matches=[]
    for index in range(number_of_matches):        
        division_final_match=app.tables.DivisionFinalMatch()        
        division_final_match.final_match_game_results=generate_division_final_match_game_result(app)
        division_final_match.final_match_player_results=generate_division_final_match_player_results(app)
        division_final_matches.append(division_final_match)
        if commit:
            app.tables.db_handle.session.add(division_final_match)            
    if commit:
        app.tables.db_handle.session.commit()
    return division_final_matches

def generate_division_final_rounds(app,finals_template,division_final_id, division_final_player_list, commit=False):
    division_final_rounds=[]
    division_final_player_dict = {
        division_final_player.adjusted_seed:division_final_player for division_final_player in division_final_player_list        
    }    
    for round_info in finals_template:
        division_final_round=app.tables.DivisionFinalRound(
            division_final_id=division_final_id,
            round_number=round_info['round']
        )
        for match_index in range(len(round_info['matches'])):
            division_final_matches = generate_division_final_matches(app,len(round_info['matches']))
            division_final_round.division_final_matches=division_final_matches
        for index_1,division_final_match in enumerate(division_final_round.division_final_matches):
            p1_seed = finals_template[round_info['round']-1]['matches'][index_1]['player_one']
            p2_seed = finals_template[round_info['round']-1]['matches'][index_1]['player_two']
            p3_seed = finals_template[round_info['round']-1]['matches'][index_1]['player_three']
            p4_seed = finals_template[round_info['round']-1]['matches'][index_1]['player_four']

            for index_2,division_final_match_game_result in enumerate(division_final_match.final_match_game_results):
                game_player_result = division_final_match_game_result.division_final_match_game_player_results
                if p1_seed:
                    game_player_result[0].final_player_id = division_final_player_dict[p1_seed].final_player_id                     
                if p2_seed:
                    game_player_result[1].final_player_id = division_final_player_dict[p2_seed].final_player_id                                         
                if p3_seed:
                    game_player_result[2].final_player_id = division_final_player_dict[p3_seed].final_player_id                                         
                if p4_seed:                    
                    game_player_result[3].final_player_id = division_final_player_dict[p4_seed].final_player_id                                         
            match_player_results = division_final_match.final_match_player_results
            if p1_seed:
                match_player_results[0].final_player_id=division_final_player_dict[p1_seed].final_player_id
            if p2_seed:
                match_player_results[1].final_player_id=division_final_player_dict[p2_seed].final_player_id                
            if p3_seed:
                match_player_results[2].final_player_id=division_final_player_dict[p3_seed].final_player_id                
            if p4_seed:
                match_player_results[3].final_player_id=division_final_player_dict[p4_seed].final_player_id
        if commit:
            app.tables.db_handle.session.add(division_final_round)
        division_final_rounds.append(division_final_round)        
    if commit:
        app.tables.db_handle.session.commit()
    return division_final_rounds



def generate_brackets(app,division_final_id, division_final_player_list,num_qualifiers):    
    # fill in rounds and matches
    division_final_player_dict = {division_final_player['final_player_id']:division_final_player for division_final_player in resolve_unimportant_ties(division_final_player_list,num_qualifiers)}
    division_final_players_from_db = app.tables.DivisionFinalPlayer.query.filter_by(division_final_id=division_final_id).all()
    for division_final_player in division_final_players_from_db:        
        if division_final_player.final_player_id in division_final_player_dict:
            division_final_player.adjusted_seed=division_final_player_dict[division_final_player.final_player_id]['reranked_seed']
        else:
            print "uh oh !"
    final_rounds = generate_division_final_rounds(app,bracket_template_4_player_groups_24_players,division_final_id,division_final_players_from_db,commit=True)
    
    app.tables.db_handle.session.commit()
    return final_rounds

def get_important_ranks_for_tiebreakers(num_qualifiers):
    important_ranks_for_tiebreakers = {}
    important_ranks_for_tiebreakers['qualifying']=num_qualifiers-1
    if num_qualifiers == 24:
        important_ranks_for_tiebreakers['bye']=7        
    if num_qualifiers == 12:
        important_ranks_for_tiebreakers['bye']=3                
    return important_ranks_for_tiebreakers
        
def get_important_tiebreakers_for_division(division_final_players,num_qualifiers,important_seeds):
    num_players = len(division_final_players)
    tiebreakers_counts = {}
    important_tiebreaker_ranks = {}
    for potential_tiebreaker_rank in range(0,num_qualifiers+1):
        tie_breaker_count = len(
            [final_player for final_player in division_final_players if final_player.initial_seed == potential_tiebreaker_rank]
        )
        tiebreakers_counts[potential_tiebreaker_rank]=tie_breaker_count    
    for type,seed in important_seeds.iteritems():        
        if seed >= len(tiebreakers_counts)-1:
            continue
        if tiebreakers_counts[seed] > 1:
            important_tiebreaker_ranks[type]=seed        
        if tiebreakers_counts[seed] == 0 and tiebreakers_counts[seed+1] == 0:
            new_important_seed = seed-1
            while new_important_seed >= 0 :            
                if new_important_seed in tiebreakers_counts and tiebreakers_counts[new_important_seed] > 1:
                    important_tiebreaker_ranks[type]=new_important_seed        
                    break        
                new_important_seed = new_important_seed-1

    return important_tiebreaker_ranks

def get_tiebreakers_for_division(division_final_players,num_qualifiers):
    num_players = len(division_final_players)
    tiebreakers = []
    for potential_tiebreaker_rank in range(0,num_qualifiers):
        tiebreaker = [{'final_player_id':final_player.final_player_id,
                       'initial_seed':final_player.initial_seed,
                       'player_name':final_player.player_name,
                       'player_score':None} for final_player in division_final_players if final_player.initial_seed == potential_tiebreaker_rank]
        if len(tiebreaker) > 1:
            tiebreakers.append(tiebreaker) 
    return tiebreakers

def record_tiebreaker_results(division_final_players,tiebreaker_scores,app):
    sorted_tiebreaker_scores = sorted(tiebreaker_scores, key= lambda e: e['player_score'],reverse=True)
    initial_seed = sorted_tiebreaker_scores[0]['initial_seed']    
    tiebreaker_results_with_new_ranks = []
    for index,tiebreaker in enumerate(sorted_tiebreaker_scores):
        tiebreaker['initial_seed']=tiebreaker['initial_seed']+index    
    for final_player in division_final_players:
        for tiebreaker_result in tiebreaker_scores:
            if tiebreaker_result['final_player_id'] == final_player.final_player_id:
                final_player.initial_seed=tiebreaker_result['initial_seed']
                tiebreaker_results_with_new_ranks.append(final_player.to_dict_simple())
    app.tables.db_handle.session.commit()
    return tiebreaker_results_with_new_ranks

def initialize_division_final(division_id, division_name, division_results, app):
    existing_division_final = app.tables.DivisionFinal.query.filter_by(division_id=division_id).all()
    if existing_division_final:
        return existing_division_final
    division_final = app.tables.DivisionFinal(
        division_id=division_id,
        name=division_name,        
    )    
    create_division_final_players(division_final,division_results,app,commit=False)
    app.tables.db_handle.session.add(division_final)
    app.tables.db_handle.session.commit()
    return division_final

def create_division_final_players(division_final,
                                  division_results, app, commit=True):
    #NOTE : assume ranks in division_results start at 0, not 1
    division_final_players=[]
    for result in division_results:        
        division_final_player = app.tables.DivisionFinalPlayer(
            player_id=result[1]['player_id'],
            #FIXME : handle team stuff here
            initial_seed=result[0],
            player_name=result[1]['player_name']            
        )
        #division_final.qualifiers.append(division_final_player)
        division_final_players.append(division_final_player)        
    division_final.qualifiers=division_final_players
    if commit:
        app.tables.db_handle.session.commit()        
    return division_final_players
        
def remove_missing_final_player(final_player_list, app):
    pruned_final_players = []        
    final_player_list = [final_player for final_player in final_player_list if final_player['type'] == 'result']    
    for final_player in final_player_list:                        
        if 'removed' in final_player and final_player['removed'] is not True:                
            final_player['removed ']=False
            final_player['reranked_seed']=final_player['initial_seed']
            pruned_final_players.append(final_player)                
                
    sorted_final_players = sorted(pruned_final_players, key= lambda e: e['reranked_seed'])    
    reranked_pruned_final_players_list = list(Ranking(sorted_final_players,
                                                      key=lambda pp: pp['reranked_seed'],
                                                      reverse=True))
    # NOTE : reranked ranks start at 0, not 1
    reranked_pruned_final_players_hash = {final_player[1]["player_id"]:final_player[0] for final_player in reranked_pruned_final_players_list}
    for index,final_player in enumerate(final_player_list):
        #if 'removed' in final_player and final_player['removed']:
        #    final_player['initial_seed']=None
        if 'removed' in final_player and final_player['removed'] is False:        
            final_player['reranked_seed']=reranked_pruned_final_players_hash[final_player['player_id']]
    return final_player_list
        
def create_simplified_division_results(final_players, division_cutoff, app):    
    simplified_results = []    
    placed_divider=False

    # NOTE : expect ranks to start from 0, not 1, so we subtract 1 from division_cutoff
    division_cutoff = division_cutoff - 1
    
    for index,final_player in enumerate(final_players):        
        if final_player['reranked_seed'] > division_cutoff and placed_divider is False:            
            simplified_results.append({
                "type":"divider",
                "text":"Cutoff"            
            })
            placed_divider=True
        simplified_result = {
            "type":"result",
            "player_id":final_player['player_id'],
            "final_player_id":final_player['final_player_id'],
            "player_name":final_player['player_name'],
            "initial_seed":final_player['initial_seed'],            
            "reranked_seed":final_player['reranked_seed'],
            "removed":final_player['removed']
        }

        simplified_results.append(simplified_result)
    if placed_divider is False:
        simplified_results.append({
            "type":"divider",
            "text":"Cutoff"            
        })
    return simplified_results
    
def calculate_points_for_game(division_final_match_game_dict):
    player_scores = [division_final_match_game_player_result for division_final_match_game_player_result in division_final_match_game_dict['division_final_match_game_player_results'] if division_final_match_game_player_result['score'] is not None]
    
    if len(player_scores)<4:
        return    
    sorted_scores = sorted(player_scores, key= lambda e: e['score'])
    
    sorted_scores[0]['papa_points']=0
    sorted_scores[1]['papa_points']=1
    sorted_scores[2]['papa_points']=2
    sorted_scores[2]['winner']=True    
    sorted_scores[3]['papa_points']=4
    sorted_scores[3]['winner']=True    
    
    division_final_match_game_dict['division_final_match_game_player_results']=sorted_scores        
    division_final_match_game_dict['completed']=True
    
def calculate_points_for_match(division_final_match):
    for game_result in division_final_match['final_match_game_results']:
        calculate_points_for_game(game_result)        
    players_score={}    
    games_completed=0
    for game_result in division_final_match['final_match_game_results']:
        if game_result['completed'] is not True:
            continue
        games_completed=games_completed+1
        for division_final_match_game_player_result in game_result['division_final_match_game_player_results']:
            final_player_id = division_final_match_game_player_result['final_player_id']
            if final_player_id not in players_score:
                players_score[final_player_id]=0
            players_score[final_player_id]=players_score[final_player_id]+division_final_match_game_player_result['papa_points']
    for match_player_result in division_final_match['final_match_player_results']:
        if match_player_result['final_player_id'] in players_score:
            match_player_result['papa_points_sum']=players_score[match_player_result['final_player_id']]
    if games_completed == 3:
        tiebreaker_final_player_ids = calculate_tiebreakers(division_final_match)
    else:
        tiebreaker_final_player_ids = []        
    if len(tiebreaker_final_player_ids) > 0:        
        
        return    
    if games_completed==3:
        division_final_match['completed']=True
    
def calculate_tiebreakers(division_final_match_dict):
    sorted_scores = sorted(division_final_match_dict['final_match_player_results'], key= lambda e: e['papa_points_sum'])
    tiebreaker_final_player_ids=[]
    if sorted_scores[1]['papa_points_sum'] == sorted_scores[2]['papa_points_sum']:
        tiebreaker_final_player_ids.append(sorted_scores[1]['final_player_id'])
        tiebreaker_final_player_ids.append(sorted_scores[2]['final_player_id'])
    if sorted_scores[1]['papa_points_sum'] == sorted_scores[2]['papa_points_sum'] and sorted_scores[1]['papa_points_sum'] == sorted_scores[0]['papa_points_sum']:
        tiebreaker_final_player_ids.append(sorted_scores[0]['final_player_id'])
    if sorted_scores[1]['papa_points_sum'] == sorted_scores[2]['papa_points_sum'] and sorted_scores[1]['papa_points_sum'] == sorted_scores[3]['papa_points_sum']:
        tiebreaker_final_player_ids.append(sorted_scores[3]['final_player_id'])
    
    for match_player_result in division_final_match_dict['final_match_player_results']:
        if match_player_result['final_player_id'] in tiebreaker_final_player_ids:            
            match_player_result['needs_tiebreaker']=True
    return tiebreaker_final_player_ids
