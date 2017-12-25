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

def check_if_team(division_id=None,division_machine_id_external=None,team_id_external=None):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    team=False
    if team_id_external:
        return True
    if division_id:
        division = tables.Division.query.filter_by(division_id=division_id).first()
        if division.team_tournament:            
            team=True
    if division_machine_id_external:
        division_machine_external = tables.DivisionMachine.query.filter_by(division_machine_id=division_machine_id_external).first()
        if division_machine_external and division_machine_external.division.team_tournament:            
            team=True
    return team

def init_dicts(player_results_dict,
               team_results_dict,               
               sorted_player_list,
               ranked_player_list,
               sorted_team_list,
               ranked_team_list,
               player_entry_dict,
               team_entry_dict,
               top_6_machines,
               divisions,
               division_id,
               team):
    db = db_util.app_db_handle(current_app)    
    tables = db_util.app_db_tables(current_app)    
    players = tables.Player.query.all()
    if team:
        teams = tables.Team.query.all()    
    for player in players:        
        player_results_dict[player.player_id]={}
    if team:
        for team in teams:
            team_results_dict[team.team_id]={}
    for division in divisions:        
        if division_id != 0:
            division_machines = tables.DivisionMachine.query.filter_by(division_id=division.division_id).all()
        else:
            division_machines = tables.DivisionMachine.query.all()
        #return_dict[division.division_id]={}
        #for division_machine in division_machines:
        #    return_dict[division.division_id][division_machine.division_machine_id]=[]
        sorted_player_list[division.division_id]=[]
        ranked_player_list[division.division_id]=[]
        sorted_team_list[division.division_id]=[]
        ranked_team_list[division.division_id]=[]

        #player_entry_dict[division.division_id]=[]
        division_name = division.get_tournament_name(division.tournament)        
        player_entry_dict[division.division_id]={'tournament_name':division_name,'entries':[],'sum':0,'rank':0}
        team_entry_dict[division.division_id]={'tournament_name':division_name,'entries':[],'sum':0,'rank':0}
        
        top_6_machines[division.division_id]={}    
        if team:
            for team in teams:        
                team_results_dict[team.team_id][division.division_id]={'points':[],'sum':0,'team_name':team.team_name}            
                top_6_machines[division.division_id][team.team_id]=[]
        else:
            for player in players:        
                player_results_dict[player.player_id][division.division_id]={'points':[],'sum':0,'player_name':player.first_name+" "+player.last_name,'ifpa_ranking':player.ifpa_ranking}            
                top_6_machines[division.division_id][player.player_id]=[]
                

def build_division_machine_results(division_machine_results,new_dict,team):
    division_machine_result = new_dict
    if team:
        division_machine_results.append({'team_name':division_machine_result['team_name'],
                                         'team_id':division_machine_result['team_id'],
                                         'machine_name':division_machine_result['machine_name'],
                                         'division_machine_id':division_machine_result['division_machine_id'],
                                         'score':division_machine_result['score'],
                                         'rank':division_machine_result['filter_rank'],
                                         'points': get_papa_points_from_rank(division_machine_result['filter_rank'])})                                
    else:
        division_machine_results.append({'player_name':division_machine_result['player_name'],
                                         'player_id':division_machine_result['player_id'],
                                         'machine_name':division_machine_result['machine_name'],
                                         'division_machine_id':division_machine_result['division_machine_id'],
                                         'score':division_machine_result['score'],
                                         'rank':division_machine_result['filter_rank'],
                                         'points': get_papa_points_from_rank(division_machine_result['filter_rank'])})                

def build_new_dict(result,team):
    new_dict={
        'division_id':result['entry_division_id'],
        'machine_name':result['machine_machine_name'],
        'division_machine_id':result['score_division_machine_id'],
        'score':result['score_score'],
        'rank':result['scorerank'],
        'filter_rank':result['filter_rank']            
    }
    if team:
        new_dict['team_id']=result['team_team_id']
        new_dict['team_name']=result['team_team_name']
    else:
        new_dict['player_id']=result['player_player_id']
        new_dict['player_name']=result['player_first_name']+" "+result['player_last_name']
    return new_dict

