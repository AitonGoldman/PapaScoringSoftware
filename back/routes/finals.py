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

bracket_template_4_player_groups_24_players = [
    {
        'round':1,
        'matches':[
            generate_rank_matchup_dict([8,15,16,23]),
            generate_rank_matchup_dict([9,14,17,22]),
            generate_rank_matchup_dict([10,13,18,21]),
            generate_rank_matchup_dict([11,12,19,20])            
        ]
    },
    {
        'round':2,
        'matches':[
            generate_rank_matchup_dict([0,7, None, None]),
            generate_rank_matchup_dict([1,6, None, None]),
            generate_rank_matchup_dict([2,5, None, None]),
            generate_rank_matchup_dict([3,4, None, None])                            
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
            generate_rank_matchup_dict([0,7,8,15]),
            generate_rank_matchup_dict([1,6,9,14]),
            generate_rank_matchup_dict([2,5,10,13]),
            generate_rank_matchup_dict([3,4,11,12])            
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
            generate_rank_matchup_dict([0,7,3,4]),                                
            generate_rank_matchup_dict([1,6,2,5])            
        ]
    },
    {
        'round':2,
        'matches':[
            generate_rank_matchup_dict([None,None, None, None]),                
        ]
    }
]    


@admin_manage_blueprint.route('/finals/scorekeeping/division_final_match_result/<division_final_match_result_id>/tiebreaker',
                              methods=['PUT'])
def route_scorekeeping_resolve_tiebreaker(division_final_match_result_id):
    match_result = json.loads(request.data)
    tiebreaker_winners = resolve_tiebreakers(match_result,current_app)
    return jsonify({'data':tiebreaker_winners})

@admin_manage_blueprint.route('/finals/scorekeeping/division_final_match_game_result/<division_final_match_game_result_id>',
                              methods=['PUT'])
def route_record_game(division_final_match_game_result_id):
    game_result = json.loads(request.data)
    for player_result in game_result['division_final_match_game_player_results']:
        if player_result['score'] is not None:
            player_result['score']=str(player_result['score']).replace(',','')
    game_result_from_db = fetch_entity(current_app.tables.DivisionFinalMatchGameResult,division_final_match_game_result_id)
    match_from_db = fetch_entity(current_app.tables.DivisionFinalMatch,game_result_from_db.division_final_match_id)
    round_from_db = fetch_entity(current_app.tables.DivisionFinalRound,match_from_db.division_final_round_id)
    division_final_from_db = fetch_entity(current_app.tables.DivisionFinal,round_from_db.division_final_id)

    match_dict = match_from_db.to_dict_simple()
    calculate_points_for_match(match_dict)    
    pre_record_tiebreakers = calculate_tiebreakers(match_dict,report_only=True,ignore_won_tiebreaker=True)
    record_scores(game_result,game_result_from_db,current_app)    
    match_dict = match_from_db.to_dict_simple()
    calculate_points_for_match(match_dict)    
    post_record_tiebreakers = calculate_tiebreakers(match_dict,report_only=True,ignore_won_tiebreaker=True)        
    
    if len(pre_record_tiebreakers)==0 or len(set(pre_record_tiebreakers) & set(post_record_tiebreakers)) == len(pre_record_tiebreakers):
        return jsonify({'data':division_final_from_db.to_dict_simple()})    
    
    reset_tiebreaker_info_on_score_change(match_from_db,current_app) 

    return jsonify({'data':None})

@admin_manage_blueprint.route('/finals/scorekeeping/division_final_round/<division_final_round_id>/complete',
                              methods=['PUT'])
def route_complete_division_final_round(division_final_round_id):    
    division_final_round = fetch_entity(current_app.tables.DivisionFinalRound,division_final_round_id)
    division_final = fetch_entity(current_app.tables.DivisionFinal,division_final_round.division_final_id)    
    winners = complete_round(division_final,division_final_round,current_app)
    
    return jsonify({'data': None})


@admin_manage_blueprint.route('/finals/division_final',
                              methods=['GET'])
def route_get_division_finals():
    division_finals = current_app.tables.DivisionFinal.query.all()
    if len(division_finals) > 0:
        finals_info = {division_final.division_final_id:division_final.division.get_tournament_name(division_final.division.tournament) for division_final in division_finals}
    else:
        finals_info = {}
    return jsonify({'data': finals_info})

