def generate_tiebreakers_class(db_handle):
    class Tiebreakers(db_handle.Model):        
        tiebreaker_id=db_handle.Column(db_handle.Integer, primary_key=True)
        tournament_id=db_handle.Column(db_handle.Integer, db_handle.ForeignKey('tournaments.tournament_id'))
        rank_of_winners=db_handle.Column(db_handle.Integer)
        rank_of_losers=db_handle.Column(db_handle.Integer)
        number_of_winners=db_handle.Column(db_handle.Integer)
        ppo_a_b_boundry=db_handle.Column(db_handle.Boolean,default=False)
        completed=db_handle.Column(db_handle.Boolean,default=False)
        round=db_handle.Column(db_handle.Integer)
    return Tiebreakers
