from flask_restless.helpers import to_dict

def generate_division_final_match_player_result_class(db_handle,relationship=None,fk=None):    
    class DivisionFinalMatchPlayerResult(db_handle.Model):        
        final_match_player_result_id = db_handle.Column(db_handle.Integer, primary_key=True)
        division_final_match_id = db_handle.Column(db_handle.Integer,db_handle.ForeignKey('division_final_match.division_final_match_id'))
        papa_points_sum = db_handle.Column(db_handle.Integer)
        needs_tiebreaker = db_handle.Column(db_handle.Boolean,default=False)
        won_tiebreaker = db_handle.Column(db_handle.Boolean)
        winner = db_handle.Column(db_handle.Boolean)
        final_player_id = db_handle.Column(db_handle.Integer,db_handle.ForeignKey('division_final_player.final_player_id'))

        final_player = db_handle.relationship('DivisionFinalPlayer',cascade="all, delete, delete-orphan",single_parent=True)
 
        
        def to_dict_simple(self):
            export_dict = to_dict(self)
            if self.final_player:
                export_dict['final_player']=self.final_player.to_dict_simple()
            # if len(self.qualifiers) > 0:
            #     division_final_dict = []
            #     for qualifier in self.qualifiers:
            #         division_final_dict.append(qualifier.to_dict_simple())
            return export_dict
        
    return DivisionFinalMatchPlayerResult
