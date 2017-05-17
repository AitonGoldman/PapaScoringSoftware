from flask_restless.helpers import to_dict

def generate_division_final_match_game_player_result_class(db_handle,relationship=None,fk=None):    
    class DivisionFinalMatchGamePlayerResult(db_handle.Model):        
        division_final_match_game_player_result_id = db_handle.Column(db_handle.Integer, primary_key=True)
        division_final_match_game_result_id = db_handle.Column(db_handle.Integer,db_handle.ForeignKey('division_final_match_game_result.division_final_match_game_result_id'))
        papa_points = db_handle.Column(db_handle.Integer)
        score = db_handle.Column(db_handle.BIGINT)
        play_order = db_handle.Column(db_handle.Integer)
        final_player_id = db_handle.Column(db_handle.Integer,db_handle.ForeignKey('division_final_player.final_player_id'))

        final_player = db_handle.relationship('DivisionFinalPlayer',cascade="all, delete, delete-orphan",single_parent=True)
 
        
        def to_dict_simple(self):
            export_dict = to_dict(self)
            if self.final_player:
                export_dict['final_player']=self.final_player.to_dict_simple()
            else:
                export_dict['final_player']={}
                
            # if len(self.qualifiers) > 0:
            #     division_final_dict = []
            #     for qualifier in self.qualifiers:
            #         division_final_dict.append(qualifier.to_dict_simple())
            return export_dict
        
    return DivisionFinalMatchGamePlayerResult
