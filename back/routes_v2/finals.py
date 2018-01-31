from lib_v2 import blueprints,permissions
from ranking import Ranking
from flask import jsonify, request, abort, current_app
import json
import time
from routes_v2.results import test_tournament_results
from flask_restless.helpers import to_dict
from lib_v2.serializers import generic

def reset_finals_players(tournament_id):
    for finals_player in current_app.table_proxy.get_all_finals_players(tournament_id):
        finals_player.finals_rank=finals_player.seed_rank
    
def set_tiebreaker_results_in_finals_players(tiebreaker):
    sorted_players = sorted(tiebreaker.players, key= lambda e: e.score,reverse=True)
    for player in sorted_players[0:tiebreaker.number_of_winners]:
        finals_player = current_app.table_proxy.get_finals_player(player.player_id,tiebreaker.tournament_id)
        finals_player.finals_rank=tiebreaker.rank_of_winners
    for player in sorted_players[tiebreaker.number_of_winners:len(sorted_players)]:
        finals_player = current_app.table_proxy.get_finals_player(player.player_id,tiebreaker.tournament_id)
        finals_player.finals_rank=tiebreaker.rank_of_losers          
    

@blueprints.test_blueprint.route('/<int:event_id>/match/<int:finals_match_id>',methods=['PUT'])
def record_finals_match_score_order_change(event_id, finals_match_id):
    # set order for each player
    ## if game one, order selection based on rank
    ## if not game one, order selection based on sorted list based on points from last game
    # record score for each player
    # if all scores are done
    #   if tiebreaker not needed, mark as completed, fill in winners 
    #   if tiebreaker needed, create tiebreaker and fill in
    #
    #
    
    pass

def get_players_for_match(players_with_ranks):
    players_for_match=[]
    last_player_index=len(players_with_ranks)-1
    middle_player_index=last_player_index/2
    middle_player_two_index=middle_player_index+1
    print "%s %s %s" % (last_player_index,middle_player_index,middle_player_two_index)
    players_for_match.insert(0,players_with_ranks.pop(last_player_index))    
    players_for_match.insert(0,players_with_ranks.pop(middle_player_two_index))
    players_for_match.insert(0,players_with_ranks.pop(middle_player_index))
    players_for_match.insert(0,players_with_ranks.pop(0))
    return players_for_match    

