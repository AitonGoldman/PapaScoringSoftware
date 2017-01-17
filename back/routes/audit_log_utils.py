from util import db_util
from flask import current_app

def create_audit_log(action,action_date,description,user_id=None,
                     player_id=None,team_id=None,division_machine_id=None,
                     entry_id=None,token_id=None):
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
    db.session.add(audit_log)
    db.session.commit()
