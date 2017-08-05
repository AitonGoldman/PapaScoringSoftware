from flask_restless.helpers import to_dict

def generate_division_final_player_class(db_handle,relationship=None,fk=None):    
    class DivisionFinalPlayer(db_handle.Model):        
        final_player_id = db_handle.Column(db_handle.Integer, primary_key=True)
        division_final_id = db_handle.Column(db_handle.Integer,
                                             db_handle.ForeignKey(
                                                 'division_final.division_final_id'))
        player_id = db_handle.Column(db_handle.Integer,
                                     db_handle.ForeignKey(
                                         'player.player_id'))
        team_id = db_handle.Column(db_handle.Integer,
                                     db_handle.ForeignKey(
                                         'team.team_id'))        
        adjusted_seed = db_handle.Column(db_handle.Integer)
        initial_seed = db_handle.Column(db_handle.Integer)
        overall_rank = db_handle.Column(db_handle.Integer)
        player_name = db_handle.Column(db_handle.String(100))
        removed = db_handle.Column(db_handle.Boolean)
        division_final = db_handle.relationship('DivisionFinal')
        player = db_handle.relationship('Player')
        team = db_handle.relationship('Team')                
        def to_dict_simple(self):
            export_dict = to_dict(self)
            if self.player:
                export_dict['player']=self.player.to_dict_simple()
            if self.team:
                export_dict['player']=self.team.to_dict_simple()
                export_dict['player']['full_name']=self.team.team_name
            return export_dict
        
    return DivisionFinalPlayer