@admin_manage_blueprint.route('/finals/scorekeeping/division_final/<division_final_id>',
                              methods=['GET'])
def route_scorekeeping_get_division_final(division_final_id):
    division_final = current_app.tables.DivisionFinal.query.filter_by(division_final_id=division_final_id).first()
    division_final_dict = division_final.to_dict_simple()        
    round_progress = "In Progress"
    matches_completed = 0
    for division_final_round in division_final_dict['division_final_rounds']:        
        matches_completed=0
        for division_final_match in division_final_round['division_final_matches']:            
            calculate_points_for_match(division_final_match)
            tiebreaker_list = calculate_tiebreakers(division_final_match,report_only=True)
            if division_final_match['completed'] is True:
                matches_completed=matches_completed+1
            if len([match_player for match_player in division_final_match['final_match_player_results'] if match_player['final_player_id'] is not None])<4:
                round_progress="Waiting to Start"                
            if len(tiebreaker_list) > 0:                                
                round_progress="Resolve Tiebreakers"                
        division_final_round['round_progress']=round_progress
        if matches_completed==len(division_final_round['division_final_matches']):
            division_final_round['round_progress']="Ready to be completed"
            division_final_round['ready_to_be_completed']=True
        if division_final_round['completed'] is True:
            division_final_round['round_progress']='Round Completed!'
    calculate_final_rankings(division_final_dict['division_final_rounds'])
    #return jsonify({'data':None})
    return jsonify({'data': division_final_dict})



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
            if round_info['round']==1:
                for index_2,division_final_match_game_result in enumerate(division_final_match.final_match_game_results):
                    game_player_result = division_final_match_game_result.division_final_match_game_player_results
                    if p1_seed is not None:
                        game_player_result[0].final_player_id = division_final_player_dict[p1_seed].final_player_id                     
                    if p2_seed:
                        game_player_result[1].final_player_id = division_final_player_dict[p2_seed].final_player_id                                         
                    if p3_seed:
                        game_player_result[2].final_player_id = division_final_player_dict[p3_seed].final_player_id                                         
                    if p4_seed:                    
                        game_player_result[3].final_player_id = division_final_player_dict[p4_seed].final_player_id                                         
            match_player_results = division_final_match.final_match_player_results
            if p1_seed is not None:                
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
    for tiebreaker_score in tiebreaker_scores:
        tiebreaker_score['player_score']=int(tiebreaker_score['player_score'].replace(',',''))
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
    sorted_scores[3]['papa_points']=4    
    
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
        sorted_match_player_results=sorted(division_final_match['final_match_player_results'], key= lambda e: e['papa_points_sum'])

        sorted_match_player_results[0]['winner']=False
        if sorted_match_player_results[0]['won_tiebreaker'] is True:
            sorted_match_player_results[0]['winner']=True            

        sorted_match_player_results[1]['winner']=False
        if sorted_match_player_results[1]['won_tiebreaker'] is True:            
            sorted_match_player_results[1]['winner']=True                    

        sorted_match_player_results[2]['winner']=True
        if sorted_match_player_results[2]['won_tiebreaker'] is False:            
            sorted_match_player_results[2]['winner']=False                    

        sorted_match_player_results[3]['winner']=True
        if sorted_match_player_results[3]['won_tiebreaker'] is False:
            
            sorted_match_player_results[3]['winner']=False                    
        
