from flask_restless.helpers import to_dict

def generate_finals_match_game_player_result_class(db_handle,relationship=None,fk=None):    
    class FinalsMatchGamePlayerResult(db_handle.Model):        
        finals_match_game_player_result_id = db_handle.Column(db_handle.Integer, primary_key=True)
        finals_match_game_result_id = db_handle.Column(db_handle.Integer,db_handle.ForeignKey('finals_match_game_result.finals_match_game_result_id'))
        papa_points = db_handle.Column(db_handle.Integer)
        score = db_handle.Column(db_handle.Integer)
        play_order = db_handle.Column(db_handle.Integer)
        finals_player_id = db_handle.Column(db_handle.Integer,db_handle.ForeignKey('finals_player.finals_player_id'))

        finals_player = db_handle.relationship('FinalsPlayer')
 
        
        def to_dict_simple(self):
            export_dict = to_dict(self)
            if self.finals_player:
                export_dict['final_player']=self.finals_player.to_dict_simple()
            else:
                export_dict['final_player']={}
                
            # if len(self.qualifiers) > 0:
            #     division_final_dict = []
            #     for qualifier in self.qualifiers:
            #         division_final_dict.append(qualifier.to_dict_simple())
            return export_dict
        
    return FinalsMatchGamePlayerResult
