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
    
def fill_in_player_match_results(player_string,
                                 match_template,
                                 new_finals_match_player_result):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    if player_string in match_template:
        player_Xs = tables.FinalsPlayer.query.filter_by(initial_seed=match_template[player_string]).all()        
        if len(player_Xs) > 1:                    
            print "uh oh - found some ties"
            pass
        player_X_id = player_Xs[0].finals_player_id        
        new_finals_match_player_result.finals_player_id=player_X_id        
    
@admin_manage_blueprint.route('/finals/division/<division_id>',methods=['POST'])
@login_required
@Scorekeeper_permission.require(403)
def route_create_finals(division_id):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    input_data = json.loads(request.data)    
    for finals_player in input_data:
        print finals_player
        new_finals_player = tables.FinalsPlayer(
            player_id=finals_player[0],
            initial_seed=finals_player[1]
        )
        db.session.add(new_finals_player)
        db.session.commit()
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
    for round in bracket_template_4_player_groups:
        new_round = tables.DivisionFinalRound()
        
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
            fill_in_player_match_results('player_one', match_template, new_finals_match_player_results[0])
            fill_in_player_match_results('player_two', match_template, new_finals_match_player_results[1])            
            fill_in_player_match_results('player_three', match_template, new_finals_match_player_results[2])
            fill_in_player_match_results('player_four', match_template, new_finals_match_player_results[3])            
            for finals_match_player_result in new_finals_match_player_results:
                db.session.add(finals_match_player_result)
                new_match.finals_match_player_results.append(finals_match_player_result)
                db.session.commit()
    
    return jsonify(new_final.to_dict_simple())        
        
