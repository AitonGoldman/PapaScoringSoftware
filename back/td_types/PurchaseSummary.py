from flask_restless.helpers import to_dict
import datetime

def generate_purchase_summary_class(db_handle):
    class PurchaseSummary(db_handle.Model):
        purchase_summary_id = db_handle.Column(db_handle.Integer, primary_key=True)        
        player_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'player.player_id'
        ))
        purchase_date = db_handle.Column(db_handle.DateTime)
        description = db_handle.Column(db_handle.String(255))
        use_stripe = db_handle.Column(db_handle.Boolean,default=False)
        stripe_charge_id = db_handle.Column(db_handle.String(255))
        ticket_purchase = db_handle.relationship('TicketPurchase')        
        def to_dict_simple(self):
            return to_dict(self)        
    return PurchaseSummary
