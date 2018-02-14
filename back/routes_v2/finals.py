from lib_v2 import blueprints,permissions
from ranking import Ranking
from flask import jsonify, request, abort, current_app
import json
import time
from routes_v2.results import test_tournament_results
from flask_restless.helpers import to_dict
from lib_v2.serializers import generic

bracket_template={}    
bracket_template[24]={
    'num_rounds':4,
    'num_matches_per_round':[4,4,2,1],
    'bye_rounds':[2],
    'bye_players_rank_per_match':{ 2 : [[1,8],[2,7],[3,6],[4,5]]},
    'number_bye_players':8
}

def reset_finals_players(tournament_id):
    for finals_player in current_app.table_proxy.get_all_finals_players(tournament_id):
        finals_player.finals_rank=finals_player.seed_rank
    
def set_tiebreaker_results_in_finals_players(tiebreaker,set_finals_rank=True):
    sorted_players = sorted(tiebreaker.players, key= lambda e: e.score,reverse=True)
    for player in sorted_players[0:tiebreaker.number_of_winners]:
        finals_player = current_app.table_proxy.get_finals_player(tiebreaker.tournament_id,finals_player_id=player.finals_player_id)
        #finals_player.finals_rank=tiebreaker.rank_of_winners
        player.winner=True
    for player in sorted_players[tiebreaker.number_of_winners:len(sorted_players)]:
        finals_player = current_app.table_proxy.get_finals_player(tiebreaker.tournament_id,finals_player_id=player.finals_player_id)
        if set_finals_rank:
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
    
    players_for_match.insert(0,players_with_ranks.pop(last_player_index))    
    players_for_match.insert(0,players_with_ranks.pop(middle_player_two_index))
    players_for_match.insert(0,players_with_ranks.pop(middle_player_index))
    players_for_match.insert(0,players_with_ranks.pop(0))
    return players_for_match    


@blueprints.test_blueprint.route('/<int:event_id>/brackets/<int:tournament_id>',methods=['POST'])
def generate_brackets(event_id, tournament_id):
    tournament = current_app.table_proxy.get_tournament_by_tournament_id(tournament_id)
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('No info in request')        
    finals_players = [finals_player_dict for finals_player_dict in input_data['data'] if finals_player_dict['present']==True]
    finals_players = finals_players[0:tournament.number_of_qualifiers]

    first_round_players=finals_players[bracket_template[24]['number_bye_players']:]
    
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
            finals_match.player_four_name=match_players[3]['player_name']            

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

#WARNING : DUPE CODE
def fill_matches_for_round(matches,ranked_players,num_matches):
    for finals_match in matches:
        match_players=get_players_for_match(ranked_players)
    
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
        finals_match.player_four_name=match_players[3]['player_name']            

    
rank_points_map={
    1:4,
    2:2,
    3:1,
    4:0
}

def calculate_points_for_machine(finals_match,game):        
    scores = []
    for player_string in ['player_four','player_three','player_two','player_one']:
        score_info = {'name':player_string}
        score = getattr(finals_match,player_string+"_score_"+str(game))
        if score and score != '':
            score_info['score']=int(score)
        else:
            score_info['score']=None
        scores.append(score_info)
    # if game == 1:
    #     scores = [
    #         {'score':int(finals_match.player_one_score_1),'name':'player_one'},
    #         {'score':int(finals_match.player_two_score_1),'name':'player_two'},
    #         {'score':int(finals_match.player_three_score_1),'name':'player_three'},
    #         {'score':int(finals_match.player_four_score_1),'name':'player_four'}        
    #     ]
    # if game == 2:
    #     scores = [
    #         {'score':int(finals_match.player_one_score_2),'name':'player_one'},
    #         {'score':int(finals_match.player_two_score_2),'name':'player_two'},
    #         {'score':int(finals_match.player_three_score_2),'name':'player_three'},
    #         {'score':int(finals_match.player_four_score_2),'name':'player_four'}        
    #     ]
    # if game == 3:
    #     scores = [
    #         {'score':int(finals_match.player_one_score_3),'name':'player_one'},
    #         {'score':int(finals_match.player_two_score_3),'name':'player_two'},
    #         {'score':int(finals_match.player_three_score_3),'name':'player_three'},
    #         {'score':int(finals_match.player_four_score_3),'name':'player_four'}        
    #     ]
    # if game == 4:
    #     scores =  [
    #         {'score':int(finals_match.player_one_score_4),'name':'player_one'},
    #         {'score':int(finals_match.player_two_score_4),'name':'player_two'},
    #         {'score':int(finals_match.player_three_score_4),'name':'player_three'},
    #         {'score':int(finals_match.player_four_score_4),'name':'player_four'}        
    #     ]
    sorted_players = sorted(scores, key= lambda e: e['score'],reverse=True)
    for index,player in enumerate(sorted_players):
        setattr(finals_match,player['name']+"_points_"+str(game),rank_points_map[index+1])
    
    
