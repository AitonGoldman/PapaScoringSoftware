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

@admin_manage_blueprint.route('/admin/audit_log/where_all_my_tokens_at/player_id/<player_id>',methods=['GET'])
#@login_required
#@Admin_permission.require(403)
def route_audit_log_missing_tokens(player_id):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)                
    audit_logs = tables.AuditLog.query.filter_by(player_id=player_id).all()
    teams = tables.Player.query.filter_by(player_id=player_id).first().teams
    if len(teams)>0:
        team_id = teams[0].team_id
        audit_logs = audit_logs + tables.AuditLog.query.filter_by(team_id=team_id).all()                
    audit_log_list = []
    users = {user.user_id:user.to_dict_simple() for user in tables.User.query.all()}
    divisions = {division.division_id:division.to_dict_simple() for division in tables.Division.query.all()}
    metadivisions = {meta_division.meta_division_id:meta_division.to_dict_simple() for meta_division in tables.MetaDivision.query.all()}
    division_machines = {division_machine.division_machine_id:division_machine.to_dict_simple() for division_machine in tables.DivisionMachine.query.all()}
    audit_log_index = 0
    short_audit_log_list=[]
    prev_type_of_purchase=None
    #while audit_log_index < len(audit_logs):
    #    short_audit_log_list.append(audit_logs[audit_log_index])                    
    #    audit_log_index=audit_log_index+1
    audit_log_index = 0
    super_short_audit_log_list=[]
    while audit_log_index < len(audit_logs):        
        if(audit_log_index == len(audit_logs)-1):            
            super_short_audit_log_list.append(audit_logs[audit_log_index])
            audit_log_index=audit_log_index+1
            continue
        if audit_logs[audit_log_index].purchase_date is not None:            
            next_al_purchase_d = audit_logs[audit_log_index+1].purchase_date
            this_al_div_id = audit_logs[audit_log_index].token.division_id
            next_al_div_id = audit_logs[audit_log_index+1].token.division_id            
            this_al_mdiv_id = audit_logs[audit_log_index].token.metadivision_id
            next_al_mdiv_id = audit_logs[audit_log_index+1].token.metadivision_id            
            
            if (this_al_div_id and next_al_div_id != this_al_div_id) or (next_al_purchase_d is None):                
                super_short_audit_log_list.append(audit_logs[audit_log_index])
                audit_log_index=audit_log_index+1                
                continue
            if (this_al_mdiv_id and next_al_mdiv_id != this_al_mdiv_id) or (next_al_purchase_d is None):                
                #if audit_logs[audit_log_index].token.metadivision_id and audit_logs[audit_log_index+1].token.metadivision_id is None:
                super_short_audit_log_list.append(audit_logs[audit_log_index])
                audit_log_index=audit_log_index+1
                continue
            audit_log_index=audit_log_index+1
        else:
            super_short_audit_log_list.append(audit_logs[audit_log_index])            
            audit_log_index=audit_log_index+1

    audit_log_index = 0    
    while audit_log_index < len(super_short_audit_log_list):        
        audit_log=super_short_audit_log_list[audit_log_index]
        if audit_log.division_machine_id: 
            machine_name=division_machines[audit_log.division_machine_id]['division_machine_name']                    
        if audit_log.purchase_date is not None:
            if audit_log.token.metadivision_id:
            #while audit_log_index < len(audit_logs) and audit_logs[audit_log_index+1].purchase_date and audit_logs[audit_log_index+1].token.metadivision_id:
                #audit_log_index=audit_log_index+1
                #audit_log_index=audit_log_index-1
                #audit_log=audit_logs[audit_log_index]
                div_string = " for metadivision %s" % metadivisions[audit_log.token.metadivision_id]['meta_division_name']
            else:
                #while audit_log_index < len(audit_logs) and audit_logs[audit_log_index+1].purchase_date and audit_logs[audit_log_index+1].token.division_id:                    
                #    audit_log_index=audit_log_index+1
                #audit_log_index=audit_log_index-1
                #audit_log=audit_logs[audit_log_index]                
                div_string = " for division %s" % divisions[audit_log.token.division_id]['tournament_name']
                
            audit_log_list.append(
                "Purchased on %s - %s - sold by %s - number purchased : %s, remaining tokens : %s " % (audit_log.purchase_date,div_string, users[audit_log.deskworker_id]['username'],audit_log.num_tokens_purchased_in_batch, audit_log.remaining_tokens)
            )
        if audit_log.game_started_date is not None:            
            audit_log_list.append(
                "Game started on %s - %s %s - by %s - remaining tokens : %s " % (audit_log.game_started_date,machine_name,div_string,users[audit_log.scorekeeper_id]['username'],audit_log.remaining_tokens)
            )
        if audit_log.voided_date is not None:            
            audit_log_list.append(
                "Game voided on %s - %s %s - by %s - remaining tokens : %s " % (audit_log.voided_date,machine_name,div_string,users[audit_log.scorekeeper_id]['username'],audit_log.remaining_tokens)
            )
        if audit_log.used_date is not None:            
            audit_log_list.append(
                "Game score (%s) submitted on %s - %s %s - by %s - remaining tokens : %s " % (audit_log.entry.scores[0].score,audit_log.used_date,machine_name,div_string,users[audit_log.scorekeeper_id]['username'],audit_log.remaining_tokens)
            )
        audit_log_index=audit_log_index+1
        
    return jsonify({'data':audit_log_list})