def build_team_player_results(team_results_dict,player_results_dict, top_6_machines, result, divisions_lookup, team, player_id, team_id, entry_div_id):
    if team:                
        if len(team_results_dict[team_id][entry_div_id]['points'])<divisions_lookup[result['entry_division_id']].number_of_relevant_scores:
            filter_score = get_papa_points_from_rank(result['filter_rank'])
            team_results_dict[result['team_team_id']][result['entry_division_id']]['points'].append(filter_score)        
            team_results_dict[result['team_team_id']][result['entry_division_id']]['sum'] = sum(team_results_dict[result['team_team_id']][result['entry_division_id']]['points'])
            if(result['filter_rank'] < 900):
                top_6_machines[entry_div_id][team_id].append({'machine_name':result['machine_machine_name'],
                                                              'machine_abbreviation':result['machine_abbreviation'],
                                                              'division_machine_id':result['score_division_machine_id'],
                                                              'rank':result['filter_rank'],
                                                              'points':filter_score})                
    else:        
        if len(player_results_dict[player_id][entry_div_id]['points'])<divisions_lookup[result['entry_division_id']].number_of_relevant_scores:
            filter_score = get_papa_points_from_rank(result['filter_rank'])
            player_results_dict[result['player_player_id']][result['entry_division_id']]['points'].append(filter_score)        
            player_results_dict[result['player_player_id']][result['entry_division_id']]['sum'] = sum(player_results_dict[result['player_player_id']][result['entry_division_id']]['points'])
            if(result['filter_rank'] < 900):
                top_6_machines[entry_div_id][player_id].append({'machine_name':result['machine_machine_name'],
                                                                'machine_abbreviation':result['machine_abbreviation'],
                                                                'division_machine_id':result['score_division_machine_id'],
                                                                'rank':result['filter_rank'],
                                                                'points':filter_score})

def build_team_player_entry_dict(team, team_id_external, team_id, player_id_external, player_id, team_entry_dict, player_entry_dict,
                                 entry_div_id, result, player_results_dict, team_results_dict):
    if team:
        if team_id_external and int(team_id_external) == team_id:
            team_entry_dict[entry_div_id]['entries'].append(
                {
                    'machine_name':result['machine_machine_name'],
                    'division_machine_id':result['score_division_machine_id'],                        
                    'score':result['score_score'],
                    'rank':result['filter_rank'],
                    'points': get_papa_points_from_rank(result['filter_rank'])
                }
            )
            team_entry_dict[entry_div_id]['sum']=team_results_dict[result['team_team_id']][result['entry_division_id']]['sum']                                
    else:
        if player_id_external and int(player_id_external) == player_id:
            player_entry_dict[entry_div_id]['entries'].append(
                {
                    'machine_name':result['machine_machine_name'],
                    'division_machine_id':result['score_division_machine_id'],                        
                    'score':result['score_score'],
                    'rank':result['filter_rank'],
                    'points': get_papa_points_from_rank(result['filter_rank'])
                }
            )
            player_entry_dict[entry_div_id]['sum']=player_results_dict[result['player_player_id']][result['entry_division_id']]['sum']                

def return_team_results(team_results_dict,sorted_team_list,divisions,ranked_team_list,team_id_external,team_entry_dict,top_6_machines):
    for team_id,div in team_results_dict.iteritems():
        for div_id, team in div.iteritems():                
            sorted_team_list[div_id].append({'team_id':team_id,'sum':team['sum'],'team_name':team['team_name']})
    for division in [division for division in divisions if division.team_tournament is True]:
        sorted_team_list[division.division_id] = sorted(sorted_team_list[division.division_id], key= lambda e: e['sum'],reverse=True)
        ranked_team_list[division.division_id] = list(Ranking(sorted_team_list[division.division_id],key=lambda pp: pp['sum']))
    if team_id_external:
        for (ranked_division_id,ranked_results) in ranked_team_list.iteritems():
            for ranked_result in ranked_results:                                
                if ranked_result[1]['team_id']==int(team_id_external):                    
                    team_entry_dict[ranked_division_id]['rank']=ranked_result[0]
        return jsonify({'data':team_entry_dict})                
    return jsonify({'data':{'top_machines':top_6_machines,'ranked_team_list':ranked_team_list}})        

