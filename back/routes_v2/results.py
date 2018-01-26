from lib_v2 import blueprints,permissions
from ranking import Ranking
from sqlalchemy.sql import functions
#from sqlalchemy import within_group
from sqlalchemy.orm import join
from sqlalchemy.sql.expression import desc, asc
from flask import jsonify, request, abort, current_app
#from util import db_util
from sqlalchemy import null, func, text, and_
from sqlalchemy.sql import select
import json
import time
from flask_restless.helpers import to_dict
from routes_v2.player import get_event_player_route
def get_rank_from_papa_points(points):
    if points == 100:
        return 1
    if points == 90:
        return 2
    if points == 85:
        return 3
    if points < 85:
        return 84-points+3
    pass
def get_papa_points_from_rank(rank):
    if rank == 1:
        return 100
    if rank == 2:
        return 90
    if rank == 3:
        return 85
    if rank >= 88:
        return 0
    return 100-rank-12

current_milli_time = lambda: int(round(time.time() * 1000))

#select sum(machine_rank), player_id, tournament_id from (
#  select machine_rank,tournament_machine_id,player_id,tournament_id,row_number() over (partition by player_id,tournament_id order by tournament_id,machine_rank desc) as row from (
#    select tournament_id,player_id,score,tournament_machine_id,papa_scoring_func(rank() over (partition by tournament_machine_id order by score desc)) as machine_rank from (
#      select score,player_id,tournament_machine_id,tournament_id from (
#        select score_id,score,player_id,tournament_machine_id,tournament_id,row_number() over (partition by player_id, tournament_machine_id, tournament_id order by score desc) as p from scores)
#      as sub where p=1)
#    as sub_two)
#  as sub_three order by player_id)
#as sub_four where row < 7 group by player_id,tournament_id            


def getTournamentResultsQuery(tournament_id,signifigant_scores):
    query = "select sum(machine_rank), player_id, tournament_id from (select machine_rank,tournament_machine_id,player_id,tournament_id,row_number() over (partition by player_id,tournament_id order by tournament_id,machine_rank desc) as row from (select tournament_id,player_id,score,tournament_machine_id,papa_scoring_func(rank() over (partition by tournament_machine_id order by score desc)) as machine_rank from (select score,player_id,tournament_machine_id,tournament_id from (select score_id,score,player_id,tournament_machine_id,tournament_id,row_number() over (partition by player_id, tournament_machine_id, tournament_id order by score desc) as p from scores where tournament_id=%s) as sub where p=1) as sub_two) as sub_three order by player_id) as sub_four where row <= %s group by player_id,tournament_id" % (tournament_id, signifigant_scores)   
    return query

def getTournamentMachineResultsQuery(tournament_id=None, tournament_machine_id=None):
    where_string = "where tournament_id= %s " % tournament_id
    if tournament_machine_id:
        where_string = where_string + " and tournament_machine_id = %s"  % tournament_machine_id
    tournament_machines_query = "select machine_rank,tournament_machine_id,player_id,tournament_id,score, row_number() over (partition by player_id,tournament_id order by tournament_id,machine_rank desc) as row from (select tournament_id,player_id,score,tournament_machine_id,papa_scoring_func(rank() over (partition by tournament_machine_id order by score desc)) as machine_rank from (select score,player_id,tournament_machine_id,tournament_id from (select score_id,score,player_id,tournament_machine_id,tournament_id,row_number() over (partition by player_id, tournament_machine_id, tournament_id order by score desc) as p from scores %s) as sub where p=1) as sub_two) as sub_three order by machine_rank desc" % where_string
    return tournament_machines_query

