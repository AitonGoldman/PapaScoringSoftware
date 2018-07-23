def generate_token_purchase_summaries_class(db_handle):
    class TokenPurchaseSummaries(db_handle.Model):        
        # pylint: disable=no-init
        # pylint can't find SQLAlchemy's __init__() method for some reason                
        token_purchase_summary_id=db_handle.Column(db_handle.Integer, primary_key=True)        
        token_purchase_id=db_handle.Column('token_purchase_id', db_handle.Integer, db_handle.ForeignKey('token_purchases.token_purchase_id'))
        tournament_id=db_handle.Column('tournament_id', db_handle.Integer, db_handle.ForeignKey('tournaments.tournament_id'))
        meta_tournament_id=db_handle.Column('meta_tournament_id', db_handle.Integer, db_handle.ForeignKey('meta_tournaments.meta_tournament_id'))
        
        token_count=db_handle.Column(db_handle.Integer)        
        
    return TokenPurchaseSummaries
    