@blueprints.test_blueprint.route('/<int:event_id>/finals_match/<int:finals_match_id>',methods=['PUT'])
def edit_finals_match(event_id, finals_match_id):
    finals_match = current_app.table_proxy.get_finals_match(finals_match_id)                
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('No info in request')        
    current_app.table_proxy.edit_finals_match(finals_match,input_data)    
    if finals_match.player_one_score_1 is not None and finals_match.player_two_score_1 is not None and finals_match.player_three_score_1 is not None and finals_match.player_four_score_1 is not None:        
        finals_match.one_completed=True
        calculate_points_for_machine(finals_match,1)
    if finals_match.player_one_score_2 is not None and finals_match.player_two_score_2 is not None and finals_match.player_three_score_2 is not None and finals_match.player_four_score_2 is not None:
        finals_match.two_completed=True
        calculate_points_for_machine(finals_match,2)        
    if finals_match.player_one_score_3 is not None and finals_match.player_two_score_3 is not None and finals_match.player_three_score_3 is not None and finals_match.player_four_score_3 is not None:
        finals_match.three_completed=True
        calculate_points_for_machine(finals_match,3)

    player_one = {'name':'player_one', 'rank':None, 'points':get_player_total_points('player_one',finals_match),'finals_player_id':finals_match.player_one_finals_player_id}
    player_two = {'name':'player_two', 'rank':None, 'points':get_player_total_points('player_two',finals_match),'finals_player_id':finals_match.player_two_finals_player_id}
    player_three = {'name':'player_three', 'rank':None, 'points':get_player_total_points('player_three',finals_match),'finals_player_id':finals_match.player_three_finals_player_id}
    player_four = {'name':'player_four', 'rank':None, 'points':get_player_total_points('player_four',finals_match),'finals_player_id':finals_match.player_four_finals_player_id}
    
    if finals_match.one_completed is True and finals_match.two_completed is True and finals_match.three_completed is True:
        finals_match.player_one_winner=False
        finals_match.player_two_winner=False
        finals_match.player_three_winner=False
        finals_match.player_four_winner=False
        
        sorted_players = sorted([player_one,player_two,player_three,player_four], key= lambda e: e['points'], reverse=True)
        ranked_players = list(Ranking(sorted_players, key=lambda f:f['points']))
        for ranked_player in ranked_players:
            ranked_player[1]['rank']=ranked_player[0]+1
        ranked_players = [ranked_player[1] for ranked_player in ranked_players]    
    
        tournament = current_app.table_proxy.get_tournament_by_tournament_id(finals_match.tournament_id)
        
        tiebreaker,cutoff,tied_player_ids = get_tiebreaker(ranked_players,2,tournament,event_id,finals_match.round,finals_player_ids=True)        
        
        if tiebreaker:            
            finals_match.tiebreakers=tiebreaker
        if finals_match.one_completed and finals_match.two_completed and finals_match.three_completed:
            print "completed 1"
            if tiebreaker:
                print "found tiebreaker"
                if tiebreaker.completed:
                    finals_match.completed=True                    
                    finals_player_ids_in_tiebreaker = [player.finals_player_id for player in tiebreaker.players]
                    if ranked_players[0]['finals_player_id'] in finals_player_ids_in_tiebreaker:
                        if [player for player in tiebreaker.players if player.finals_player_id==ranked_players[0]['finals_player_id']][0].winner:
                            setattr(finals_match,ranked_players[0]['name']+"_winner",True)                            
                    else:
                        setattr(finals_match,ranked_players[0]['name']+"_winner",True)

                    if ranked_players[1]['finals_player_id'] in finals_player_ids_in_tiebreaker:
                        if [player for player in tiebreaker.players if player.finals_player_id==ranked_players[1]['finals_player_id']][0].winner:
                            setattr(finals_match,ranked_players[1]['name']+"_winner",True)                            
                    else:
                        setattr(finals_match,ranked_players[1]['name']+"_winner",True)

                    if ranked_players[2]['finals_player_id'] in finals_player_ids_in_tiebreaker:
                        if [player for player in tiebreaker.players if player.finals_player_id==ranked_players[2]['finals_player_id']][0].winner:
                            setattr(finals_match,ranked_players[2]['name']+"_winner",True)                            

                    if ranked_players[3]['finals_player_id'] in finals_player_ids_in_tiebreaker:
                        if [player for player in tiebreaker.players if player.finals_player_id==ranked_players[3]['finals_player_id']][0].winner:
                            setattr(finals_match,ranked_players[3]['name']+"_winner",True)                            
                            
                        
                    # is first player in match in list of tiebreakers
                    # if yes, check if they won - and assign winner in match player if they did
                    # if no, mark as winner
                    # repeat for second player
                    # is third player in match in list of tiebreakers
                    # if yes, check if they won - and assign winner in match player if they did
                    # is third player in match in list of tiebreakers
                    # if yes, check if they won - and assign winner in match player if they did

            else:
                finals_match.completed=True
                player_string=ranked_players[0]['name']
                print "setting %s to true" % player_string                
                setattr(finals_match,player_string+"_winner",True)
                player_string=ranked_players[1]['name']                
                print "setting %s to true" % player_string
                setattr(finals_match,player_string+"_winner",True)
                
    current_app.table_proxy.commit_changes()
    finals_match_dict=to_dict(finals_match)
    if finals_match.tiebreaker_id:
        finals_match_dict['tiebreaker']=generic.serialize_tiebreaker(finals_match.tiebreakers)
    return jsonify(finals_match_dict)    

