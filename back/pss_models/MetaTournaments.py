def generate_meta_tournaments_class(db_handle,event_name):
    class MetaTournaments(db_handle.Model):        
        # pylint: disable=no-init
        # pylint can't find SQLAlchemy's __init__() method for some reason        
        __tablename__="meta_tournaments_"+event_name                
        meta_tournament_id=db_handle.Column(db_handle.Integer, primary_key=True)
        meta_tournament_name=db_handle.Column(db_handle.String(100))
        minimum_number_of_tickets_allowed=db_handle.Column(db_handle.Integer,default=1)
        number_of_unused_tickets_allowed=db_handle.Column(db_handle.Integer,default=15)
        ticket_increment_for_each_purchase=db_handle.Column(db_handle.Integer,default=1)
        number_of_tickets_for_discount=db_handle.Column(db_handle.Integer)
        use_stripe=db_handle.Column(db_handle.Boolean,default=False)
        stripe_sku=db_handle.Column(db_handle.String(100))
        discount_stripe_sku=db_handle.Column(db_handle.String(100))
        stripe_price=db_handle.Column(db_handle.Float)
        discount_stripe_price=db_handle.Column(db_handle.Float)
        manually_set_price=db_handle.Column(db_handle.Float,default=15.0)
        discount_price=db_handle.Column(db_handle.Integer)
        
    return MetaTournaments