def return_player_results(player_results_dict,sorted_player_list,divisions,ranked_player_list,player_id_external,player_entry_dict,top_6_machines, return_json, division_id):
    for player_id,div in player_results_dict.iteritems():
        for div_id, player in div.iteritems():
            sorted_player_list[div_id].append({'player_id':player_id,'sum':player['sum'],'player_name':player['player_name'],'ifpa_ranking':player['ifpa_ranking']})
    for division in divisions:
        sorted_player_list[division.division_id] = sorted(sorted_player_list[division.division_id], key= lambda e: e['sum'],reverse=True)
        ranked_player_list[division.division_id] = list(Ranking(sorted_player_list[division.division_id],key=lambda pp: pp['sum']))
    if player_id_external:
        for (ranked_division_id,ranked_results) in ranked_player_list.iteritems():
            for ranked_result in ranked_results:                                
                if ranked_result[1]['player_id']==int(player_id_external):                    
                    player_entry_dict[ranked_division_id]['rank']=ranked_result[0]
        return jsonify({'data':player_entry_dict})        
    if return_json:
        top_6_machines_division_only = {key: value for (key, value) in top_6_machines.iteritems() if key == int(division_id)}
        # ranked_player_list_division_only = {key: value for (key, value) in ranked_player_list.iteritems() if key == int(division_id)}
        ranked_player_list_division_only = {key: value[:900] for (key, value) in ranked_player_list.iteritems() if key == int(division_id)}                
        return jsonify({'data':{'top_machines':top_6_machines_division_only,'ranked_player_list':ranked_player_list_division_only}})        
    else:
        return {'data':{'top_machines':top_6_machines,'ranked_player_list':ranked_player_list}}
    
def get_division_results(tournament_id=None,tournament_machine_id_external=None,player_id_external=None,team_id_external=None,return_json=True):
    #db = db_util.app_db_handle(current_app)
    db = current_app.table_proxy.db_handle    
    if tournament_id=="0":
        tournament_id=None
    #team=check_if_team(division_id,division_machine_id_external,team_id_external)
    team=False
    first_query = get_first_query(tournament_id,tournament_machine_id_external,team)
    results = db.engine.execute(first_query)##
    for result in results:
        print result
    return None
    second_query = get_herb_second_query(first_query,team)
    third_query = get_herb_third_query(second_query)
    fourth_query = get_herb_fourth_query(third_query)
    results = db.engine.execute(fourth_query)
    divisions = tables.Division.query.all()
    divisions_lookup = {division.division_id:division for division in divisions}

    player_results_dict = {}
    team_results_dict = {}
    player_entry_dict = {}
    team_entry_dict={}
    sorted_player_list = {}
    sorted_team_list = {}    
    ranked_player_list = {}
    ranked_team_list = {}
    top_6_machines = {}    
    division_machine_results = []    

    init_dicts(player_results_dict,
               team_results_dict,
               sorted_player_list,
               ranked_player_list,
               sorted_team_list,
               ranked_team_list,
               player_entry_dict,
               team_entry_dict,
               top_6_machines,
               divisions,
               division_id,
               team)    
    for result in results:        
        new_dict = build_new_dict(result,team)
        entry_div_id = result['entry_division_id']
        if team:
            team_id = result['team_team_id']
            player_id = None
        else:
            player_id = result['player_player_id']
            team_id = None
        if division_machine_id_external:            
            build_division_machine_results(division_machine_results,new_dict,team)
        if division_machine_id_external is None:
            build_team_player_results(team_results_dict,player_results_dict, top_6_machines, result, divisions_lookup, team, player_id, team_id, entry_div_id)
            build_team_player_entry_dict(team, team_id_external, team_id, player_id_external, player_id, team_entry_dict, player_entry_dict,
                                         entry_div_id, result, player_results_dict, team_results_dict)
    if division_machine_id_external:
        return jsonify({'data': division_machine_results})
    if team:        
        return return_team_results(team_results_dict,sorted_team_list,divisions,ranked_team_list,team_id_external,team_entry_dict,top_6_machines)        
    else:
        return return_player_results(player_results_dict,sorted_player_list,divisions,ranked_player_list,player_id_external,player_entry_dict,top_6_machines,return_json,division_id)


