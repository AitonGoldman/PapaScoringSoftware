from flask_restless.helpers import to_dict

def generate_entry_class(db_handle):    
    class Entry(db_handle.Model):
        """Model object for an entry"""
        # pylint: disable=no-init
        # pylint can't find SQLAlchemy's __init__() method for some reason
        voided = db_handle.Column(db_handle.Boolean, default=False)
        entry_id = db_handle.Column(db_handle.Integer, primary_key=True)
        player_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'player.player_id'
        ))
        team_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'team.team_id'
        ))
        
        division_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'division.division_id'
        ))
        division = db_handle.relationship(
            'Division',
            backref=db_handle.backref('entries'),
            foreign_keys=[division_id]
        )    
        player = db_handle.relationship(
            'Player',
            backref=db_handle.backref('entries'),
            foreign_keys=[player_id]
        )
        team = db_handle.relationship(
            'Team',
            backref=db_handle.backref('entries'),        
            foreign_keys=[team_id]
        )    
        
        scores = db_handle.relationship("Score",
                                 lazy='joined'
        )
        
        def to_dict_simple(self):
            entry_dict = to_dict(self)
            if self.scores:
                entry_dict['score']=self.scores[0].to_dict_simple()
            return entry_dict        
        
    return Entry
