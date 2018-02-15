def generate_finals_players_class(db_handle):
    class FinalsPlayers(db_handle.Model):        
        finals_player_id=db_handle.Column(db_handle.Integer, primary_key=True)
        player_id=db_handle.Column('player_id', db_handle.Integer, db_handle.ForeignKey('players.player_id'))
        tournament_id=db_handle.Column('tournament_id', db_handle.Integer, db_handle.ForeignKey('tournaments.tournament_id'))        
        player_name=db_handle.Column(db_handle.String(100))
        seed_rank=db_handle.Column(db_handle.Integer)
        ppo_b_seed_rank=db_handle.Column(db_handle.Integer)
        finals_rank=db_handle.Column(db_handle.Integer)
        finishing_rank=db_handle.Column(db_handle.Integer)
        
    return FinalsPlayers
