from util import db_util
from flask import current_app
import datetime
import json
import routes.utils

def create_audit_log_ex(app, action,user_id, player_id=None,division_machine_id=None,team_id=None,generic_json_data=None,commit=True,summary=False,description=None):
    actions_to_add_ticket_summary_to = ["Score Recorded","Ticket Purchase","Player Ticket Purchase Complete"]
    db = db_util.app_db_handle(app)
    tables = db_util.app_db_tables(app)                
    audit_log_ex = tables.AuditLogEx()
    audit_log_ex.action=action
    audit_log_ex.action_date=datetime.datetime.now()    
    if user_id:
        audit_log_ex.user_id=user_id
        user = routes.utils.fetch_entity(tables.User,user_id)
        if user.is_player:
            audit_log_ex.player_initiated=True
    if player_id:
        audit_log_ex.player_id=player_id
    if team_id:
        audit_log_ex.team_id=team_id        
    if division_machine_id:
        audit_log_ex.division_machine_id=division_machine_id
    if generic_json_data:                
        generic_string = ",".join(["%s : %s"%(key,value) for key,value in generic_json_data.iteritems()])
        audit_log_ex.generic_json_data=generic_string        
    if summary:
        audit_log_ex.summary=True
    if description:
        audit_log_ex.description=description
    db.session.add(audit_log_ex)
    if commit is True:
        db.session.commit()
    if action not in actions_to_add_ticket_summary_to:
        return
    if player_id:
        tokens_left_info = routes.utils.calc_audit_log_remaining_tokens(player_id,return_string=False)
        tokens_left_string = tokens_left_info['tokens_left_string']        
    
    audit_log_ticket_summary_ex = tables.AuditLogEx()
    audit_log_ticket_summary_ex.action="Ticket Summary"
    audit_log_ticket_summary_ex.action_date=datetime.datetime.now()
    if user_id:
        audit_log_ex.user_id=user_id            
    if player_id:
        audit_log_ticket_summary_ex.player_id=player_id    
    audit_log_ticket_summary_ex.generic_json_data=tokens_left_string
    audit_log_ticket_summary_ex.summary=True
    db.session.add(audit_log_ticket_summary_ex)
    if commit is True:
        db.session.commit()
    

def create_audit_log(action,action_date,description,user_id=None,
                     player_id=None,team_id=None,division_machine_id=None,
                     entry_id=None,token_id=None,amount=None,commit=True):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)                
    audit_log = tables.AuditLog()
    audit_log.action=action
    audit_log.action_date=action_date
    audit_log.description=description
    if user_id:
        audit_log.user_id=user_id
    if player_id:
        audit_log.player_id=player_id
    if team_id:
        audit_log.team_id=team_id
    if division_machine_id:
        audit_log.division_machine_id=division_machine_id
    if entry_id:
        audit_log.entry_id=entry_id
    if token_id:
        audit_log.token_id=token_id
    if amount:
        audit_log.amount=amount
    db.session.add(audit_log)
    if commit is True:
        db.session.commit()
