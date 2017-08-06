"""Model object for a Events"""
def generate_events_class(db_handle):
    class Events(db_handle.Model):
        """Model object for Events"""
        # pylint: disable=no-init
        # pylint can't find SQLAlchemy's __init__() method for some reason
        role_id = db_handle.Column(db_handle.Integer, primary_key=True)
        name = db_handle.Column(db_handle.String(100))
    return Events
    