# @blueprints.test_blueprint.route('/<int:event_id>/results/player/<player_id>',methods=['GET'])
# def route_get_player_results(event_id,player_id):
#     return get_division_results(player_id_external=player_id)

# @blueprints.test_blueprint.route('/<int:event_id>/results/team/<team_id>',methods=['GET'])
# def route_get_team_results(event_id,team_id):
#     return get_division_results(team_id_external=team_id)
 
# @blueprints.test_blueprint.route('/<int:event_id>/results/tournament/<tournament_id>',methods=['GET'])
# def route_get_division_results(event_id,tournament_id):    
#     return get_division_results(division_id=division_id)

def get_ranked_qualifying_ppo_players(division_id,absent_players,tie_breaker_ranks):
    tables = db_util.app_db_tables(current_app)
    division = fetch_entity(tables.Division,division_id)         
    max_ifpa_rank = division.ppo_a_ifpa_range_end
    num_a_qualifiers = division.finals_num_qualifiers_ppo_a
    type_of_ranked_list=None
    if division.team_tournament:
        ppo_results = json.loads(get_division_results(division_id=division_id,return_json=False).data)
        type_of_ranked_list="ranked_team_list"
        type_of_competitor_id="team_id"        
    else:
        ppo_results = get_division_results(division_id=division_id,return_json=False)
        type_of_ranked_list="ranked_player_list"
        type_of_competitor_id="player_id"        
    ppo_qualifying_list = []
    #match_absent_player = lambda x: str(x[1]['player_id']) in absent_players                
    for div_id,div_results in ppo_results['data'][type_of_ranked_list].iteritems():                
        if int(div_id) != division.division_id:            
            continue        
        for idx,player_result in enumerate(div_results):                        
            player = player_result[1]                        
            if str(player[type_of_competitor_id]) in absent_players:                                
                continue
            if type_of_competitor_id=='player_id' and player['ifpa_ranking'] < max_ifpa_rank:
                if str(player[type_of_competitor_id]) in tie_breaker_ranks and int(tie_breaker_ranks[str(player[type_of_competitor_id])]) > num_a_qualifiers:
                    continue
                if idx > num_a_qualifiers :                
                    continue
            if str(player[type_of_competitor_id]) in tie_breaker_ranks:                
                new_rank = tie_breaker_ranks[str(player[type_of_competitor_id])]                
                player_result[1]['temp_rank']=int(new_rank)-1                
                ppo_qualifying_list.append(player_result[1])
            else:
                player_result[1]['temp_rank']=player_result[0]
                ppo_qualifying_list.append(player_result[1])
    sorted_list = sorted(ppo_qualifying_list, key= lambda e: e['temp_rank'])
    return list(Ranking(sorted_list,key=lambda pp: pp['temp_rank'],reverse=True))
    

# @blueprints.test_blueprint.route('/<int:event_id>/results/tournament/<tournament_id>/ppo/qualifying',methods=['GET'])
# def route_get_tournament_ppo_qualifying_results(tournament_id):
#     absent_players_raw = request.args.get('absent_players')
#     tie_breaker_ranks = json.loads(request.data)    
#     reranked_ppo_qualifying_list = get_ranked_qualifying_ppo_players(division_id,absent_players_raw,tie_breaker_ranks)
#     return jsonify({'data':reranked_ppo_qualifying_list})

