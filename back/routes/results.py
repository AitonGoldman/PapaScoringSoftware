from blueprints import admin_login_blueprint,admin_manage_blueprint
from ranking import Ranking
from sqlalchemy.sql import functions
#from sqlalchemy import within_group
from sqlalchemy.orm import join
from sqlalchemy.sql.expression import desc, asc
from flask import jsonify, request, abort, current_app
from util import db_util
from sqlalchemy import null, func, text, and_
from sqlalchemy.sql import select

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

def get_division_results(division_id=None,division_machine_id_external=None,player_id_external=None,team_id_external=None):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    if division_id=="0":
        division_id=None
    team=False
    if division_id:
        division = tables.Division.query.filter_by(division_id=division_id).first()
        if division.team_tournament:
            team=True
    first_query = get_first_query(division_id,division_machine_id_external,team)
    second_query = get_herb_second_query(first_query,team)
    third_query = get_herb_third_query(second_query)
    fourth_query = get_herb_fourth_query(third_query)
    results = db.engine.execute(fourth_query)
    divisions = tables.Division.query.all()
    players = tables.Player.query.all()
    if team:
        teams = tables.Team.query.all()
    return_dict = {}
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
        return_dict[division.division_id]={}
        for division_machine in division_machines:
            return_dict[division.division_id][division_machine.division_machine_id]=[]
        sorted_player_list[division.division_id]=[]
        ranked_player_list[division.division_id]=[]
        sorted_team_list[division.division_id]=[]
        ranked_team_list[division.division_id]=[]

        #player_entry_dict[division.division_id]=[]
        division_name = division.get_tournament_name(division.tournament)        
        player_entry_dict[division.division_id]={'tournament_name':division_name,'entries':[],'sum':0,'rank':0}
        top_6_machines[division.division_id]={}    
        if team:
            for team in teams:        
                team_results_dict[team.team_id][division.division_id]={'points':[],'sum':0,'team_name':team.team_name}            
                top_6_machines[division.division_id][team.team_id]=[]
        else:
            for player in players:        
                player_results_dict[player.player_id][division.division_id]={'points':[],'sum':0,'player_name':player.first_name+" "+player.last_name}            
                top_6_machines[division.division_id][player.player_id]=[]
                
    for result in results:        
        new_dict={
            'division_id':result['entry_division_id'],
            #'player_id':result['player_player_id'],
            #'player_name':result['player_first_name']+" "+result['player_last_name'],
            'machine_name':result['machine_machine_name'],
            'division_machine_id':result['score_division_machine_id'],
            'score':result['score_score'],
            'rank':result['scorerank'],
            ##'points':result['scorepoints']#,
            #'filter_points':result['filter_score'],
            'filter_rank':result['filter_rank']            
        }
        if team:
            new_dict['team_id']=result['team_team_id']
            new_dict['team_name']=result['team_team_name']
        else:
            new_dict['player_id']=result['player_player_id']
            new_dict['player_name']=result['player_first_name']+" "+result['player_last_name']
        entry_div_id = result['entry_division_id']
        score_div_machine_id = result['score_division_machine_id']        
        return_dict[entry_div_id][score_div_machine_id].append(new_dict)
        if team:
            team_id = result['team_team_id']
        else:
            player_id = result['player_player_id']
        
        entry_div_id = result['entry_division_id']
        if division_machine_id_external:            
            #for division_machine_result in return_dict[entry_div_id][score_div_machine_id]:
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
            ## machine view            
        if division_machine_id_external is None:
            if team:
                if len(team_results_dict[team_id][entry_div_id]['points'])<3:
                    filter_score = get_papa_points_from_rank(result['filter_rank'])
                    team_results_dict[result['team_team_id']][result['entry_division_id']]['points'].append(filter_score)        
                    team_results_dict[result['team_team_id']][result['entry_division_id']]['sum'] = sum(team_results_dict[result['team_team_id']][result['entry_division_id']]['points'])
                    if(result['filter_rank'] < 150):
                        top_6_machines[entry_div_id][team_id].append({'machine_name':result['machine_machine_name'],
                                                                      'machine_abbreviation':result['machine_abbreviation'],
                                                                      'division_machine_id':result['score_division_machine_id'],
                                                                      'rank':result['filter_rank'],
                                                                      'points':filter_score})                
            else:
                if len(player_results_dict[player_id][entry_div_id]['points'])<3:
                    filter_score = get_papa_points_from_rank(result['filter_rank'])
                    player_results_dict[result['player_player_id']][result['entry_division_id']]['points'].append(filter_score)        
                    player_results_dict[result['player_player_id']][result['entry_division_id']]['sum'] = sum(player_results_dict[result['player_player_id']][result['entry_division_id']]['points'])
                    if(result['filter_rank'] < 150):
                        top_6_machines[entry_div_id][player_id].append({'machine_name':result['machine_machine_name'],
                                                                        'machine_abbreviation':result['machine_abbreviation'],
                                                                        'division_machine_id':result['score_division_machine_id'],
                                                                        'rank':result['filter_rank'],
                                                                        'points':filter_score})
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
    if division_machine_id_external:
        return jsonify({'data': division_machine_results})
    if team:
        for team_id,div in team_results_dict.iteritems():
            for div_id, team in div.iteritems():                
                sorted_team_list[div_id].append({'team_id':team_id,'sum':team['sum'],'team_name':team['team_name']})
        for division in divisions:
            sorted_team_list[division.division_id] = sorted(sorted_team_list[division.division_id], key= lambda e: e['sum'],reverse=True)
            ranked_team_list[division.division_id] = list(Ranking(sorted_team_list[division.division_id],key=lambda pp: pp['sum']))
        if team_id_external:
            for (ranked_division_id,ranked_results) in ranked_team_list.iteritems():
                for ranked_result in ranked_results:                                
                    if ranked_result[1]['team_id']==int(team_id_external):                    
                        team_entry_dict[ranked_division_id]['rank']=ranked_result[0]
            return jsonify({'data':team_entry_dict})        
        return jsonify({'data':{'top_machines':top_6_machines,'ranked_team_list':ranked_team_list}})        
    else:
        for player_id,div in player_results_dict.iteritems():
            for div_id, player in div.iteritems():
                sorted_player_list[div_id].append({'player_id':player_id,'sum':player['sum'],'player_name':player['player_name']})
        for division in divisions:
            sorted_player_list[division.division_id] = sorted(sorted_player_list[division.division_id], key= lambda e: e['sum'],reverse=True)
            ranked_player_list[division.division_id] = list(Ranking(sorted_player_list[division.division_id],key=lambda pp: pp['sum']))
        if player_id_external:
            for (ranked_division_id,ranked_results) in ranked_player_list.iteritems():
                for ranked_result in ranked_results:                                
                    if ranked_result[1]['player_id']==int(player_id_external):                    
                        player_entry_dict[ranked_division_id]['rank']=ranked_result[0]
            return jsonify({'data':player_entry_dict})        
        return jsonify({'data':{'top_machines':top_6_machines,'ranked_player_list':ranked_player_list}})