def calculate_tiebreakers(division_final_match_dict,report_only=False, ignore_won_tiebreaker=False):
    sorted_scores = sorted(division_final_match_dict['final_match_player_results'], key= lambda e: e['papa_points_sum'],reverse=True)
    completed_tiebreakers = len([division_final_match_player for division_final_match_player in division_final_match_dict["final_match_player_results"] if division_final_match_player['won_tiebreaker']!=None]) > 0
    if ignore_won_tiebreaker:
        completed_tiebreakers = False
    tiebreaker_final_player_ids=[]

    if completed_tiebreakers is True:
        return tiebreaker_final_player_ids    
    if sorted_scores[1]['papa_points_sum'] == sorted_scores[2]['papa_points_sum']:
        if sorted_scores[1]['papa_points_sum'] is not None:
            tiebreaker_final_player_ids.append(sorted_scores[1]['final_player_id'])
            tiebreaker_final_player_ids.append(sorted_scores[2]['final_player_id'])
            if report_only is False:
                division_final_match_dict['expected_num_tiebreaker_winners']=1
    if sorted_scores[1]['papa_points_sum'] == sorted_scores[2]['papa_points_sum'] and sorted_scores[1]['papa_points_sum'] == sorted_scores[0]['papa_points_sum']:
        if sorted_scores[1]['papa_points_sum'] is not None:
            tiebreaker_final_player_ids.append(sorted_scores[0]['final_player_id'])
            if report_only is False:
                division_final_match_dict['expected_num_tiebreaker_winners']=2        
    if sorted_scores[1]['papa_points_sum'] == sorted_scores[2]['papa_points_sum'] and sorted_scores[1]['papa_points_sum'] == sorted_scores[3]['papa_points_sum']:
        if sorted_scores[1]['papa_points_sum'] is not None:
            tiebreaker_final_player_ids.append(sorted_scores[3]['final_player_id'])
            if report_only is False:
                division_final_match_dict['expected_num_tiebreaker_winners']=1


    for match_player_result in division_final_match_dict['final_match_player_results']:
        if match_player_result['final_player_id'] in tiebreaker_final_player_ids and report_only is False:            
            match_player_result['needs_tiebreaker']=True
    return tiebreaker_final_player_ids

def resolve_tiebreakers(division_final_match_dict,app):    
    for match_player_result in division_final_match_dict['final_match_player_results']:
        if match_player_result['needs_tiebreaker'] is True:
            match_player_result['tiebreaker_score']=int(match_player_result['tiebreaker_score'].replace(',',''))
    sorted_scores = sorted([match_player_result for match_player_result in division_final_match_dict['final_match_player_results'] if match_player_result['needs_tiebreaker'] is True], key= lambda e: e['tiebreaker_score'])    
    final_match_game_result = app.tables.DivisionFinalMatch.query.filter_by(division_final_match_id=division_final_match_dict['division_final_match_id']).first()
    final_match_game_result.completed=True
    final_match_player_results = {match_player_result.final_player_id:match_player_result for match_player_result in  app.tables.DivisionFinalMatchPlayerResult.query.filter_by(division_final_match_id=division_final_match_dict['division_final_match_id']).all()}
    tiebreaker_winners=[]
    if len(sorted_scores)==2:
        final_match_player_results[sorted_scores[1]['final_player_id']].won_tiebreaker=True
        final_match_player_results[sorted_scores[0]['final_player_id']].won_tiebreaker=False
        tiebreaker_winners.append({"final_player_id":sorted_scores[1]['final_player_id'],"final_player_name":sorted_scores[1]['final_player']['player_name']})
    if len(sorted_scores)==3:
        if division_final_match_dict['expected_num_tiebreaker_winners']==2:
            final_match_player_results[sorted_scores[0]['final_player_id']].won_tiebreaker=False
            final_match_player_results[sorted_scores[1]['final_player_id']].won_tiebreaker=True
            final_match_player_results[sorted_scores[2]['final_player_id']].won_tiebreaker=True
            tiebreaker_winners.append({"final_player_id":sorted_scores[1]['final_player_id'],"final_player_name":sorted_scores[1]['final_player']['player_name']})
            tiebreaker_winners.append({"final_player_id":sorted_scores[2]['final_player_id'],"final_player_name":sorted_scores[2]['final_player']['player_name']})
        if division_final_match_dict['expected_num_tiebreaker_winners']==1:
            final_match_player_results[sorted_scores[0]['final_player_id']].won_tiebreaker=False
            final_match_player_results[sorted_scores[1]['final_player_id']].won_tiebreaker=False
            final_match_player_results[sorted_scores[2]['final_player_id']].won_tiebreaker=True
            tiebreaker_winners.append({"final_player_id":sorted_scores[2]['final_player_id'],"final_player_name":sorted_scores[2]['final_player']['player_name']})                        
    app.tables.db_handle.session.commit()
    return tiebreaker_winners

