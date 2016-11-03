from flask_restless.helpers import to_dict

def generate_division_class(db_handle,relationship=None,fk=None):    
    class Division(db_handle.Model):
        """Model object for a division in a tournament"""
        # pylint: disable=no-init
        # pylint can't find SQLAlchemy's __init__() method for some reason
        #metadivision_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
        #    'metadivision.metadivision_id'
        #))
        division_id = db_handle.Column(db_handle.Integer, primary_key=True)
        division_name = db_handle.Column(db_handle.String(100))
        number_of_scores_per_entry = db_handle.Column(db_handle.Integer)
        stripe_sku = db_handle.Column(db_handle.String(100))
        local_price = db_handle.Column(db_handle.Integer)
        finals_player_selection_type = db_handle.Column(db_handle.String(100))
        finals_num_qualifiers = db_handle.Column(db_handle.Integer)
        finals_num_qualifiers_ppo_a = db_handle.Column(db_handle.Integer)
        finals_num_qualifiers_ppo_b = db_handle.Column(db_handle.Integer)
        finals_challonge_name_ppo_a = db_handle.Column(db_handle.String(100))
        finals_challonge_name_ppo_b = db_handle.Column(db_handle.String(100))        
        finals_num_players_per_group = db_handle.Column(db_handle.Integer)
        finals_num_games_per_match = db_handle.Column(db_handle.Integer)
                
        tournament_id = db_handle.Column(db_handle.Integer,
                                         db_handle.ForeignKey(
                                             'tournament.tournament_id'
                                         ))
        tournament = db_handle.relationship(
            'Tournament',
            foreign_keys=[tournament_id]
        )
        
        
        def to_dict_simple(self):
            division = to_dict(self)
            division['tournament_name'] = self.get_tournament_name(self.tournament)
            
            return division

        def get_tournament_name(self, tournament):
            if tournament.single_division:
                return tournament.tournament_name
            return tournament.tournament_name+", "+self.division_name

        
        
    return Division
