def generate_tiebreaker_players_class(db_handle):
    class TiebreakerPlayers(db_handle.Model):        
        tiebreaker_player_id=db_handle.Column(db_handle.Integer, primary_key=True)
        finals_player_id=db_handle.Column(db_handle.Integer, db_handle.ForeignKey('finals_players.finals_player_id'))
        tiebreaker_id=db_handle.Column(db_handle.Integer, db_handle.ForeignKey('tiebreakers.tiebreaker_id'))
        player_id=db_handle.Column('player_id', db_handle.Integer, db_handle.ForeignKey('players.player_id'))        
        player_name=db_handle.Column(db_handle.String(100))        
        # rank after tiebreaker
        score=db_handle.Column(db_handle.Integer)
        winner=db_handle.Column(db_handle.Boolean)        
    return TiebreakerPlayers
