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

def getTournamentMachineResultsQuery(tournament_id, tournament_machine_id=None):
    where_string = "where tournament_id= %s " % tournament_id
    if tournament_machine_id:
        where_string = where_string + " and tournament_machine_id = %s"  % tournament_machine_id
    tournament_machines_query = "select machine_rank,tournament_machine_id,player_id,tournament_id,score, row_number() over (partition by player_id,tournament_id order by tournament_id,machine_rank desc) as row from (select tournament_id,player_id,score,tournament_machine_id,papa_scoring_func(rank() over (partition by tournament_machine_id order by score desc)) as machine_rank from (select score,player_id,tournament_machine_id,tournament_id from (select score_id,score,player_id,tournament_machine_id,tournament_id,row_number() over (partition by player_id, tournament_machine_id, tournament_id order by score desc) as p from scores %s) as sub where p=1) as sub_two) as sub_three order by player_id,machine_rank desc" % where_string
    return tournament_machines_query

def build_tournament_result(event_id, result,
                            player_top_machines,
                            players_dict,tournament_machines_dict,
                            ifpa_ranking_restricted=False,
                            seperator=False,seperator_message=None):    
    value={}
    value['rank']=result[0]
    value['player_id']=result[1].player_id
    player = players_dict[result[1].player_id]
    value['event_player_id']=[event_info.player_id_for_event for event_info in player.event_info if event_info.event_id==event_id][0]    
    value['player_name']=player.__repr__()
    value['seperator']=seperator
    value['seperator_message']=seperator_message
    value['ifpa_ranking_restricted']=ifpa_ranking_restricted
    top_machines=[]
    for top_machine_id in player_top_machines[result[1].player_id]:
        top_machines.append(tournament_machines_dict[top_machine_id])
    value['top_machines']=top_machines
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
    for player in players:
        players_dict[player.player_id]=player
    for tournament_machine in tournament_machines:
        tournament_machines_dict[tournament_machine.tournament_machine_id]=to_dict(tournament_machine)
    
#for x in range(1,7):    
    query = getTournamentResultsQuery(tournament_id,4)
    #query = getTournamentResultsQuery(x,4)
    machine_query = getTournamentMachineResultsQuery(tournament_id)
    #machine_query = getTournamentMachineResultsQuery(x)
    results = [result for result in current_app.table_proxy.db_handle.engine.execute(query)]                        
    machine_results = [result for result in current_app.table_proxy.db_handle.engine.execute(machine_query)]                        
    #tournament_id=x
    sorted_results = sorted(results, key= lambda e: e[0],reverse=True)
    ranked_results = list(Ranking(sorted_results,key=lambda pp: pp[0]))
    ranked_results_dict[tournament_id]=ranked_results    

    player_top_machines = {}        
    for i in machine_results:
        #machine_ids.append(i.tournament_machine_id)
        if machine_dict.get(i.tournament_machine_id,None) is None:
            machine_dict[i.tournament_machine_id]=[]
        machine_dict[i.tournament_machine_id].append(i)        
        if player_top_machines.get(i.player_id,None) is None:                
            player_top_machines[i.player_id]=[]
        if len(player_top_machines[i.player_id]) < 3:                
            player_top_machines[i.player_id].append(i.tournament_machine_id)

    
    for tournament_id,tournament_results in ranked_results_dict.iteritems():        
        for result in tournament_results:
        #RANK - SCORE - PLAYER ID - TOURNAMENT ID            
            value = []
            print "-------------"
            print result[0]
            print result[1].player_id
            value.append({'rank':result[0]})
            value.append({'points':result[1][0]})
            value.append({'player_name':players_dict[result[1][1]]})
            value.append({'tournament':result[1][2]})
            #value = "[%s,%s,%s,%s" % (result[0],result[1][0],players_dict[result[1][1]],result[1][2])            
            #value = value + ", [%s]]" % ','.join(player_top_machines[result[1][1]])
            top_machines=[]
            for top_machine_id in player_top_machines[result[1][1]]:
                top_machines.append(tournament_machines_dict[top_machine_id])
            value.append({'top_machines':top_machines})
            value = build_tournament_result(event_id, result,
                                            player_top_machines,
                                            players_dict,tournament_machines_dict)
            values.append(value)
    return jsonify({'data':values})
    

