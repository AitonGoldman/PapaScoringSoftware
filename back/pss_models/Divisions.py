def generate_divisions_class(db_handle,event_name):
    class Divisions(db_handle.Model):        
        # pylint: disable=no-init
        # pylint can't find SQLAlchemy's __init__() method for some reason        
        __tablename__="divisions_"+event_name                
        division_id=db_handle.Column(db_handle.Integer, primary_key=True)
        division_name=db_handle.Column(db_handle.String(100))
        tournament_name=db_handle.Column(db_handle.String(100))
        tournament_id=db_handle.Column('tournament_id', db_handle.Integer, db_handle.ForeignKey('tournaments_'+event_name+'.tournament_id'))
        
        queuing=db_handle.Column(db_handle.Boolean,default=False)
        num_spaces_to_bump_player_down_queue=db_handle.Column(db_handle.Integer,default=1)

        use_stripe=active=db_handle.Column(db_handle.Boolean,default=False)
        stripe_sku=db_handle.Column(db_handle.String(100))
        discount_stripe_sku=db_handle.Column(db_handle.String(100))
        stripe_price=db_handle.Column(db_handle.Float)
        discount_stripe_price=db_handle.Column(db_handle.Float)
        manually_set_price=db_handle.Column(db_handle.Float)
        #FIXME : make ticket discounts more flexible
        number_of_tickets_for_discount=db_handle.Column(db_handle.Integer)
        discount_price=db_handle.Column(db_handle.Integer)
        number_of_unused_tickets_allowed=db_handle.Column(db_handle.Integer,default=15)
        
        active=db_handle.Column(db_handle.Boolean,default=False)
        scoring_style=db_handle.Column(db_handle.String(100),default="HERB")
        limited_herb=db_handle.Column(db_handle.Boolean,default=False)
        number_of_signifigant_scores=db_handle.Column(db_handle.Integer,default=4)
        ifpa_rank_restriction=db_handle.Column(db_handle.Integer)
        team_tournament=db_handle.Column(db_handle.Boolean,default=False)
        number_players_per_team=db_handle.Column(db_handle.Integer,default=2)
        
        finals_style=db_handle.Column(db_handle.String(100),default="PAPA")
        number_of_qualifiers=db_handle.Column(db_handle.Integer,default=24)
        number_of_qualifiers_for_a_when_finals_style_is_ppo=db_handle.Column(db_handle.Integer,default=12)
        number_of_qualifiers_for_b_when_finals_style_is_ppo=db_handle.Column(db_handle.Integer,default=12)
        number_of_games_played_in_each_finals_match=db_handle.Column(db_handle.Integer,default=3)
        style_of_points_assigned_during_finals=db_handle.Column(db_handle.String(100),default="PAPA")

        division_machines = db_handle.relationship('DivisionMachines')
        tournament = db_handle.relationship('Tournaments',uselist=False)

        allow_desk_purchases = db_handle.Column(db_handle.Boolean,default=True)
        allow_phone_purchases = db_handle.Column(db_handle.Boolean,default=True)
        
    return Divisions
    
