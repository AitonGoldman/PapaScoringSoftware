def generate_finals_matches_class(db_handle):
    class FinalsMatches(db_handle.Model):        
        finals_match_id=db_handle.Column(db_handle.Integer, primary_key=True)
        tournament_id=db_handle.Column('tournament_id', db_handle.Integer, db_handle.ForeignKey('tournaments.tournament_id'))        
        final_id=db_handle.Column('final_id', db_handle.Integer, db_handle.ForeignKey('finals.final_id'))
        machine_one=db_handle.Column(db_handle.String(100))
        machine_two=db_handle.Column(db_handle.String(100))
        machine_three=db_handle.Column(db_handle.String(100))        
        machine_four=db_handle.Column(db_handle.String(100))        
        completed=db_handle.Column(db_handle.Boolean)
        
        one_completed=db_handle.Column(db_handle.Boolean)
        two_completed=db_handle.Column(db_handle.Boolean)
        three_completed=db_handle.Column(db_handle.Boolean)
        
        round=db_handle.Column(db_handle.Integer)
        tiebreaker_id=db_handle.Column('tiebreaker_id', db_handle.Integer, db_handle.ForeignKey('tiebreakers.tiebreaker_id'))
        bye_player_one_finals_player_id=db_handle.Column('bye_player_one_finals_player_id', db_handle.Integer, db_handle.ForeignKey('finals_players.finals_player_id'))
        bye_player_one_name=db_handle.Column(db_handle.String(100))
        bye_player_two_finals_player_id=db_handle.Column('bye_player_two_finals_player_id', db_handle.Integer, db_handle.ForeignKey('finals_players.finals_player_id'))
        bye_player_two_name=db_handle.Column(db_handle.String(100))
        
        
        player_one_rank=db_handle.Column(db_handle.Integer)        
        player_one_finals_player_id=db_handle.Column('player_one_finals_player_id', db_handle.Integer, db_handle.ForeignKey('finals_players.finals_player_id'))
        player_one_name=db_handle.Column(db_handle.String(100))
        player_one_score_one=db_handle.Column(db_handle.Integer)
        player_one_score_two=db_handle.Column(db_handle.Integer)
        player_one_score_three=db_handle.Column(db_handle.Integer)        

        player_one_winner=db_handle.Column(db_handle.Boolean)
                
        player_one_points_one=db_handle.Column(db_handle.Boolean)
        player_one_points_two=db_handle.Column(db_handle.Boolean)
        player_one_points_three=db_handle.Column(db_handle.Boolean)
        
        player_one_order_one=db_handle.Column(db_handle.Integer)
        player_one_order_two=db_handle.Column(db_handle.Integer)
        player_one_order_three=db_handle.Column(db_handle.Integer)
        
        player_two_rank=db_handle.Column(db_handle.Integer)        
        player_two_finals_player_id=db_handle.Column('player_two_finals_player_id', db_handle.Integer, db_handle.ForeignKey('finals_players.finals_player_id'))
        player_two_name=db_handle.Column(db_handle.String(100))                

        player_two_score_one=db_handle.Column(db_handle.Integer)
        player_two_score_two=db_handle.Column(db_handle.Integer)
        player_two_score_three=db_handle.Column(db_handle.Integer)        

        player_two_winner=db_handle.Column(db_handle.Boolean)                

        player_two_points_one=db_handle.Column(db_handle.Boolean)
        player_two_points_two=db_handle.Column(db_handle.Boolean)
        player_two_points_three=db_handle.Column(db_handle.Boolean)
        
        player_two_order_one=db_handle.Column(db_handle.Integer)
        player_two_order_two=db_handle.Column(db_handle.Integer)
        player_two_order_three=db_handle.Column(db_handle.Integer)
        
        player_three_rank=db_handle.Column(db_handle.Integer)        
        player_three_finals_player_id=db_handle.Column('player_three_finals_player_id', db_handle.Integer, db_handle.ForeignKey('finals_players.finals_player_id'))
        player_three_name=db_handle.Column(db_handle.String(100))                                
        player_three_score_one=db_handle.Column(db_handle.Integer)
        player_three_score_two=db_handle.Column(db_handle.Integer)
        player_three_score_three=db_handle.Column(db_handle.Integer)        

        player_three_winner=db_handle.Column(db_handle.Boolean)                

        player_three_points_one=db_handle.Column(db_handle.Boolean)
        player_three_points_two=db_handle.Column(db_handle.Boolean)
        player_three_points_three=db_handle.Column(db_handle.Boolean)
        
        player_three_order_one=db_handle.Column(db_handle.Integer)
        player_three_order_two=db_handle.Column(db_handle.Integer)
        player_three_order_three=db_handle.Column(db_handle.Integer)

        player_three_rank=db_handle.Column(db_handle.Integer)                
        player_four_finals_player_id=db_handle.Column('player_four_finals_player_id', db_handle.Integer, db_handle.ForeignKey('finals_players.finals_player_id'))
        player_four_name=db_handle.Column(db_handle.String(100))                                
        player_four_score_one=db_handle.Column(db_handle.Integer)
        player_four_score_two=db_handle.Column(db_handle.Integer)
        player_four_score_three=db_handle.Column(db_handle.Integer)        

        player_four_winner=db_handle.Column(db_handle.Boolean)                

        player_four_points_one=db_handle.Column(db_handle.Boolean)
        player_four_points_two=db_handle.Column(db_handle.Boolean)
        player_four_points_three=db_handle.Column(db_handle.Boolean)
        
        player_four_order_one=db_handle.Column(db_handle.Integer)
        player_four_order_two=db_handle.Column(db_handle.Integer)
        player_four_order_three=db_handle.Column(db_handle.Integer)

        
        
    return FinalsMatches