def record_scores(match_game_result_dict,match_game_result_from_db,app):
    match_game_player_results_scores = {}
    for match_game_player_result in match_game_result_dict['division_final_match_game_player_results']:
        match_game_player_result_id = match_game_player_result['division_final_match_game_player_result_id']        
        match_game_player_results_scores[match_game_player_result_id] = match_game_player_result
        
    if match_game_result_dict['division_machine_string']:
        match_game_result_from_db.division_machine_string=match_game_result_dict['division_machine_string']

    for match_game_player_result in match_game_result_from_db.division_final_match_game_player_results:        
        game_player_result_id = match_game_player_result.division_final_match_game_player_result_id        
        if  match_game_player_results_scores[game_player_result_id]['score'] is not None:
            match_game_player_result.score=match_game_player_results_scores[game_player_result_id]['score']
        if  match_game_player_results_scores[game_player_result_id]['play_order'] is not None:
            match_game_player_result.play_order=match_game_player_results_scores[game_player_result_id]['play_order']            
    app.tables.db_handle.session.commit()
    
def reset_tiebreaker_info_on_score_change(match,app):
    for match_player_result in match.final_match_player_results:
        match_player_result.needs_tiebreaker=False
        match_player_result.won_tiebreaker=None
    match.expected_num_tiebreaker_winners=None
    app.tables.db_handle.session.commit()

def generate_match_players_groupings(match_player_results):    
    index_last=len(match_player_results)-1
    index_middle_1=(len(match_player_results)-1)/2
    index_middle_2=index_middle_1+1
    return [match_player_results.pop(),match_player_results.pop(index_middle_2),match_player_results.pop(index_middle_1),match_player_results.pop(0)]
    

def complete_round(division_final, division_final_round,app):
    division_final_round_id=division_final_round.division_final_round_id
    division_final_round_dict = division_final_round.to_dict_simple()                    
    next_division_final_round = app.tables.DivisionFinalRound.query.filter_by(division_final_round_id=division_final_round_id+1).first()
    division_final_match_winners=[]
    
    for division_final_match in division_final_round_dict['division_final_matches']:            
        calculate_points_for_match(division_final_match)    
    
    for division_final_match in division_final_round_dict['division_final_matches']:            
        for division_final_match_player in division_final_match['final_match_player_results']:                
            if division_final_match_player['winner']:
                division_final_match_winners.append(division_final_match_player)
    if next_division_final_round and division_final_round.round_number == "1":
        for division_final_match in next_division_final_round.division_final_matches:
            for division_final_match_player in division_final_match.final_match_player_results:                
                if division_final_match_player.final_player_id:                    
                    division_final_match_winners.append(division_final_match_player.to_dict_simple())
                    
    sorted_winners = sorted(division_final_match_winners, key= lambda e: e['final_player']['adjusted_seed'])
    
    if next_division_final_round is None:
        return sorted_winners    
    winner_groups = []
    while len(sorted_winners) > 0:
        group = generate_match_players_groupings(sorted_winners)
        winner_groups.append(group)
    next_round_matches = app.tables.DivisionFinalMatch.query.filter_by(division_final_round_id=division_final_round_id+1).all()
    for index,match in enumerate(next_round_matches):
        for player_index,match_player_result in enumerate(winner_groups[index]):
            match.final_match_player_results[player_index].final_player_id=match_player_result['final_player_id']
            for game_index,match_game in enumerate(match.final_match_game_results):
                match_game.division_final_match_game_player_results[player_index].final_player_id=match_player_result['final_player_id']
    division_final_round.completed=True
    app.tables.db_handle.session.commit()
    return division_final_match_winners
    
def calculate_final_rankings(round_dicts):
    number_matches = 0
    previous_number_matches = 0
    for round in round_dicts:
        number_matches = number_matches + len(round['division_final_matches'])
    for round in round_dicts:
        if round['completed'] is not True:
            continue
        unranked_match_players = []
        matches_in_current_round = len(round['division_final_matches'])
        for match in round['division_final_matches']:
            for match_player in match['final_match_player_results']:
                unranked_match_players.append(match_player)
        sorted_player_list = sorted(unranked_match_players, key= lambda e: e['papa_points_sum'],reverse=True)
        ranked_player_list = list(Ranking(sorted_player_list,key=lambda pp: pp['papa_points_sum']))                
        ranked_player_dict = {ranked_player[1]['final_player_id']:ranked_player for ranked_player in ranked_player_list}
        base_rank = (number_matches*4) - previous_number_matches
        for ranked_final_player_id,ranked_final_player in ranked_player_dict.iteritems():
            if ranked_final_player[1]['winner'] is not True:
                ranked_final_player[1]['final_rank']=base_rank-(matches_in_current_round*4)-ranked_final_player[0]+1
        previous_number_matches=previous_number_matches + len(round['division_final_matches'])*4
        
    pass
    
