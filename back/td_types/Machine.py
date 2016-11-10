"""Model object for a game machine"""

from flask_restless.helpers import to_dict

def generate_machine_class(db_handle):
    class Machine(db_handle.Model):
        """Model object for a game machine"""
        # pylint: disable=no-init
        # pylint can't find SQLAlchemy's __init__() method for some reason
        machine_id = db_handle.Column(db_handle.Integer, primary_key=True)
        machine_name = db_handle.Column(db_handle.String(1000))
        search_name = db_handle.Column(db_handle.String(1000))
        year = db_handle.Column(db_handle.SmallInteger())
        abbreviation = db_handle.Column(db_handle.String(10))
        
        def to_dict_simple(self):
            return to_dict(self)
        
    return Machine
