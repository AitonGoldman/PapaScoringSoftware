def generate_tokens_class(db_handle,event_name):
    class Tokens(db_handle.Model):        
        # pylint: disable=no-init
        # pylint can't find SQLAlchemy's __init__() method for some reason        
        __tablename__="tokens_"+event_name                
        token_id=db_handle.Column(db_handle.Integer, primary_key=True)        
        used=db_handle.Column(db_handle.Boolean,default=False)        
        deleted=db_handle.Column(db_handle.Boolean,default=False)        
        voided=db_handle.Column(db_handle.Boolean,default=False)
        paid_for=db_handle.Column(db_handle.Boolean,default=False)
        comped=db_handle.Column('comped',db_handle.Boolean,default=False)        
        player_id=db_handle.Column('player_id', db_handle.Integer, db_handle.ForeignKey('players.player_id'))
        team_id=db_handle.Column('team_id', db_handle.Integer, db_handle.ForeignKey('teams_'+event_name+'.team_id'))        
        tournament_id=db_handle.Column('tournament_id', db_handle.Integer, db_handle.ForeignKey('tournaments_'+event_name+'.tournament_id'))
        meta_tournament_id=db_handle.Column('meta_tournament_id', db_handle.Integer, db_handle.ForeignKey('meta_tournaments_'+event_name+'.meta_tournament_id'))
        token_purchase_id=db_handle.Column('token_purchase_id', db_handle.Integer, db_handle.ForeignKey('token_purchases_'+event_name+'.token_purchase_id'))                
    return Tokens
    
