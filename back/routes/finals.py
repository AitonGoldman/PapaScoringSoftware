from ranking import Ranking
from blueprints import admin_login_blueprint,admin_manage_blueprint
from flask import jsonify,current_app,request
import json
from werkzeug.exceptions import BadRequest,Conflict
from util import db_util
from util.permissions import Admin_permission, Desk_permission, Scorekeeper_permission
from flask_login import login_required,current_user
from routes.utils import fetch_entity
import os
from orm_creation import create_player,create_user,RolesEnum
import random

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

def get_finals_players_with_seed(seed, division_final_id):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    return tables.FinalsPlayer.query.filter_by(initial_seed=seed,division_final_id=division_final_id).all()        
    
def fill_in_player_match_results(player_string,
                                 match_template,
                                 new_finals_match_player_result,
                                 division_final_id):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    if player_string in match_template:
        #player_Xs = tables.FinalsPlayer.query.filter_by(initial_seed=match_template[player_string]).all()
        player_Xs = get_finals_players_with_seed(match_template[player_string],division_final_id)
        if len(player_Xs) > 1:                    
            print "uh oh - found some ties"
            pass
        player_X_id = player_Xs[0].finals_player_id        
        new_finals_match_player_result.finals_player_id=player_X_id        
        db.session.commit()
        
@admin_manage_blueprint.route('/finals/finals_match_game_result/<finals_match_game_result_id>/game_name/<game_name>',
                              methods=['PUT'])
@login_required
@Scorekeeper_permission.require(403)
def route_set_finals_match_result_game(finals_match_game_result_id,game_name):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    finals_match_game_result = fetch_entity(tables.FinalsMatchGameResult,finals_match_game_result_id)
    finals_match_game_result.division_machine_string = game_name
    db.session.commit()
    return jsonify({'data':'success'})

@admin_manage_blueprint.route('/finals/finals_match_game_player_result/<finals_match_game_player_result_id>/finals_player/<finals_player_id>/play_order/<play_order>',
                              methods=['PUT'])
@login_required
@Scorekeeper_permission.require(403)
def route_set_finals_match_game_player_result_player(finals_match_game_player_result_id,finals_player_id,play_order):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    finals_match_game_player_result = fetch_entity(tables.FinalsMatchGamePlayerResult,finals_match_game_player_result_id)
    finals_match_game_player_result.finals_player_id = finals_player_id
    finals_match_game_player_result.play_order = play_order
    db.session.commit()
    return jsonify({'data':'success'})

@admin_manage_blueprint.route('/finals/finals_match_game_player_result/<finals_match_game_player_result_id>/score/<score>',
                              methods=['PUT'])
@login_required
@Scorekeeper_permission.require(403)
def route_set_finals_match_game_player_result_score(finals_match_game_player_result_id,score):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    finals_match_game_player_result = fetch_entity(tables.FinalsMatchGamePlayerResult,finals_match_game_player_result_id)
    finals_match_game_player_result.score = score    
    db.session.commit()
    return jsonify({'data':'success'})

@admin_manage_blueprint.route('/finals/finals_match_game_result/<finals_match_game_result_id>/completed',
                              methods=['PUT'])
@login_required
@Scorekeeper_permission.require(403)
def route_set_finals_match_game_player_result_completed(finals_match_game_result_id):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    finals_match_game_result = fetch_entity(tables.FinalsMatchGameResult,finals_match_game_result_id)
    finals_match_game_result.completed = True
    sorted_player_results = sorted(finals_match_game_result.finals_match_game_player_results, key=lambda player_result: player_result.score)
    papa_points = [0,1,2,4]
    for idx,finals_match_game_player_result in enumerate(sorted_player_results):
        finals_match_game_player_result.papa_points=papa_points[idx]
    db.session.commit()
    return jsonify({'data':'success'})

@admin_manage_blueprint.route('/finals/division_final_match/<division_final_match_id>/completed',
                              methods=['PUT'])
