from passlib.hash import sha512_crypt

"""Model object for a Pss Event Role mappings"""
def generate_pss_users_event_roles_class(db_handle):
    class PssUsersEventsRoles(db_handle.Model):        
        # pylint: disable=no-init
        # pylint can't find SQLAlchemy's __init__() method for some reason        

        pss_user_id = db_handle.Column('pss_user_id', db_handle.Integer, db_handle.ForeignKey('pss_users.pss_user_id'),primary_key=True,)
        role_id = db_handle.Column('role_id', db_handle.Integer,  db_handle.ForeignKey('roles.role_id'),primary_key=True,)
        event_id = db_handle.Column('event_id', db_handle.Integer, db_handle.ForeignKey('events.event_id'),primary_key=True,)
        role = db_handle.relationship('Roles')
        event = db_handle.relationship('Events')

    return PssUsersEventsRoles
    
