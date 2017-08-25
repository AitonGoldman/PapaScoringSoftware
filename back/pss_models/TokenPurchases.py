def generate_token_purchases_class(db_handle,event_name):
    class TokenPurchases(db_handle.Model):        
        # pylint: disable=no-init
        # pylint can't find SQLAlchemy's __init__() method for some reason        
        __tablename__="token_purchases_"+event_name
        token_purchase_id=db_handle.Column(db_handle.Integer, primary_key=True)        
        number_of_discount_tokens_in_purchase=db_handle.Column(db_handle.Integer)
        number_of_normal_tokens_in_purchase=db_handle.Column(db_handle.Integer)
        stripe_purchase=db_handle.Column(db_handle.Boolean,default=False)
        completed_purchase=db_handle.Column(db_handle.Boolean,default=False)
        stripe_transaction_id = db_handle.Column(db_handle.String(180))
        tokens = db_handle.relationship('Tokens')
        total_cost = db_handle.Column(db_handle.Integer)
        token_purchase_summaries = db_handle.relationship('TokenPurchaseSummaries')
    return TokenPurchases
    
