"""Model object for a team (i.e. splitflipper team)"""

from flask_restless.helpers import to_dict
    
def generate_team_class(db_handle,Team_Player_mapping):
    #Team_Player_mapping = generate_player_team_mapping(db_handle)
    class Team(db_handle.Model):
    #FIXME : tie a team to a specific tournament/division
        team_id = db_handle.Column(db_handle.Integer, primary_key=True)
        team_name = db_handle.Column(db_handle.String(1000))
        players = db_handle.relationship(
            'Player',
            secondary=Team_Player_mapping        
        )
        division_machine = db_handle.relationship('DivisionMachine',                                       
                                                  uselist=False)
    
        def to_dict_simple(self):
            return to_dict(self)
    return Team
