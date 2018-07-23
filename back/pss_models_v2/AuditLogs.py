import datetime

def generate_audit_logs_class(db_handle):
    class AuditLogs(db_handle.Model):        
        audit_log_id = db_handle.Column(db_handle.Integer, primary_key=True)        
        player_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'players.player_id'
        ))
        team_id = db_handle.Column('team_id', db_handle.Integer, db_handle.ForeignKey('teams.team_id'))
        event_id = db_handle.Column('event_id', db_handle.Integer, db_handle.ForeignKey('events.event_id'))
        tournament_machine_id = db_handle.Column('tournament_machine_id', db_handle.Integer, db_handle.ForeignKey('tournament_machines.tournament_machine_id'))
        pss_user_id = db_handle.Column('pss_user_id', db_handle.Integer, db_handle.ForeignKey('pss_users.pss_user_id'))
        action_date = db_handle.Column(db_handle.DateTime)
        description = db_handle.Column(db_handle.String(255))
        action=db_handle.Column(db_handle.String(255))
        generic_json_data = db_handle.Column(db_handle.String(1000))
        summary=db_handle.Column(db_handle.Boolean,default=False)
        player_initiated=db_handle.Column(db_handle.Boolean,default=False)
    return AuditLogs
