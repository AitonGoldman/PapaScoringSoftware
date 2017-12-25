from flask_restless.helpers import to_dict

def generate_scores_class(db_handle):    
    class Scores(db_handle.Model):
        score_id = db_handle.Column(db_handle.Integer, primary_key=True)
        
        score = db_handle.Column(db_handle.BIGINT)            
        
        entry_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'entries.entry_id'
        ))
        player_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'players.player_id'
        ))
        event_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'events.event_id'
        ))
        
        tournament_machine_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'tournament_machines.tournament_machine_id'
        ))
        tournament_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'tournaments.tournament_id'
        ))                                
    return Scores