@login_required
@Scorekeeper_permission.require(403)
def route_set_division_final_match_completed(division_final_match_id):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    division_final_match = fetch_entity(tables.DivisionFinalMatch,division_final_match_id)
    papa_points_sum = {}
    for finals_player_result in division_final_match.finals_match_player_results:        
        papa_points_sum[finals_player_result.finals_player_id]=0        
    for finals_match_game_result in division_final_match.finals_match_game_results:
        for finals_match_game_player_result in finals_match_game_result.finals_match_game_player_results:            
            papa_points_sum[finals_match_game_player_result.finals_player_id] = papa_points_sum[finals_match_game_player_result.finals_player_id] + finals_match_game_player_result.papa_points
    sorted_player_results = sorted(papa_points_sum, key=lambda player_result_id: papa_points_sum[player_result_id],reverse=True)
    
    for idx,sum in enumerate(sorted_player_results):
        
        if idx > 0 and papa_points_sum[sorted_player_results[idx-1]] == papa_points_sum[sorted_player_results[idx]]:            
            division_final_match.has_tiebreaker=True
            db.session.commit()            
    for finals_player_result in division_final_match.finals_match_player_results:        
        finals_player_result.papa_points_sum = papa_points_sum[finals_player_result.finals_player_id]
    db.session.commit()
    if division_final_match.has_tiebreaker is False:
        division_final_match.completed = True
        db.session.commit()
        for finals_player_result in division_final_match.finals_match_player_results:        
            if finals_player_result.finals_player_id == sorted_player_results[0] or finals_player_result.finals_player_id == sorted_player_results[1]:
                finals_player_result.winner = True
            else:
                finals_player_result.winner = False                
        db.session.commit()
        return jsonify({'data':'success'})
    mark_finals_match_player_results_that_need_tiebreaker(division_final_match)
    return jsonify({'data':'success'})

def mark_finals_match_player_results_that_need_tiebreaker(division_final_match):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    sorted_finals_match_player_results = sorted(division_final_match.finals_match_player_results,key= lambda e: e.papa_points_sum,reverse=True)
    ranked_finals_match_player_results = list(Ranking(sorted_finals_match_player_results, key= lambda pp: pp.papa_points_sum))    
    if ranked_finals_match_player_results[1][0] == ranked_finals_match_player_results[2][0]:        
        ranked_finals_match_player_results[1][1].needs_tiebreaker=True
        ranked_finals_match_player_results[2][1].needs_tiebreaker=True                
        if ranked_finals_match_player_results[1][0] == ranked_finals_match_player_results[0][0]:
            ranked_finals_match_player_results[0][1].needs_tiebreaker=True                            
        if ranked_finals_match_player_results[1][0] == ranked_finals_match_player_results[3][0]:
            ranked_finals_match_player_results[3][1].needs_tiebreaker=True                                        
    
    db.session.commit()

@admin_manage_blueprint.route('/finals/finals_match_game_result/<finals_match_game_result_id>',
                              methods=['GET'])
@login_required
@Scorekeeper_permission.require(403)
def route_get_finals_match_game_result(finals_match_game_result_id):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    finals_match_game_result = fetch_entity(tables.FinalsMatchGameResult,finals_match_game_result_id)
    #players = {finals_player.finals_player_id:finals_player.to_dict_simple() for finals_player in tables.FinalsPlayer.query.join(tables.FinalsMatchGamePlayerResult).filter_by(finals_match_game_result_id=finals_match_game_result_id).all()}    
    return jsonify({'data':finals_match_game_result.to_dict_simple()})

@admin_manage_blueprint.route('/finals/division_finals_match/<division_finals_match_id>',
                              methods=['GET'])
@login_required
@Scorekeeper_permission.require(403)
def route_get_finals_match_game_result_players(division_finals_match_id):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    division_finals_match = fetch_entity(tables.DivisionFinalMatch,division_finals_match_id)    
    return jsonify({'data':division_finals_match.to_dict_simple()})


