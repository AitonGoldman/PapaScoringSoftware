def generate_meta_tournaments_class(db_handle):
    class MetaTournaments(db_handle.Model):        
        # pylint: disable=no-init
        # pylint can't find SQLAlchemy's __init__() method for some reason                
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
        #tournaments = db_handle.relationship('Tournaments')
        ifpa_rank_restriction=db_handle.Column(db_handle.Integer,default=0)
        team_tournament=db_handle.Column(db_handle.Boolean,default=False)
        event_id=db_handle.Column('event_id', db_handle.Integer, db_handle.ForeignKey('events.event_id'))
        allow_desk_purchases = db_handle.Column(db_handle.Boolean,default=True)
        allow_phone_purchases = db_handle.Column(db_handle.Boolean,default=True)
        has_pic=db_handle.Column(db_handle.Boolean,default=False)
        img_url=db_handle.Column(db_handle.String(100))
        
    return MetaTournaments



