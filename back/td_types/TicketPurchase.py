from flask_restless.helpers import to_dict
import datetime

def generate_ticket_purchase_class(db_handle):
    class TicketPurchase(db_handle.Model):
        ticket_purchase_id = db_handle.Column(db_handle.Integer, primary_key=True)        
        player_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'player.player_id'
        ))
        division_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'division.division_id'
        ))
        meta_division_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'meta_division.meta_division_id'
        ))                
        user_id = db_handle.Column('deskworker_id', db_handle.Integer, db_handle.ForeignKey('user.user_id'))
        purchase_date = db_handle.Column(db_handle.DateTime)
        description = db_handle.Column(db_handle.String(255))
        amount = db_handle.Column(db_handle.Integer)
        use_stripe = db_handle.Column(db_handle.Boolean,default=False)
        stripe_charge_id = db_handle.Column(db_handle.String(255))
        division = db_handle.relationship(
            'Division',
            foreign_keys=[division_id]
        )
        metadivision = db_handle.relationship(
            'MetaDivision',
            foreign_keys=[meta_division_id]
        )
        
        def to_dict_simple(self):
            return to_dict(self)        
    return TicketPurchase
