from flask_restless.helpers import to_dict

def generate_finals_match_game_result_class(db_handle,relationship=None,fk=None):    
    class FinalsMatchGameResult(db_handle.Model):        
        finals_match_game_result_id = db_handle.Column(db_handle.Integer, primary_key=True)
        division_final_match_id = db_handle.Column(db_handle.Integer,db_handle.ForeignKey('division_final_match.division_final_match_id'))
        division_machine_id = db_handle.Column(db_handle.Integer,db_handle.ForeignKey('division_machine.division_machine_id'))
        division_machine = db_handle.relationship('DivisionMachine')
        completed = db_handle.Column(db_handle.Boolean,default=False)
        finals_match_game_player_results = db_handle.relationship('FinalsMatchGamePlayerResult')
 
        
        def to_dict_simple(self):
            export_dict = to_dict(self)
            if len(self.finals_match_game_player_results) > 0:
                export_dict['finals_match_game_player_results'] = []
                for result in self.finals_match_game_player_results:
                    export_dict['finals_match_game_player_results'].append(result.to_dict_simple())
            return export_dict
        
    return FinalsMatchGameResult