# @admin_manage_blueprint.route('/results/tournament/<tournament_id>/ppo/qualifying/list',methods=['PUT'])
# def route_get_tournament_ppo_qualifying_results_list(tournament_id):
#     tables = db_util.app_db_tables(current_app)
#     #absent_players_raw = request.args.get('absent_players',None)    
#     #tie_breaker_ranks = json.loads(request.data)
#     json_data = json.loads(request.data)
#     if 'tie_breaker_ranks' in json_data:
#         tie_breaker_ranks = json_data['tie_breaker_ranks']
#     else:
#         tie_breaker_ranks = {}
#     if 'absent_players' in json_data:        
#         absent_players = json_data['absent_players']        
#     else:
#         absent_players = {}
        
#     reranked_ppo_qualifying_list = get_ranked_qualifying_ppo_players(division_id,absent_players,tie_breaker_ranks)    
#     division = fetch_entity(tables.Division,division_id)         
#     if division.finals_player_selection_type == "ppo":
#         num_a_qualifiers = division.finals_num_qualifiers_ppo_a
#         num_b_qualifiers = division.finals_num_qualifiers_ppo_b
#         a_end_rank=num_a_qualifiers
#         if len(reranked_ppo_qualifying_list) < a_end_rank:
#             a_end_rank = len(reranked_ppo_qualifying_list)
#         while(reranked_ppo_qualifying_list[a_end_rank-1][0] == reranked_ppo_qualifying_list[a_end_rank][0]):
#             a_end_rank = a_end_rank+1
#         b_end_rank=a_end_rank + num_b_qualifiers    
#         if len(reranked_ppo_qualifying_list) < b_end_rank:                
#             b_end_rank = len(reranked_ppo_qualifying_list)
#         while(reranked_ppo_qualifying_list[b_end_rank-1][0] == reranked_ppo_qualifying_list[b_end_rank][0]):
#             b_end_rank = b_end_rank+1
            
#         #print reranked_ppo_qualifying_list[0:a_end_rank]
#         return jsonify({'data':{'a':reranked_ppo_qualifying_list[0:a_end_rank],
#                                 'b':reranked_ppo_qualifying_list[a_end_rank:b_end_rank],
#                                 'rest':reranked_ppo_qualifying_list[b_end_rank:]}})

#     if division.finals_player_selection_type == "papa":
#         num_qualifiers = division.finals_num_qualifiers        
#         end_rank=num_qualifiers
 
#         while(reranked_ppo_qualifying_list[end_rank-1][0] == reranked_ppo_qualifying_list[end_rank][0]):
#             end_rank = end_rank+1
        
#         return jsonify({'data':{'qualified':reranked_ppo_qualifying_list[0:end_rank],
#                                 'rest':reranked_ppo_qualifying_list[end_rank:]}})
        
current_milli_time = lambda: int(round(time.time() * 1000))

