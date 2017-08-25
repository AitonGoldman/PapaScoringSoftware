#FIXME : rename this file EventUsers.py
from passlib.hash import sha512_crypt

"""Model object for a EventUsers"""
def generate_event_users_class(db_handle,event_name):
    class EventUsers(db_handle.Model):
        """Model object for Events"""
        # pylint: disable=no-init
        # pylint can't find SQLAlchemy's __init__() method for some reason        
        __tablename__="event_users_"+event_name                
        password_crypt = db_handle.Column(db_handle.String(134))
        pss_user_id = db_handle.Column('pss_user_id', db_handle.Integer, db_handle.ForeignKey('pss_users.pss_user_id'),primary_key=True)
        active=db_handle.Column(db_handle.Boolean(),default=True)

        def crypt_password(self, password):
            """Encrypt a plaintext password and store it"""
            self.password_crypt = sha512_crypt.encrypt(password)

        def verify_password(self, password):
            """Check to see if a plaintext password matches our crypt"""
            return sha512_crypt.verify(password, self.password_crypt)
        
        
    return EventUsers
    
