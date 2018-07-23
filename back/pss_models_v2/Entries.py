from flask_restless.helpers import to_dict

def generate_entries_class(db_handle):    
    class Entries(db_handle.Model):
        """Model object for an entry"""
        # pylint: disable=no-init
        # pylint can't find SQLAlchemy's __init__() method for some reason
        voided = db_handle.Column(db_handle.Boolean, default=False)
        entry_id = db_handle.Column(db_handle.Integer, primary_key=True)
        player_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'players.player_id'
        ))
        event_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'events.event_id'
        ))        
        team_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'teams.team_id'
        ))        
        tournament_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'tournaments.tournament_id'
        ))
        
    return Entries