def rock_and_roll():    
    query = "select sum(machine_rank), player_id, tournament_id from (select machine_rank,tournament_machine_id,player_id,tournament_id,row_number() over (partition by player_id,tournament_id order by tournament_id,machine_rank desc) as row from (select tournament_id,player_id,score,tournament_machine_id,papa_scoring_func(rank() over (partition by tournament_machine_id order by score desc)) as machine_rank from (select score,player_id,tournament_machine_id,tournament_id from (select score_id,score,player_id,tournament_machine_id,tournament_id,row_number() over (partition by player_id, tournament_machine_id, tournament_id order by score desc) as p from scores) as sub where p=1) as sub_two) as sub_three order by player_id) as sub_four where row < 7 group by player_id,tournament_id"
    #query = "select sum(machine_rank), player_id, tournament_id from (select machine_rank,tournament_machine_id,player_id,tournament_id,row_number() over (partition by player_id,tournament_id order by tournament_id,machine_rank desc) as row from (select tournament_id,player_id,score,tournament_machine_id,papa_scoring_func(rank() over (partition by tournament_machine_id order by score desc)) as machine_rank from (select score,player_id,tournament_machine_id,tournament_id from (select score_id,score,player_id,tournament_machine_id,tournament_id,row_number() over (partition by player_id, tournament_machine_id, tournament_id order by score desc) as p from scores where tournament_id=1) as sub where p=1) as sub_two) as sub_three order by player_id) as sub_four where row < 7 group by player_id,tournament_id"
    tournament_machines_query = "select machine_rank,tournament_machine_id,player_id,tournament_id,row_number() over (partition by player_id,tournament_id order by tournament_id,machine_rank desc) as row from (select tournament_id,player_id,score,tournament_machine_id,papa_scoring_func(rank() over (partition by tournament_machine_id order by score desc)) as machine_rank from (select score,player_id,tournament_machine_id,tournament_id from (select score_id,score,player_id,tournament_machine_id,tournament_id,row_number() over (partition by player_id, tournament_machine_id, tournament_id order by score desc) as p from scores) as sub where p=1) as sub_two) as sub_three order by player_id"
    #tournament_machines_query = "select machine_rank,tournament_machine_id,player_id,tournament_id,row_number() over (partition by player_id,tournament_id order by tournament_id,machine_rank desc) as row from (select tournament_id,player_id,score,tournament_machine_id,papa_scoring_func(rank() over (partition by tournament_machine_id order by score desc)) as machine_rank from (select score,player_id,tournament_machine_id,tournament_id from (select score_id,score,player_id,tournament_machine_id,tournament_id,row_number() over (partition by player_id, tournament_machine_id, tournament_id order by score desc) as p from scores where tournament_id=1) as sub where p=1) as sub_two) as sub_three order by player_id"
    
    #query = "select machine_scores.player_id, sum(machine_scores.ranking) from (select tournament_machine_id,score_id,score,scores.player_id, papa_scoring_func(rank() over (partition by scores.tournament_machine_id order by score)) as ranking from scores) as machine_scores group by machine_scores.player_id"
    results = [result for result in current_app.table_proxy.db_handle.engine.execute(query)]                
    machine_results = [result for result in current_app.table_proxy.db_handle.engine.execute(tournament_machines_query)]                
    ranked_results_dict={}
    ranked_machine_dict={}            
    machine_dict={}
    machine_ids={}
    for i in machine_results:
        machine_ids[i.tournament_machine_id]=i.tournament_machine_id
        if machine_dict.get(i.tournament_machine_id,None) is None:
            machine_dict[i.tournament_machine_id]=[]
        machine_dict[i.tournament_machine_id].append(i)
    for machine_id in machine_ids:
        sorted_results = sorted([result for result in machine_dict[machine_id]], key= lambda e: e[0],reverse=True)
        ranked_results = list(Ranking(sorted_results,key=lambda pp: pp[0]))
        ranked_machine_dict[machine_id]=ranked_results
    for i in range(1,7):
        sorted_results = sorted([result for result in results if result.tournament_id==i], key= lambda e: e[0],reverse=True)
        ranked_results = list(Ranking(sorted_results,key=lambda pp: pp[0]))
        ranked_results_dict[i]=ranked_results    
    return ranked_results_dict,ranked_machine_dict

@blueprints.test_blueprint.route('/test',methods=['GET'])
def test():
    start_time_raw = time.time()
    start_time = current_milli_time()
#    query = "select tournaments.tournament_id,machine_scores.player_id, sum(machine_scores.ranking) from (select tournament_machine_id,score_id,score,scores.player_id,papa_scoring_func(rank() over (partition by scores.tournament_machine_id order by score)) as ranking from scores) as machine_scores, tournament_machines,tournaments where machine_scores.tournament_machine_id=tournament_machines.tournament_machine_id and tournament_machines.tournament_id=tournaments.tournament_id and machine_scores.score_id in (select score_id from (select score_id, row_number() over (partition by scores.player_id order by score) as p from scores,entries where scores.entry_id=entries.entry_id and entries.voided=false) as x where x.p<7) group by machine_scores.player_id,tournaments.tournament_id"
#    results = current_app.table_proxy.db_handle.engine.execute(query)
#    sorted_results = sorted(results, key= lambda e: e[2],reverse=True)
# ranked_results = list(Ranking(sorted_results,key=lambda pp: pp[2]))
    values=[]    
    ranked_results,ranked_machine_results=rock_and_roll()
    for tournament_id,tournament_results in ranked_results.iteritems():
        for result in tournament_results:
            value = "%s,%s,%s,%s" % (result[0],result[1][0],result[1][1],result[1][2])
            #value = "%s,%s,%s" %(result[0],result[1],result[2])            
            values.append(value)                
    for tournament_machine_id,results in ranked_machine_results.iteritems():
        for result in results:
            value = "%s - %s %s %s" % (result[0],result[1][0],result[1][1],result[1][2])        
            values.append(value)                
    
    return jsonify({'data':values,'raw_data':(time.time())-start_time_raw})
    #return jsonify({})
    
