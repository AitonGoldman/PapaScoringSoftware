from flask_restless.helpers import to_dict

def generate_finals_match_player_result_class(db_handle,relationship=None,fk=None):    
    class FinalsMatchPlayerResult(db_handle.Model):        
        finals_match_player_result_id = db_handle.Column(db_handle.Integer, primary_key=True)
        division_final_match_id = db_handle.Column(db_handle.Integer,db_handle.ForeignKey('division_final_match.division_final_match_id'))
        papa_points_sum = db_handle.Column(db_handle.Integer)
        needs_tiebreaker = db_handle.Column(db_handle.Boolean,default=False)
        won_tiebreaker = db_handle.Column(db_handle.Boolean)
        winner = db_handle.Column(db_handle.Boolean)
        finals_player_id = db_handle.Column(db_handle.Integer,db_handle.ForeignKey('finals_player.finals_player_id'))

        #finals_match_game_results = db_handle.relationship('FinalsMatchGameResults')
 
        
        def to_dict_simple(self):
            export_dict = to_dict(self)
            # if len(self.qualifiers) > 0:
            #     division_final_dict = []
            #     for qualifier in self.qualifiers:
            #         division_final_dict.append(qualifier.to_dict_simple())
            return export_dict
        
    return FinalsMatchPlayerResult
