from flask_restless.helpers import to_dict
import datetime

def generate_audit_log_ex_class(db_handle):
    class AuditLogEx(db_handle.Model):
        audit_log_ex_id = db_handle.Column(db_handle.Integer, primary_key=True)        
        player_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'player.player_id'
        ))
        team_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'team.team_id'
        ))        
        division_machine_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'division_machine.division_machine_id'
        ))        
        user_id = db_handle.Column('deskworker_id', db_handle.Integer, db_handle.ForeignKey('user.user_id'))
        action_date = db_handle.Column(db_handle.DateTime)
        description = db_handle.Column(db_handle.String(255))
        action=db_handle.Column(db_handle.String(255))
        generic_json_data = db_handle.Column(db_handle.String(1000))
        summary=db_handle.Column(db_handle.Boolean,default=False)
        player_initiated=db_handle.Column(db_handle.Boolean,default=False)
        def to_dict_simple(self):
            return to_dict(self)        
    return AuditLogEx
