from flask_restless.helpers import to_dict

def generate_finals_player_class(db_handle,relationship=None,fk=None):    
    class FinalsPlayer(db_handle.Model):        
        finals_player_id = db_handle.Column(db_handle.Integer, primary_key=True)
        division_final_id = db_handle.Column(db_handle.Integer,
                                             db_handle.ForeignKey(
                                                 'division_final.division_final_id'))
        player_id = db_handle.Column(db_handle.Integer,
                                     db_handle.ForeignKey(
                                         'player.player_id'))
                
        initial_seed = db_handle.Column(db_handle.Integer)
        overall_rank = db_handle.Column(db_handle.Integer)

        def to_dict_simple(self):
            return to_dict(self)        
        
    return FinalsPlayer