@admin_manage_blueprint.route('/finals/division/<division_id>',methods=['POST'])
@login_required
@Scorekeeper_permission.require(403)
def route_create_finals(division_id):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    input_data = json.loads(request.data)    
    division = fetch_entity(tables.Division, division_id)         
    bracket_template_4_player_groups = [
        {
            'round':1,
            'matches':[
                generate_rank_matchup_dict([9,16,17,24]),
                generate_rank_matchup_dict([10,15,18,23]),
                generate_rank_matchup_dict([11,14,19,22]),
                generate_rank_matchup_dict([12,13,20,21]),            
            ]
        },
        {
            'round':2,
            'matches':[
                generate_rank_matchup_dict([1,8]),
                generate_rank_matchup_dict([2,7]),
                generate_rank_matchup_dict([3,6]),
                generate_rank_matchup_dict([4,5]),                            
            ]
        },
        {
            'round':3,
            'matches':[
                {},
                {}                                
            ]
        },
        {
            'round':4,
            'matches':[
                {}                                
            ]
        }
    ]
    new_final = tables.DivisionFinal(
        division_id=division_id
    )
    db.session.add(new_final)
    db.session.commit()
    for finals_player in input_data:
        new_finals_player = tables.FinalsPlayer(
            player_id=finals_player[0],
            initial_seed=finals_player[1],
            division_final_id=new_final.division_final_id
        )
        db.session.add(new_finals_player)
        db.session.commit()
    
    for round in bracket_template_4_player_groups:
        new_round = tables.DivisionFinalRound(
            round_number=round['round']
        )
        
        db.session.add(new_round)
        new_final.division_final_rounds.append(new_round)
        db.session.commit()
        for match_template in round['matches']:
            new_match = tables.DivisionFinalMatch(
                number_of_games = division.finals_num_games_per_match                
            )
            db.session.add(new_match)
            new_round.division_final_matches.append(new_match)
            db.session.commit()
            new_finals_match_player_results=[]
            for player_x in range(4):
                new_finals_match_player_results.append(tables.FinalsMatchPlayerResult())
                db.session.add(new_finals_match_player_results[player_x])
                db.session.commit()
            fill_in_player_match_results('player_one', match_template, new_finals_match_player_results[0],new_final.division_final_id)
            fill_in_player_match_results('player_two', match_template, new_finals_match_player_results[1],new_final.division_final_id)
            fill_in_player_match_results('player_three', match_template, new_finals_match_player_results[2],new_final.division_final_id)
            fill_in_player_match_results('player_four', match_template, new_finals_match_player_results[3],new_final.division_final_id)

            if round['round'] != 1:
                return jsonify(new_final.to_dict_simple())        
            for finals_match_player_result in new_finals_match_player_results:
                db.session.add(finals_match_player_result)
                new_match.finals_match_player_results.append(finals_match_player_result)
                db.session.commit()
            for game_x in range(division.finals_num_games_per_match):
                new_finals_match_game_results = tables.FinalsMatchGameResult()
                db.session.add(new_finals_match_game_results)
                db.session.commit()
                new_match.finals_match_game_results.append(new_finals_match_game_results)
                for player_position_string,value in match_template.iteritems():                    
                    player_Xs = get_finals_players_with_seed(match_template[player_position_string],new_final.division_final_id)
                    if len(player_Xs) > 1:
                        raise BadRequest('oops - need code to deal with ties')
                    new_finals_match_game_player_result = tables.FinalsMatchGamePlayerResult(
                        finals_player_id=player_Xs[0].finals_player_id
                    )
                    db.session.add(new_finals_match_game_player_result)                    
                    db.session.commit()
                    new_finals_match_game_results.finals_match_game_player_results.append(new_finals_match_game_player_result)
                    db.session.commit()
                    
            #     pass
    return jsonify(new_final.to_dict_simple())        
        
