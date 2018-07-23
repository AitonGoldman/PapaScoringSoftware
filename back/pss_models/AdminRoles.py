"""Model object for a role"""
def generate_admin_roles_class(db_handle):
    class AdminRoles(db_handle.Model):
        """Model object for a role"""
        # pylint: disable=no-init
        # pylint can't find SQLAlchemy's __init__() method for some reason
        admin_role_id = db_handle.Column(db_handle.Integer, primary_key=True)
        name = db_handle.Column(db_handle.String(100))
        admin_role = db_handle.Column(db_handle.Boolean)
    return AdminRoles