def get_player_total_points(player_string,match):
    points=0
    for index,machine_num in enumerate([1,2,3]):
        points_for_game = getattr(match,player_string+"_points_"+str(machine_num))
        if points_for_game:
            points=points+points_for_game
    return points

@blueprints.test_blueprint.route('/<int:event_id>/tiebreaker/<int:tiebreaker_id>/match/<int:finals_match_id>',methods=['PUT'])
def edit_tiebreaker_and_match(event_id,tiebreaker_id,finals_match_id):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('No info in request')        
    edit_tiebreakers_route(event_id,tiebreaker_id,input_data['tiebreaker'],False)
    current_app.table_proxy.commit_changes()
    return edit_finals_match(event_id, finals_match_id)
    

def edit_tiebreakers_route(event_id,tiebreaker_id,input_data,set_finals_rank=True):
    tiebreaker = current_app.table_proxy.get_tiebreaker(tiebreaker_id)
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
        finals_match = current_app.table_proxy.get_finals_match_by_tiebreaker_id(tiebreaker.tiebreaker_id)
        if finals_match:
            finals_match.completed=True
        if set_finals_rank:
            reset_finals_players(tiebreaker.tournament_id)
        set_tiebreaker_results_in_finals_players(tiebreaker,set_finals_rank)
        tiebreakers = [completed_tiebreaker for completed_tiebreaker in current_app.table_proxy.get_all_tiebreakers(tiebreaker.tournament_id,tiebreaker.round) if completed_tiebreaker.completed is True]
        for other_tiebreaker in tiebreakers:
            set_tiebreaker_results_in_finals_players(other_tiebreaker,set_finals_rank)
    return tiebreaker
