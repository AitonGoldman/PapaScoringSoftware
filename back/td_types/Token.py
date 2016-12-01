from flask_restless.helpers import to_dict
import datetime

def generate_token_class(db_handle):
    class Token(db_handle.Model):
        token_id = db_handle.Column(db_handle.Integer, primary_key=True)
        team_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'team.team_id'
        ))
        player_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'player.player_id'
        ))
        division_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'division.division_id'
        ))
        metadivision_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'meta_division.meta_division_id'
        ))
        deskworker_id = db_handle.Column('deskworker_id', db_handle.Integer, db_handle.ForeignKey('user.user_id'))
        scorekeeper_id = db_handle.Column('scorekeeper_id', db_handle.Integer, db_handle.ForeignKey('user.user_id'))
        purchase_date = db_handle.Column(db_handle.DateTime,default=datetime.datetime.now)
        game_started_date = db_handle.Column(db_handle.DateTime)
        used_date = db_handle.Column(db_handle.DateTime)
        paid_for = db_handle.Column(db_handle.Boolean,default=False)
        used = db_handle.Column(db_handle.Boolean,default=False)
        comped = db_handle.Column(db_handle.Boolean,default=False)
        division_machine_id = db_handle.Column('division_machine_id', db_handle.Integer, db_handle.ForeignKey('division_machine.division_machine_id'))
        voided = db_handle.Column(db_handle.Boolean,default=False)
        def to_dict_simple(self):
            return to_dict(self)        
    return Token