def build_tournament_result(event_id, result,
                            player_top_machines,
                            players_dict,tournament_machines_dict,
                            tournament, values,
                            include_seperator=True):    
    value={}
    value['rank']=result[0]+1
    value['points']=result[1][0]
    value['player_id']=result[1].player_id
    player = players_dict[result[1].player_id]
    event_info = [event_info.player_id_for_event for event_info in player.event_info if event_info.event_id==event_id]
    value['event_player_id']= event_info[0]    
    value['tournament_id']=tournament.tournament_id
    value['tournament_name']=tournament.tournament_name
    value['player_name']=player.__repr__()
    value['seperator']=False        
    value['seperator_message']=""
    if tournament.finals_style == "PAPA":
        first_qualifying_delemiter=tournament.number_of_qualifiers
        second_qualifying_delemiter=None
        seperator_message="QUALIFYING CUTOFF"
    if tournament.finals_style == "PPO":
        first_qualifying_delemiter=tournament.number_of_qualifiers_for_a_when_finals_style_is_ppo
        second_qualifying_delemiter=tournament.number_of_qualifiers_for_b_when_finals_style_is_ppo
        seperator_message="QUALIFYING CUTOFF FOR A"
        seperator_message_b="QUALIFYING CUTOFF FOR B"
    if include_seperator:
        if len(values) > 0 and value['rank'] > first_qualifying_delemiter :
            if value['rank'] > first_qualifying_delemiter and values[len(values)-1]['rank'] <= first_qualifying_delemiter:
                print "in tournament %s" % tournament.tournament_id
                values.append({'rank':0,'seperator':True,'seperator_message':seperator_message})
            if second_qualifying_delemiter and value['rank'] > second_qualifying_delemiter and values[len(values)-1]['rank'] <= second_qualifying_delemiter:
                values.append({'rank':0, 'seperator':True,'seperator_message':seperator_message_b})                    

    value['ifpa_ranking_restricted']=tournament.ifpa_rank_restriction is not None and tournament.ifpa_rank_restriction > event_info.ifpa_ranking
    top_machines=[]
    for top_machine in player_top_machines[tournament.tournament_id].get(result[1].player_id):
        top_machines.append(top_machine)
    value['top_machines']=top_machines
    values.append(value)
    return value


@blueprints.test_blueprint.route('/<int:event_id>/test_tournament_results/<int:tournament_id>',methods=['GET'])
def test_tournament_results(event_id, tournament_id):
    players_dict={}
    tournament_machines_dict={}
    values=[]
    ranked_results_dict={}
    machine_ids=[]
    machine_dict={}
    ranked_machine_dict={}
    players=current_app.table_proxy.get_all_event_players(event_id)
    tournament_machines=current_app.table_proxy.get_tournament_machines(tournament_id)
    tournament = current_app.table_proxy.get_tournament_by_tournament_id(tournament_id)
    for player in players:
        players_dict[player.player_id]=player
    for tournament_machine in tournament_machines:
        tournament_machines_dict[tournament_machine.tournament_machine_id]=to_dict(tournament_machine)
    

    query = getTournamentResultsQuery(tournament_id,4)    
    machine_query = getTournamentMachineResultsQuery(tournament_id=tournament_id)    
    results = [result for result in current_app.table_proxy.db_handle.engine.execute(query)]                        
    machine_results = [result for result in current_app.table_proxy.db_handle.engine.execute(machine_query)]                            
    sorted_results = sorted(results, key= lambda e: e[0],reverse=True)
    ranked_results = list(Ranking(sorted_results,key=lambda pp: pp[0]))
    ranked_results_dict[tournament_id]=ranked_results    

    player_top_machines = {tournament_id:{}}        
    for i in machine_results:        
        if machine_dict.get(i.tournament_machine_id,None) is None:
            machine_dict[i.tournament_machine_id]=[]
        machine_dict[i.tournament_machine_id].append(i)        
        if player_top_machines[tournament_id].get(i.player_id,None) is None:                
            player_top_machines[tournament_id][i.player_id]=[]
        if len(player_top_machines[tournament_id][i.player_id]) < 3:            
            player_top_machines[tournament_id][i.player_id].append({'tournament_machine_id':i.tournament_machine_id,
                                                                    'tournament_machine_name':tournament_machines_dict[i.tournament_machine_id]['tournament_machine_name'],
                                                                    "abbreviation":tournament_machines_dict[i.tournament_machine_id]['tournament_machine_abbreviation'],
                                                                    "rank":get_rank_from_papa_points(i.machine_rank),
                                                                    "score":i.score})
    for tournament_id,tournament_results in ranked_results_dict.iteritems():                
        for idx, result in enumerate(tournament_results):
        #RANK - SCORE - PLAYER ID - TOURNAMENT ID            
            build_tournament_result(event_id, result,
                                    player_top_machines,
                                    players_dict,tournament_machines_dict,
                                    tournament, values)
            #values.append(value)
    return jsonify({'data':values})