#    current_app.table_proxy.commit_changes()


@blueprints.test_blueprint.route('/<int:event_id>/final/<int:final_id>/<int:round>',methods=['PUT'])
def complete_round(event_id, final_id, round):
                
    final = current_app.table_proxy.get_final(final_id)
    loosers_finals_player_ids=[]
    lowest_rank_for_each_round={24:{1:17,2:9,3:5,4:1}}    
    tournament = current_app.table_proxy.get_tournament_by_tournament_id(final.tournament_id)
    finals_players = current_app.table_proxy.get_all_finals_players(final.tournament_id)    
    finals_player_dict = {finals_player.finals_player_id:finals_player for finals_player in finals_players}

    for match in [match for match in current_app.table_proxy.get_all_finals_matches(final_id) if match.round==round]:
        for player_string in ['player_four','player_three','player_two','player_one']:            
            winner = getattr(match,player_string+"_winner")
            if winner is not True:                
                loosers_finals_player_ids.append({'finals_player_id':getattr(match,player_string+"_finals_player_id"),
                                                  'points':get_player_total_points(player_string,match)})
    
    sorted_players = sorted(loosers_finals_player_ids, key= lambda e: e['points'], reverse=True)
    ranked_players = list(Ranking(sorted_players, key=lambda f:f['points']))
    for ranked_player in ranked_players:
        looser_rank = lowest_rank_for_each_round[tournament.number_of_qualifiers][round]+ranked_player[0]
        finals_player_dict[ranked_player[1]['finals_player_id']].finishing_rank=looser_rank
        print "player %s %s is NOT a winner" % (ranked_player[1]['finals_player_id'],looser_rank)
    if bracket_template[tournament.number_of_qualifiers]['num_rounds']!=round:
        next_round_matches = [match for match in current_app.table_proxy.get_all_finals_matches(final_id) if match.round==round+1]
        first_match_of_next_round = next_round_matches[0]
        if first_match_of_next_round.player_one_finals_player_id is not None and first_match_of_next_round.player_two_finals_player_id is not None and first_match_of_next_round.player_three_finals_player_id is not None and first_match_of_next_round.player_four_finals_player_id is not None:
            return jsonify({})
        for match in next_round_matches:
            match.player_one_finals_player_id=None
            match.player_one_name=None

            match.player_two_finals_player_id=None
            match.player_two_name=None

            match.player_three_finals_player_id=None
            match.player_three_name=None

            match.player_four_finals_player_id=None
            match.player_four_name=None
        winners_finals_player_ids=[]
        for match in [match for match in current_app.table_proxy.get_all_finals_matches(final_id) if match.round==round]:
            for player_string in ['player_four','player_three','player_two','player_one']:            
                winner = getattr(match,player_string+"_winner")
                if winner is True:
                    winners_finals_player_ids.append(to_dict(finals_player_dict[getattr(match,player_string+"_finals_player_id")]))

            pass
        next_round_matches = [match for match in current_app.table_proxy.get_all_finals_matches(final_id) if match.round==round+1]  
        for match in next_round_matches:
            for bye_string in ['bye_player_one','bye_player_two']:            
                bye = getattr(match,bye_string+"_finals_player_id")
                if bye:
                    winners_finals_player_ids.append(to_dict(finals_player_dict[getattr(match,bye_string+"_finals_player_id")]))
      
        sorted_players = sorted(winners_finals_player_ids, key= lambda e: e['finals_rank'])
        ranked_players = list(Ranking(sorted_players, key=lambda f:f['finals_rank'],reverse=True))
        ranked_players = [ranked_player[1] for ranked_player in ranked_players]
        number_of_matches = bracket_template[tournament.number_of_qualifiers]['num_matches_per_round'][round-1]
        fill_matches_for_round(next_round_matches,ranked_players,number_of_matches)    
    # clean up next round (if round 1 has no players) 
    # get winners from this round
    # organize into groups
    # populate next round
    #
    
    current_app.table_proxy.commit_changes()
    return jsonify({})

