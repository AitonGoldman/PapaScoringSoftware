def generate_finals_matches_class(db_handle):
    class FinalsMatches(db_handle.Model):        
        finals_match_id=db_handle.Column(db_handle.Integer, primary_key=True)
        tournament_id=db_handle.Column('tournament_id', db_handle.Integer, db_handle.ForeignKey('tournaments.tournament_id'))        
        final_id=db_handle.Column('final_id', db_handle.Integer, db_handle.ForeignKey('finals.final_id'))
        machine_1=db_handle.Column(db_handle.String(100))
        machine_2=db_handle.Column(db_handle.String(100))
        machine_3=db_handle.Column(db_handle.String(100))        
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
        player_one_score_1=db_handle.Column(db_handle.Integer)
        player_one_score_2=db_handle.Column(db_handle.Integer)
        player_one_score_3=db_handle.Column(db_handle.Integer)        

        player_one_winner=db_handle.Column(db_handle.Boolean)
                
        player_one_points_1=db_handle.Column(db_handle.Integer)
        player_one_points_2=db_handle.Column(db_handle.Integer)
        player_one_points_3=db_handle.Column(db_handle.Integer)
        
        player_one_order_1=db_handle.Column(db_handle.Integer)
        player_one_order_2=db_handle.Column(db_handle.Integer)
        player_one_order_3=db_handle.Column(db_handle.Integer)
        
        player_two_rank=db_handle.Column(db_handle.Integer)        
        player_two_finals_player_id=db_handle.Column('player_two_finals_player_id', db_handle.Integer, db_handle.ForeignKey('finals_players.finals_player_id'))
        player_two_name=db_handle.Column(db_handle.String(100))                

        player_two_score_1=db_handle.Column(db_handle.Integer)
        player_two_score_2=db_handle.Column(db_handle.Integer)
        player_two_score_3=db_handle.Column(db_handle.Integer)        

        player_two_winner=db_handle.Column(db_handle.Boolean)                

        player_two_points_1=db_handle.Column(db_handle.Integer)
        player_two_points_2=db_handle.Column(db_handle.Integer)
        player_two_points_3=db_handle.Column(db_handle.Integer)
        
        player_two_order_1=db_handle.Column(db_handle.Integer)
        player_two_order_2=db_handle.Column(db_handle.Integer)
        player_two_order_3=db_handle.Column(db_handle.Integer)
        
        player_three_rank=db_handle.Column(db_handle.Integer)        
        player_three_finals_player_id=db_handle.Column('player_three_finals_player_id', db_handle.Integer, db_handle.ForeignKey('finals_players.finals_player_id'))
        player_three_name=db_handle.Column(db_handle.String(100))                                
        player_three_score_1=db_handle.Column(db_handle.Integer)
        player_three_score_2=db_handle.Column(db_handle.Integer)
        player_three_score_3=db_handle.Column(db_handle.Integer)        

        player_three_winner=db_handle.Column(db_handle.Boolean)                

        player_three_points_1=db_handle.Column(db_handle.Integer)
        player_three_points_2=db_handle.Column(db_handle.Integer)
        player_three_points_3=db_handle.Column(db_handle.Integer)
        
        player_three_order_1=db_handle.Column(db_handle.Integer)
        player_three_order_2=db_handle.Column(db_handle.Integer)
        player_three_order_3=db_handle.Column(db_handle.Integer)

        player_three_rank=db_handle.Column(db_handle.Integer)                
        player_four_finals_player_id=db_handle.Column('player_four_finals_player_id', db_handle.Integer, db_handle.ForeignKey('finals_players.finals_player_id'))
        player_four_name=db_handle.Column(db_handle.String(100))                                
        player_four_score_1=db_handle.Column(db_handle.Integer)
        player_four_score_2=db_handle.Column(db_handle.Integer)
        player_four_score_3=db_handle.Column(db_handle.Integer)        

        player_four_rank=db_handle.Column(db_handle.Integer)                        
        player_four_winner=db_handle.Column(db_handle.Boolean)                

        player_four_points_1=db_handle.Column(db_handle.Integer)
        player_four_points_2=db_handle.Column(db_handle.Integer)
        player_four_points_3=db_handle.Column(db_handle.Integer)
        
        player_four_order_1=db_handle.Column(db_handle.Integer)
        player_four_order_2=db_handle.Column(db_handle.Integer)
        player_four_order_3=db_handle.Column(db_handle.Integer)        

        
        machine_4=db_handle.Column(db_handle.String(100))
        player_4_order_4=db_handle.Column(db_handle.Integer)
        player_3_order_4=db_handle.Column(db_handle.Integer)
        player_2_order_4=db_handle.Column(db_handle.Integer)
        player_1_order_4=db_handle.Column(db_handle.Integer)
        player_four_points_4=db_handle.Column(db_handle.Integer)
        player_three_points_4=db_handle.Column(db_handle.Integer)
        player_two_points_4=db_handle.Column(db_handle.Integer)
        player_one_points_4=db_handle.Column(db_handle.Integer)                                
        player_one_score_4=db_handle.Column(db_handle.BigInteger)        
        player_two_score_4=db_handle.Column(db_handle.BigInteger)        
        player_three_score_4=db_handle.Column(db_handle.BigInteger)        
        player_four_score_4=db_handle.Column(db_handle.BigInteger)        
        four_completed=db_handle.Column(db_handle.Boolean)        
    return FinalsMatches
