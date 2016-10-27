"""Model object for a role"""
from flask_restless.helpers import to_dict

def generate_role_class(db_handle):
    class Role(db_handle.Model):
        """Model object for a role"""
        # pylint: disable=no-init
        # pylint can't find SQLAlchemy's __init__() method for some reason
        role_id = db_handle.Column(db_handle.Integer, primary_key=True)
        name = db_handle.Column(db_handle.String(100))

        def to_dict_simple(self):
            return to_dict(self)
    return Role