@blueprints.test_blueprint.route('/<int:event_id>/tiebreaker/<int:tiebreaker_id>',methods=['PUT'])
def edit_tiebreakers(event_id, tiebreaker_id):
    # tiebreaker = current_app.table_proxy.get_tiebreaker(tiebreaker_id)
    # if request.data:        
    #     input_data = json.loads(request.data)
    # else:
    #     raise BadRequest('No info in request')        
    # #if input_data['completed']==True:
    # #    tiebreaker.completed=True
    # score_count=0
    # for player in input_data['players']:
    #     tiebreaker_player = current_app.table_proxy.get_tiebreaker_player(player['tiebreaker_player_id'])
    #     tiebreaker_player.score=player['score']
    #     if player['score']:
    #         score_count=score_count+1
    # if score_count==len(tiebreaker.players):
    #     tiebreaker.completed=True
    #     finals_match = current_app.table_proxy.get_finals_match_by_tiebreaker_id(tiebreaker.tiebreaker_id)
    #     if finals_match:
    #         finals_match.completed=True
    #     reset_finals_players(tiebreaker.tournament_id)
    #     set_tiebreaker_results_in_finals_players(tiebreaker)
    #     tiebreakers = [completed_tiebreaker for completed_tiebreaker in current_app.table_proxy.get_all_tiebreakers(tiebreaker.tournament_id,tiebreaker.round) if completed_tiebreaker.completed is True]
    #     for other_tiebreaker in tiebreakers:
    #         set_tiebreaker_results_in_finals_players(other_tiebreaker)
        
    # current_app.table_proxy.commit_changes()
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('No info in request')        
    tiebreaker = edit_tiebreakers_route(event_id,tiebreaker_id,input_data['tiebreaker'])    
    current_app.table_proxy.commit_changes()
    return jsonify({'data':generic.serialize_tiebreaker(tiebreaker)})    