@blueprints.test_blueprint.route('/<int:event_id>/results/tournament_machine/<tournament_machine_id>',methods=['GET'])
def route_get_tournament_machine_results(event_id,tournament_machine_id):
    sub_query_sub_two='(select score_id, row_number() over (partition by scores.player_id order by score) as p from scores,entries where scores.entry_id=entries.entry_id and entries.voided=false)'
    sub_query_two='select score_id from ('+sub_query_sub_two+') as x where x.p<4'
    query_for_machine_only='select tournament_machines.tournament_machine_id,score_id,score,scores.player_id,papa_scoring_func(rank() over (partition by scores.tournament_machine_id order by score)) as ranking from scores,tournament_machines where tournament_machines.tournament_machine_id=scores.tournament_machine_id and tournament_machines.tournament_id=%s'%(1)
    sub_query_one='select tournament_machine_id,score_id,score,scores.player_id,papa_scoring_func(rank() over (partition by scores.tournament_machine_id order by score)) as ranking from scores'    
    results = current_app.table_proxy.db_handle.engine.execute(query_for_machine_only)
    for result in results:
        print "machine_id"+str(result.tournament_machine_id)
        print "score_id"+str(result.score_id)
        print "score"+str(result.score)
        print "player_id"+str(result.player_id)
        print "ranking"+str(result.ranking)
        print "---------"
    results = current_app.table_proxy.db_handle.engine.execute('select tournaments.tournament_id,machine_scores.player_id, sum(machine_scores.ranking) from ('+sub_query_one+') as machine_scores, tournament_machines,tournaments where machine_scores.tournament_machine_id=tournament_machines.tournament_machine_id and tournament_machines.tournament_id=tournaments.tournament_id and machine_scores.score_id in ('+sub_query_two+') group by machine_scores.player_id,tournaments.tournament_id')    
    for result in results:        
       print result.tournament_id
       print result.player_id
       print result[2]
    #get_division_results(tournament_machine_id_external=tournament_machine_id)
    return jsonify({})

# @blueprints.test_blueprint.route('/<int:event_id>/results/player_best_scores/tournament/<tournament_id>/player/<player_id>',methods=['GET'])
# def route_get_player_best_scores_tournament_results(tournament_id,player_id):
#     db = db_util.app_db_handle(current_app)
#     tables = db_util.app_db_tables(current_app)
#     #tables.Score.query.filter(func.max(tables.Score.score)).all()
#     max_scores = db.session.query(func.max(tables.Score.score),tables.Score.division_machine_id).join(tables.Entry).filter_by(player_id=player_id,division_id=division_id).group_by(tables.Score.division_machine_id).all()            
#     for score in max_scores:
#         print score[0]
#     return jsonify({'data':{score[1]:score[0] for score in max_scores}})



