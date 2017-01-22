from flask_restless.helpers import to_dict
from blueprints import admin_login_blueprint,admin_manage_blueprint
from flask import jsonify,current_app,request
import json
from werkzeug.exceptions import BadRequest,Conflict
from util import db_util
from util.permissions import Admin_permission,Scorekeeper_permission
from flask_login import login_required,current_user
from routes.utils import fetch_entity,check_player_team_can_start_game,set_token_start_time
from orm_creation import create_entry
import datetime
from sqlalchemy import and_,or_
import locale
from sqlalchemy import desc,asc

locale.setlocale(locale.LC_ALL, 'en_US')

@admin_manage_blueprint.route('/admin/audit_log/where_all_my_scores_at/player_id/<player_id>/audit_log_id/<audit_log_id>/time_delta/<minutes>',methods=['GET'])
#@login_required
#@Admin_permission.require(403)
def route_audit_log_missing_scores(player_id,audit_log_id,minutes):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    users = {user.user_id:user.to_dict_simple() for user in tables.User.query.all()}
    divisions = {division.division_id:division.to_dict_simple() for division in tables.Division.query.all()}
    metadivisions = {meta_division.meta_division_id:meta_division.to_dict_simple() for meta_division in tables.MetaDivision.query.all()}
    division_machines = {division_machine.division_machine_id:division_machine.to_dict_simple() for division_machine in tables.DivisionMachine.query.all()}
    players = {player.player_id:player.to_dict_simple() for player in tables.Player.query.all()}
    teams = {team.team_id:team.to_dict_simple() for team in tables.Team.query.all()}
    
    audit_log_base = fetch_entity(tables.AuditLog,audit_log_id)
    if audit_log_base.action_date:
        audit_log_base_date = audit_log_base.action_date    
    #if audit_log_base.game_started_date:
    #    audit_log_base_date = audit_log_base.game_started_date        
    audit_log_end_range = audit_log_base_date+datetime.timedelta(minutes=int(minutes))
    print "%s - %s" % (audit_log_base_date,audit_log_end_range)
    division_id = audit_log_base.token.division_id
    metadivision_id = audit_log_base.token.metadivision_id            
    audit_logs_query = tables.AuditLog.query
    if metadivision_id:
        div_string = " for metadivision %s" % metadivisions[metadivision_id]['meta_division_name']
        audit_logs_query = audit_logs_query.filter(tables.AuditLog.token.has(metadivision_id=metadivision_id))
    else:
        div_string = " for division %s" % divisions[division_id]['tournament_name']        
        audit_logs_query = audit_logs_query.filter(tables.AuditLog.token.has(division_id=division_id))        
    audit_logs_query=audit_logs_query.filter_by(action="Score Added")
    audit_logs = audit_logs_query.filter(
        and_(
            tables.AuditLog.action_date >= audit_log_base_date,
            tables.AuditLog.action_date <= audit_log_end_range
        )
    ).order_by(asc(tables.AuditLog.action_date)).all()
    #audit_logs = audit_logs_query.all()
    audit_log_list = []
    audit_log_index = 0
    print len(audit_logs)
    for audit_log in audit_logs:
        #while audit_log_index < len(audit_logs):        
        #audit_log=audit_logs[audit_log_index]        
        if audit_log.division_machine_id: 
            machine_name=division_machines[audit_log.division_machine_id]['division_machine_name']                    
        if audit_log.team_id:
            player_team_string = "team %s " % teams[audit_log.team_id]['team_name']
        else:
            player_team_string = "player %s "% players[audit_log.player_id]['first_name']+" "+players[audit_log.player_id]['first_name']
        if audit_log.action == "Voided":
            continue
        division_machine_name = division_machines[audit_log.division_machine_id]['division_machine_name']
        score = locale.format("%d",audit_log.entry.scores[0].score,grouping=True)

        audit_log_list.append({
            'audit_log_id':audit_log.audit_log_id,
            'contents': [audit_log.action_date,audit_log.action,player_team_string,score,division_machine_name]
        })
        
    return jsonify({'data':audit_log_list})

