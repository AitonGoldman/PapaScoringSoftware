from passlib.hash import sha512_crypt

"""Model object for a Pss Event Role mappings"""
def generate_pss_event_users_roles_class(db_handle, event_name):
    class EventUsersRoles(db_handle.Model):        
        # pylint: disable=no-init
        # pylint can't find SQLAlchemy's __init__() method for some reason        
        __tablename__="event_users_roles_"+event_name                

        pss_user_id = db_handle.Column('pss_user_id', db_handle.Integer, db_handle.ForeignKey('pss_users.pss_user_id'),primary_key=True,)
        event_role_id = db_handle.Column('event_role_id', db_handle.Integer,  db_handle.ForeignKey('event_roles.event_role_id'),primary_key=True,)        
        role = db_handle.relationship('EventRoles')
        

    return EventUsersRoles
    