@blueprints.test_blueprint.route('/<int:event_id>/brackets/<int:tournament_id>',methods=['POST'])
def generate_brackets(event_id, tournament_id):
    tournament = current_app.table_proxy.get_tournament_by_tournament_id(tournament_id)
    bracket_template={}    
    bracket_template[24]={
        'num_rounds':4,
        'num_matches_per_round':[4,4,2,1],
        'bye_rounds':[2],
        'bye_players_rank_per_match':{ 2 : [[1,8],[2,7],[3,6],[4,5]]},
        'number_bye_players':8
    }
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('No info in request')        
    finals_players = [finals_player_dict for finals_player_dict in input_data['data'] if finals_player_dict['present']==True]
    finals_players = finals_players[0:tournament.number_of_qualifiers]

    first_round_players=finals_players[bracket_template[24]['number_bye_players']:]
    print len(first_round_players)
    bye_players=finals_players[0:bracket_template[24]['number_bye_players']]    
    
    num_rounds=bracket_template[24]['num_rounds']
    num_matches_per_round=bracket_template[24]['num_matches_per_round']
    final = current_app.table_proxy.create_finals(tournament_id,input_data['description'])
    
    for round_index in range(0,num_rounds):
        
        for match_num in range(0,num_matches_per_round[round_index]):
            #get_players_for_match(players_with_ranks)
            finals_match=current_app.table_proxy.create_finals_match(tournament_id,final,round_index+1)
            if(round_index+1 not in bracket_template[24]['bye_rounds'] and round_index+1!=1):
                continue
            if(round_index+1 in bracket_template[24]['bye_rounds']):
                bye_template = bracket_template[24]['bye_players_rank_per_match'][round_index+1]
                bye_player_ranks = bye_template.pop()
                bye_player = bye_players[bye_player_ranks[0]-1]
                finals_match.bye_player_one_finals_player_id=bye_player['finals_player_id']
                finals_match.bye_player_one_name=bye_player['player_name']
                print "lenfth of bye players is %s, %s " % (len(bye_players),bye_player_ranks)

                bye_player = bye_players[bye_player_ranks[1]-1]                
                finals_match.bye_player_two_finals_player_id=bye_player['finals_player_id']
                finals_match.bye_player_two_name=bye_player['player_name']
                continue
            
            match_players=get_players_for_match(first_round_players)
            finals_match.player_one_rank=match_players[0]['seed_rank']
            finals_match.player_one_finals_player_id=match_players[0]['finals_player_id']
            finals_match.player_one_name=match_players[0]['player_name']
            
            finals_match.player_two_rank=match_players[1]['seed_rank']
            finals_match.player_two_finals_player_id=match_players[1]['finals_player_id']
            finals_match.player_two_name=match_players[1]['player_name']
            
            finals_match.player_three_rank=match_players[2]['seed_rank']
            finals_match.player_three_finals_player_id=match_players[2]['finals_player_id']
            finals_match.player_three_name=match_players[2]['player_name']            

            finals_match.player_four_rank=match_players[3]['seed_rank']
            finals_match.player_four_finals_player_id=match_players[3]['finals_player_id']
            finals_match.player_four_name=match_players[3]['finals_player_id']            

            pass
    
    current_app.table_proxy.commit_changes()
    return jsonify({'data':to_dict(final)})
    # 
    # get ordered list of finals players
    # shuffle tied players
    # create matches per round
    # fill in byes
    # fill in players
    # 
    
    pass

@blueprints.test_blueprint.route('/<int:event_id>/tiebreaker/<int:tiebreaker_id>',methods=['PUT'])
def edit_tiebreakers(event_id, tiebreaker_id):
    tiebreaker = current_app.table_proxy.get_tiebreaker(tiebreaker_id)
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('No info in request')        
    #if input_data['completed']==True:
    #    tiebreaker.completed=True
    score_count=0
    for player in input_data['players']:
        tiebreaker_player = current_app.table_proxy.get_tiebreaker_player(player['tiebreaker_player_id'])
        tiebreaker_player.score=player['score']
        if player['score']:
            score_count=score_count+1
    if score_count==len(tiebreaker.players):
        tiebreaker.completed=True
        reset_finals_players(tiebreaker.tournament_id)
        set_tiebreaker_results_in_finals_players(tiebreaker)
        tiebreakers = [completed_tiebreaker for completed_tiebreaker in current_app.table_proxy.get_all_tiebreakers(tiebreaker.tournament_id,tiebreaker.round) if completed_tiebreaker.completed is True]
        for other_tiebreaker in tiebreakers:
            set_tiebreaker_results_in_finals_players(other_tiebreaker)
        
    current_app.table_proxy.commit_changes()
    return jsonify({'data':generic.serialize_tiebreaker(tiebreaker)})    