def get_tiebreaker(ranked_results,boundry_rank,tournament,event_id,round=0,player_ids=False,finals_player_ids=False):
    cutoff_index=len(ranked_results)
    rank_closest_to_cutoff=None
    rank_after_cutoff=None
    print ranked_results
    if ranked_results[len(ranked_results)-1]['rank']==boundry_rank and boundry_rank==2:
        rank_closest_to_cutoff=2
    for idx, result in enumerate(ranked_results):        
        rank = int(result['rank'])        
        if idx > 0 and rank > boundry_rank and ranked_results[idx-1]['rank'] <= boundry_rank :            
            cutoff_index=idx            
            rank_closest_to_cutoff=ranked_results[idx-1]['rank']
            rank_after_cutoff=ranked_results[idx]['rank']
    count_of_rank_closest_to_cutoff = len([rank for rank in ranked_results if rank['rank']==rank_closest_to_cutoff])            
    if (rank_closest_to_cutoff == boundry_rank and count_of_rank_closest_to_cutoff < 2) or rank_closest_to_cutoff is None:        
        print "no tiebreakers found... %s %s "%(rank_closest_to_cutoff, boundry_rank)
        return None,None,None
    #count_of_rank_closest_to_cutoff = len([rank for rank in ranked_results if rank['rank']==rank_closest_to_cutoff])
    if count_of_rank_closest_to_cutoff-1 + rank_closest_to_cutoff <= boundry_rank:
        print "no tiebreakers found...again %s %s %s "%(count_of_rank_closest_to_cutoff, rank_closest_to_cutoff, boundry_rank)        
        return None,None,None
    breach_difference = count_of_rank_closest_to_cutoff-1 + rank_closest_to_cutoff - boundry_rank
    num_players_that_advance = count_of_rank_closest_to_cutoff - breach_difference
    rank_of_tiebreaker_losers = rank_closest_to_cutoff+num_players_that_advance
    finals_players = current_app.table_proxy.get_all_finals_players(tournament.tournament_id)    
    finals_player_dict = {finals_player.player_id:finals_player.finals_player_id for finals_player in finals_players}
    if player_ids:
        tied_player_ids = [int(finals_player_dict[result['player_id']]) for result in ranked_results[cutoff_index-count_of_rank_closest_to_cutoff:cutoff_index]]        
    else:        
        tied_player_ids = [int(result['finals_player_id']) for result in ranked_results[cutoff_index-count_of_rank_closest_to_cutoff:cutoff_index]]

    matched_tiebreaker = None
    for tiebreaker in current_app.table_proxy.get_all_tiebreakers(tournament.tournament_id,round):
        tied_players_to_check = list(tied_player_ids)
        for tied_player_id_from_tiebreaker in [player.finals_player_id for player in tiebreaker.players]:
            if tied_player_id_from_tiebreaker in tied_players_to_check:
                tied_players_to_check.remove(tied_player_id_from_tiebreaker)
        if len(tied_players_to_check)==0:
            matched_tiebreaker = tiebreaker
    if matched_tiebreaker:
        return matched_tiebreaker,cutoff_index, tied_player_ids
    print "DEBUG : event id - %s" % event_id
    print "DEBUG : tied_player_ids - %s" % tied_player_ids
    print "DEBUG : tournament id - %s" % tournament.tournament_id
    
    new_tiebreaker = current_app.table_proxy.create_tiebreaker(event_id,
                                                               tied_player_ids,
                                                               tournament.tournament_id,
                                                               rank_closest_to_cutoff,
                                                               rank_of_tiebreaker_losers,
                                                               num_players_that_advance,
                                                               round)
    return new_tiebreaker,cutoff_index,tied_player_ids
    

@blueprints.test_blueprint.route('/<int:event_id>/final/<int:final_id>',methods=['GET'])
def get_final(event_id, final_id):
    finals_matches = current_app.table_proxy.get_all_finals_matches(final_id)
    final_matches_dict={}
    for final_match in finals_matches:
        round = final_match.round
        if final_matches_dict.get(round,None) is None:
            final_matches_dict[round]=[]
        final_match_dict = to_dict(final_match)
        if final_match.tiebreaker_id:
            final_match_dict['tiebreaker']=generic.serialize_tiebreaker(final_match.tiebreakers)
        final_matches_dict[round].append(final_match_dict)
    final_info=[]
    final = current_app.table_proxy.get_final(final_id)
    finals_players = current_app.table_proxy.get_all_finals_players(final.tournament_id)    
    finals_player_dict = {finals_player.finals_player_id:to_dict(finals_player) for finals_player in finals_players}
    
    return jsonify({'data':final_matches_dict,'finals_players':finals_player_dict,'final_name':final.name})
    
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
    finals_players = current_app.table_proxy.get_all_finals_players(tournament_id)
    #finals_player_dict = {finals_player.finals_player_id:finals_player.player_id for finals_player in finals_players}
    tiebreakers = []
    for important_boundry in important_tiebreaker_boundry_ranks[32]:
        returned_tiebreaker,cutoff_index,tied_player_ids = get_tiebreaker(ranked_results,important_boundry,tournament,event_id,player_ids=True)
        tiebreakers.append(returned_tiebreaker)
    current_app.table_proxy.commit_changes()
    final = current_app.table_proxy.get_final_by_tournament_id(tournament_id,finals_name)
    if(final):
        final_dict = to_dict(final)
    else:
        final_dict = None
    return jsonify({'data':[generic.serialize_tiebreaker(tiebreaker) for tiebreaker in tiebreakers if tiebreaker is not None],
                    'finals_players':[to_dict(finals_player) for finals_player in finals_players],
                    'tournament_qualifiers':tournament.number_of_qualifiers,
                    'final':final_dict})



