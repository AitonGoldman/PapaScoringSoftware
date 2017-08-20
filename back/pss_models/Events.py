"""Model object for a Events"""
def generate_events_class(db_handle):
    class Events(db_handle.Model):
        """Model object for Events"""
        # pylint: disable=no-init
        # pylint can't find SQLAlchemy's __init__() method for some reason
        event_id = db_handle.Column(db_handle.Integer, primary_key=True)
        name = db_handle.Column(db_handle.String(100))
        queue_bump_amount = db_handle.Column(db_handle.Integer)
        stripe_api_key = db_handle.Column(db_handle.String(100))
        stripe_public_key = db_handle.Column(db_handle.String(100))
        number_unused_tickets_allowed = db_handle.Column(db_handle.Integer)
        ionic_profile = db_handle.Column(db_handle.String(100))
        ionic_api_key = db_handle.Column(db_handle.String(100))
        active = db_handle.Column(db_handle.Boolean)
        flask_secret_key = db_handle.Column(db_handle.String(100))
        sendgrid_api_key = db_handle.Column(db_handle.String(100))
        player_id_seq_start = db_handle.Column(db_handle.Integer)
        upload_folder = db_handle.Column(db_handle.String(100))
        ifpa_api_key=db_handle.Column(db_handle.String(100))
    return Events
    
