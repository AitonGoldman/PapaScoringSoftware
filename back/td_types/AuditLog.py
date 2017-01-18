from flask_restless.helpers import to_dict
import datetime

def generate_audit_log_class(db_handle):
    class AuditLog(db_handle.Model):
        audit_log_id = db_handle.Column(db_handle.Integer, primary_key=True)        
        player_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'player.player_id'
        ))
        team_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'team.team_id'
        ))        
        entry_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'entry.entry_id'
        ))
        token_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'token.token_id'
        ))
        division_machine_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'division_machine.division_machine_id'
        ))        
        user_id = db_handle.Column('deskworker_id', db_handle.Integer, db_handle.ForeignKey('user.user_id'))
        action_date = db_handle.Column(db_handle.DateTime)
        description = db_handle.Column(db_handle.String(255))
        amount = db_handle.Column(db_handle.Integer)
        action=db_handle.Column(db_handle.String(255))
        division_machine = db_handle.relationship(
            'DivisionMachine',
            foreign_keys=[division_machine_id]
        )
        token = db_handle.relationship(
            'Token',
            foreign_keys=[token_id]
        )
        entry = db_handle.relationship(
            'Entry',
            foreign_keys=[entry_id]
        )        
        
        
        def to_dict_simple(self):
            return to_dict(self)        
    return AuditLog
