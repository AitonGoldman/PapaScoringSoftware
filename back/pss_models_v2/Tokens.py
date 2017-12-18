def generate_tokens_class(db_handle):
    class Tokens(db_handle.Model):        
        # pylint: disable=no-init
        # pylint can't find SQLAlchemy's __init__() method for some reason                
        token_id=db_handle.Column(db_handle.Integer, primary_key=True)        
        used=db_handle.Column(db_handle.Boolean,default=False)        
        deleted=db_handle.Column(db_handle.Boolean,default=False)        
        voided=db_handle.Column(db_handle.Boolean,default=False)
        paid_for=db_handle.Column(db_handle.Boolean,default=False)
        comped=db_handle.Column('comped',db_handle.Boolean,default=False)        
        player_id=db_handle.Column('player_id', db_handle.Integer, db_handle.ForeignKey('players.player_id'))
        team_id=db_handle.Column('team_id', db_handle.Integer, db_handle.ForeignKey('teams.team_id'))        
        tournament_id=db_handle.Column('tournament_id', db_handle.Integer, db_handle.ForeignKey('tournaments.tournament_id'))
        meta_tournament_id=db_handle.Column('meta_tournament_id', db_handle.Integer, db_handle.ForeignKey('meta_tournaments.meta_tournament_id'))
        token_purchase_id=db_handle.Column('token_purchase_id', db_handle.Integer, db_handle.ForeignKey('token_purchases.token_purchase_id'))
        event_id=db_handle.Column('event_id', db_handle.Integer, db_handle.ForeignKey('events.event_id'))        
    return Tokens
    