@blueprints.test_blueprint.route('/<int:event_id>/test_player_results/<int:event_player_id>',methods=['GET'])
def test_player_results(event_id, event_player_id):
    players_dict={}
    tournament_machines_dict={}
    values=[]
    ranked_results_dict={}
    machine_ids=[]
    machine_dict={}
    ranked_machine_dict={}
    start_time = current_milli_time()
    
    event_player_info = get_event_player_route(current_app,event_id,event_player_id)
    event_player_info['tournament_calculated_lists']=event_player_info['tournament_calculated_lists']
    event_player_info['tournament_counts']=event_player_info['tournament_counts']    
    players=current_app.table_proxy.get_all_event_players(event_id)
    
    tournaments = current_app.table_proxy.get_tournaments(event_id)
    for player in players:
        players_dict[player.player_id]=player
    player_top_machines = {}        

    for tournament in tournaments:        

        player_top_machines[tournament.tournament_id]={}        
        tournament_machines=current_app.table_proxy.get_tournament_machines(tournament.tournament_id)
        for tournament_machine in tournament_machines:
           tournament_machines_dict[tournament_machine.tournament_machine_id]=to_dict(tournament_machine)        
        query = getTournamentResultsQuery(tournament.tournament_id,4)            
        machine_query = getTournamentMachineResultsQuery(tournament_id=tournament.tournament_id)            
        results = [result for result in current_app.table_proxy.db_handle.engine.execute(query)]                                
        machine_results = [result for result in current_app.table_proxy.db_handle.engine.execute(machine_query)]                                    
        sorted_results = sorted(results, key= lambda e: e[0],reverse=True)
        ranked_results = list(Ranking(sorted_results,key=lambda pp: pp[0]))
        ranked_results_dict[tournament.tournament_id]=ranked_results    

        
        for i in machine_results:        
            if machine_dict.get(i.tournament_machine_id,None) is None:
                machine_dict[i.tournament_machine_id]=[]
            machine_dict[i.tournament_machine_id].append(i)        
            if player_top_machines[tournament.tournament_id].get(i.player_id,None) is None:                
                player_top_machines[tournament.tournament_id][i.player_id]=[]
            if len(player_top_machines[tournament.tournament_id][i.player_id]) < 999:            
               player_top_machines[tournament.tournament_id][i.player_id].append({'tournament_machine_id':i.tournament_machine_id,
                                                                                  'tournament_machine_name':tournament_machines_dict[i.tournament_machine_id]['tournament_machine_name'],
                                                                                  "abbreviation":tournament_machines_dict[i.tournament_machine_id]['tournament_machine_abbreviation'],
                                                                                  "rank":get_rank_from_papa_points(i.machine_rank),
                                                                                  "score":i.score})        

    for tournament_id,tournament_results in ranked_results_dict.iteritems():                
        print "building results for %s" % tournament_id
        tournament = current_app.table_proxy.get_tournament_by_tournament_id(tournament_id)
        for idx, result in enumerate(tournament_results):
        ##RANK - SCORE - PLAYER ID - TOURNAMENT ID                        
            if result[1].player_id==event_player_info['data']['player_id']:                
                build_tournament_result(event_id, result,
                                        player_top_machines,
                                        players_dict,tournament_machines_dict,
                                        tournament, values,
                                        include_seperator=False)
            #values.append(value)
            pass    
    event_player_info['data']['values']=values
    #return jsonify({'data':values})
    return jsonify(event_player_info)


@blueprints.test_blueprint.route('/<int:event_id>/test_tournament_machine_results/<int:tournament_id>/<int:tournament_machine_id>',methods=['GET'])
def test_tournament_machine_results(event_id, tournament_id, tournament_machine_id):
    players_dict={}    
    values=[]            
    ranked_machine_dict={}
    players=current_app.table_proxy.get_all_event_players(event_id)        
    for player in players:
        players_dict[player.player_id]=player
    
    machine_query = getTournamentMachineResultsQuery(tournament_id=tournament_id,tournament_machine_id=tournament_machine_id)        
    machine_results = [result for result in current_app.table_proxy.db_handle.engine.execute(machine_query)]                                        
    sorted_results = sorted(machine_results, key= lambda e: e[0],reverse=True)
    ranked_results = list(Ranking(sorted_results,key=lambda pp: pp[0]))
    
    #    for machine_result in machine_results:
    for machine_result in ranked_results:        
        values.append({'rank':machine_result[0]+1,
                       'points':machine_result[1].machine_rank,
                       'player_id':machine_result[1].player_id,
                       'player_name':players_dict[machine_result[1].player_id].__repr__(),
                       'score':machine_result[1].score
            
        })        
    
    return jsonify({'data':values})


