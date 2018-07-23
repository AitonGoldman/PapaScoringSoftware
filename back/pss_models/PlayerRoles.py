"""Model object for a event role"""
def generate_player_roles_class(db_handle):
    class PlayerRoles(db_handle.Model):
        """Model object for a role"""
        # pylint: disable=no-init
        # pylint can't find SQLAlchemy's __init__() method for some reason
        player_role_id = db_handle.Column(db_handle.Integer, primary_key=True)
        name = db_handle.Column(db_handle.String(100))
    return PlayerRoles