def get_tiebreaker(ranked_results,boundry_rank,tournament,event_id):
    cutoff_index=len(ranked_results)
    rank_closest_to_cutoff=None
    rank_after_cutoff=None
    for idx, result in enumerate(ranked_results):        
        rank = int(result['rank'])        
        if idx > 0 and rank > boundry_rank and ranked_results[idx-1]['rank'] <= boundry_rank :            
            cutoff_index=idx
            rank_closest_to_cutoff=ranked_results[idx-1]['rank']
            rank_after_cutoff=ranked_results[idx]['rank']
    if rank_closest_to_cutoff == boundry_rank or rank_closest_to_cutoff is None:
        return None
    count_of_rank_closest_to_cutoff = len([rank for rank in ranked_results if rank['rank']==rank_closest_to_cutoff])
    if count_of_rank_closest_to_cutoff-1 + rank_closest_to_cutoff <= boundry_rank:
        return None
    breach_difference = count_of_rank_closest_to_cutoff-1 + rank_closest_to_cutoff - boundry_rank
    num_players_that_advance = count_of_rank_closest_to_cutoff - breach_difference
    rank_of_tiebreaker_losers = rank_closest_to_cutoff+num_players_that_advance
    tied_player_ids = [int(result['player_id']) for result in ranked_results[cutoff_index-count_of_rank_closest_to_cutoff:cutoff_index]]

    matched_tiebreaker = None
    for tiebreaker in current_app.table_proxy.get_all_tiebreakers(tournament.tournament_id,0):
        tied_players_to_check = list(tied_player_ids)
        for tied_player_id_from_tiebreaker in [player.player_id for player in tiebreaker.players]:
            if tied_player_id_from_tiebreaker in tied_players_to_check:
                tied_players_to_check.remove(tied_player_id_from_tiebreaker)
        if len(tied_players_to_check)==0:
            matched_tiebreaker = tiebreaker
    if matched_tiebreaker:
        return matched_tiebreaker
    new_tiebreaker = current_app.table_proxy.create_tiebreaker(event_id,
                                                               tied_player_ids,
                                                               tournament.tournament_id,
                                                               rank_closest_to_cutoff,
                                                               rank_of_tiebreaker_losers,
                                                               num_players_that_advance,
                                                               0)
    return new_tiebreaker
    

@blueprints.test_blueprint.route('/<int:event_id>/final/<int:final_id>',methods=['GET'])
def get_final(event_id, final_id):
    finals_matches = current_app.table_proxy.get_all_finals_matches(final_id)
    final_matches_dict={}
    for final_match in finals_matches:
        round = final_match.round
        if final_matches_dict.get(round,None) is None:
            final_matches_dict[round]=[]
        final_matches_dict[round].append(to_dict(final_match))
    final_info=[]
    
    return jsonify({'data':final_matches_dict})
    
@blueprints.test_blueprint.route('/<int:event_id>/tiebreakers/<int:tournament_id>/<finals_name>',methods=['GET'])
def get_tiebreakers(event_id, tournament_id,finals_name):
    tournament = current_app.table_proxy.get_tournament_by_tournament_id(tournament_id)
    important_tiebreaker_boundry_ranks={}
    important_tiebreaker_boundry_ranks[32]=[8,32]    
    
    num_qualifiers = tournament.number_of_qualifiers        
    raw_ranked_results=test_tournament_results(event_id,tournament_id)
    ranked_results = json.loads(raw_ranked_results.data)
    ranked_results = [rank for rank in ranked_results['data'] if rank['seperator']==False]
    for ranked_result in ranked_results:
        current_app.table_proxy.create_finals_player(event_id,ranked_result['player_id'],tournament_id,ranked_result['rank'])
    tiebreakers = []
    for important_boundry in important_tiebreaker_boundry_ranks[32]:
        returned_tiebreaker = get_tiebreaker(ranked_results,important_boundry,tournament,event_id)
        tiebreakers.append(returned_tiebreaker)
    current_app.table_proxy.commit_changes()
    finals_players = current_app.table_proxy.get_all_finals_players(tournament_id)
    final = current_app.table_proxy.get_final_by_tournament_id(tournament_id,finals_name)
    if(final):
        final_dict = to_dict(final)
    else:
        final_dict = None
    return jsonify({'data':[generic.serialize_tiebreaker(tiebreaker) for tiebreaker in tiebreakers if tiebreaker is not None],
                    'finals_players':[to_dict(finals_player) for finals_player in finals_players],
                    'tournament_qualifiers':tournament.number_of_qualifiers,
                    'final':final_dict})