@admin_manage_blueprint.route('/results/player/<player_id>',methods=['GET'])
def route_get_player_results(player_id):
    return get_division_results(player_id_external=player_id)
                       
@admin_manage_blueprint.route('/results/division/<division_id>',methods=['GET'])
def route_get_division_results(division_id):
    return get_division_results(division_id=division_id)

@admin_manage_blueprint.route('/results/division_machine/<division_machine_id>',methods=['GET'])
def route_get_division_machine_results(division_machine_id):
    return get_division_results(division_machine_id_external=division_machine_id)
    
def get_first_query(division_id=None, division_machine_id=None,team=False):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    where_string = "entry.voided=false "
    if division_id:
        where_string = where_string + " and entry.division_id=%s" % division_id
    #else:
    #    where_string = "entry.division_id > 0"

    if division_machine_id:
        where_string = where_string + " and score.division_machine_id = "+division_machine_id
    papa_scoring_func = func.papa_scoring_func(func.rank().over(order_by=desc(tables.Score.score),
                                                                   partition_by=(tables.Entry.division_id,
                                                                                 tables.Score.division_machine_id))).label('scorepoints')            
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
        giant_join = join(join(join(tables.Machine,join(join(tables.Division,tables.Tournament),tables.DivisionMachine)),tables.Score), join(tables.Entry, tables.Player))
        return select([                
            tables.Entry.entry_id,
            tables.Entry.division_id,
            tables.Entry.player_id,        
            tables.Score.score_id,
            tables.Score.entry_id,
            tables.Score.division_machine_id,        
            tables.Score.score,        
            tables.Player.first_name,
            tables.Player.last_name,
            tables.Player.player_id,        
            tables.Machine.machine_id,
            tables.Machine.machine_name,
            tables.Machine.abbreviation,
            func.rank().over(order_by=desc(tables.Score.score),
                             partition_by=tables.Score.division_machine_id).label('scorerank')],
            use_labels=True).select_from(giant_join).where(text(where_string)).order_by(desc(text("entry.division_id,score.division_machine_id,scorerank"))).alias('first_query')

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
