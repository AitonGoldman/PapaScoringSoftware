from flask_restless.helpers import to_dict
        
def generate_tournament_class(db_handle):
    class Tournament(db_handle.Model):
        """Model object for a tournament"""
        # pylint: disable=no-init
        # pylint can't find SQLAlchemy's __init__() method for some reason
        tournament_id = db_handle.Column(db_handle.Integer, primary_key=True)
        team_tournament = db_handle.Column(db_handle.Boolean)
        tournament_name = db_handle.Column(db_handle.String(1000))
        active = db_handle.Column(db_handle.Boolean)
        single_division = db_handle.Column(db_handle.Boolean)        
        scoring_type = db_handle.Column(db_handle.String(100))
        start_date = db_handle.Column(db_handle.DateTime)
        end_date = db_handle.Column(db_handle.DateTime)
        divisions = db_handle.relationship('Division',lazy='joined')


        def to_dict_simple(self):
            return to_dict(self)
    return Tournament
    