def get_first_query(tournament_id=None, tournament_machine_id=None,team=False):
    #db = current_app.table_proxy.db_handle    
    table_proxy = current_app.table_proxy
    where_string = "entries.voided=false "
    if tournament_id:
        where_string = where_string + " and entries.tournament_id=%s" % tournament_id
    if tournament_machine_id:
        where_string = where_string + " and scores.tournament_machine_id = "+tournament_machine_id
    papa_scoring_func = func.papa_scoring_func(func.rank().over(order_by=desc(table_proxy.Scores.score),
                                                                   partition_by=(table_proxy.Entries.tournament_id,
                                                                                 table_proxy.Scores.tournament_machine_id))).label('scorepoints')            
    if team:
        giant_join = join(join(join(tables.Machine,join(join(tables.Division,tables.Tournament),tables.DivisionMachine)),tables.Score), join(tables.Entry, tables.Team))
        return select([                
            tables.Entry.entry_id,
            tables.Entry.division_id,
            tables.Entry.team_id,        
            tables.Score.score_id,
            tables.Score.entry_id,
            tables.Score.division_machine_id,        
            tables.Score.score,
            tables.Team.team_id,
            tables.Team.team_name,
            #tables.Player.first_name,
            #tables.Player.last_name,
            #tables.Player.player_id,        
            tables.Machine.machine_id,
            tables.Machine.machine_name,
            tables.Machine.abbreviation,
            func.rank().over(order_by=desc(tables.Score.score),
                             partition_by=tables.Score.division_machine_id).label('scorerank')],
            use_labels=True).select_from(giant_join).where(text(where_string)).order_by(desc(text("entry.division_id,score.division_machine_id,scorerank"))).alias('first_query')
        
    else:
        giant_join = join(join(join(table_proxy.Scores,table_proxy.TournamentMachines),table_proxy.Tournaments), join(table_proxy.Entries, table_proxy.Players))
        return select([                
            table_proxy.Entries.entry_id,
            table_proxy.Entries.tournament_id,
            table_proxy.Entries.player_id,        
            table_proxy.Scores.score_id,
            table_proxy.Scores.entry_id,
            table_proxy.Scores.tournament_machine_id,        
            table_proxy.Scores.score,        
            table_proxy.Players.first_name,
            table_proxy.Players.last_name,
            table_proxy.Players.player_id,        
            table_proxy.TournamentMachines.tournament_machine_id,
            table_proxy.TournamentMachines.tournament_machine_name,
            table_proxy.TournamentMachines.tournament_machine_abbreviation,
            func.rank().over(order_by=desc(table_proxy.Scores.score),
                             partition_by=table_proxy.Scores.tournament_machine_id).label('scorerank')],
            use_labels=True).select_from(giant_join).where(text(where_string)).order_by(desc(text("entries.tournament_id,scores.tournament_machine_id,scorerank"))).alias('first_query')

def get_herb_fourth_query(third_query):
    fourth_query_rank = func.rank().over(order_by=desc(third_query.c.score_score),
                                         partition_by=(third_query.c.score_division_machine_id))

    return select([
        third_query,
        fourth_query_rank.label('filter_rank'),                
#        func.papa_scoring_func(func.rank().over(order_by=desc(third_query.c.score_score),
#                                  partition_by=(third_query.c.score_division_machine_id))).label('filter_score')
#        func.rank().over(order_by=desc(third_query.c.score_score),
#                 partition_by=(third_query.c.score_division_machine_id)).label('filter_score')
    ]).select_from(third_query).order_by(fourth_query_rank).alias('fourth_query')
    
def get_herb_third_query(second_query):
    return select([
        second_query
    ]).select_from(second_query).where(second_query.c.single_players_rank_on_machine == 1).alias('third_query')
    
def get_herb_second_query(first_query,team=False):
    if team:
        return select([
            first_query,                
            #        func.rank().over(order_by=desc(first_query.c.scorepoints),
            #        func.rank().over(order_by=desc(first_query.c.scorerank),
            func.rank().over(order_by=asc(first_query.c.scorerank),                
                             partition_by=(first_query.c.entry_team_id,
                                           first_query.c.score_division_machine_id)
            ).label('single_players_rank_on_machine'),                
        ]).select_from(first_query).alias('second_query')            
    else:
        return select([
            first_query,                
            #        func.rank().over(order_by=desc(first_query.c.scorepoints),
            #        func.rank().over(order_by=desc(first_query.c.scorerank),
            func.rank().over(order_by=asc(first_query.c.scorerank),                
                             partition_by=(first_query.c.entry_player_id,
                                           first_query.c.score_division_machine_id)
            ).label('single_players_rank_on_machine'),                
        ]).select_from(first_query).alias('second_query')    