@admin_manage_blueprint.route('/admin/audit_log/where_all_my_tokens_at/player_id/<player_id>',methods=['GET'])
#@login_required
#@Admin_permission.require(403)
def route_audit_log_missing_tokens(player_id):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)                
    teams = tables.Player.query.filter_by(player_id=player_id).first().teams    
    if len(teams)>0:
        team_id = teams[0].team_id
        audit_logs = tables.AuditLog.query.filter(or_(tables.AuditLog.team_id==team_id,
                                                      tables.AuditLog.player_id==int(player_id))).order_by(desc(tables.AuditLog.action_date)).all()
    else:
        audit_logs = tables.AuditLog.query.filter_by(player_id=player_id).all()
    audit_log_list = []
    users = {user.user_id:user.to_dict_simple() for user in tables.User.query.all()}
    players = {player.player_id:player for player in tables.Player.query.all()}
    divisions = {division.division_id:division.to_dict_simple() for division in tables.Division.query.all()}
    metadivisions = {meta_division.meta_division_id:meta_division.to_dict_simple() for meta_division in tables.MetaDivision.query.all()}
    division_machines = {division_machine.division_machine_id:division_machine.to_dict_simple() for division_machine in tables.DivisionMachine.query.all()}
    audit_log_index = 0
    short_audit_log_list=[]
    prev_type_of_purchase=None
    audit_log_index = 0    
    for audit_log in audit_logs:        
        # on purchase (player)                                
        if audit_log.action == "Ticket Purchase":
            username = users[audit_log.user_id]['username']
            audit_log_list.append({
                'audit_log_id':audit_log.audit_log_id,
                'contents': [audit_log.action_date,audit_log.action,username,audit_log.description]
            })
        if audit_log.action == "Player Ticket Purchase Completed":
            playername = players[audit_log.player_id].get_full_name()            
            audit_log_list.append({
                'audit_log_id':audit_log.audit_log_id,
                'contents': [audit_log.action_date,audit_log.action,playername,audit_log.description]
            })

        if audit_log.action == "Player Ticket Purchase Started":
            playername = players[audit_log.player_id].get_full_name()
            audit_log_list.append({
                'audit_log_id':audit_log.audit_log_id,
                'contents': [audit_log.action_date,audit_log.action,playername,audit_log.description]
            })                        
        if audit_log.action == "Ticket Summary":                        
            audit_log_list.append({
                'audit_log_id':audit_log.audit_log_id,
                'contents': [audit_log.action_date,audit_log.action," ",audit_log.description]
            })
        if audit_log.action == "Game Started":            
            username = users[audit_log.user_id]['username']            
            machine_name=division_machines[audit_log.division_machine_id]['division_machine_name']                                
            audit_log_list.append({
                'audit_log_id':audit_log.audit_log_id,
                'contents': [audit_log.action_date,audit_log.action,username,machine_name]
            })
        if audit_log.action == "Score Added":            
            username = users[audit_log.user_id]['username']            
            machine_name=division_machines[audit_log.division_machine_id]['division_machine_name']                                
            if audit_log.entry and len(audit_log.entry.scores) > 0:
                score = locale.format("%d",audit_log.entry.scores[0].score,grouping=True)
            else:
                score = "SOMEONE DONE FUCKED UP"
            audit_log_list.append({
                'audit_log_id':audit_log.audit_log_id,
                'contents': [audit_log.action_date,audit_log.action,username,"(%s) %s"%(machine_name,score)]
            })
        if audit_log.action == "Score Voided":            
            username = users[audit_log.user_id]['username']            
            machine_name=division_machines[audit_log.division_machine_id]['division_machine_name']                                
            audit_log_list.append({
                'audit_log_id':audit_log.audit_log_id,
                'contents': [audit_log.action_date,audit_log.action,username,machine_name]
            })
        if audit_log.action == "Jagoff Declared":            
            username = users[audit_log.user_id]['username']            
            machine_name=division_machines[audit_log.division_machine_id]['division_machine_name']                                
            audit_log_list.append({
                'audit_log_id':audit_log.audit_log_id,
                'contents': [audit_log.action_date,audit_log.action,username,machine_name]
            })
        
    return jsonify({'data':audit_log_list})
