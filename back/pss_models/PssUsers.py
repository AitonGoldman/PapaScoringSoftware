from passlib.hash import sha512_crypt

def generate_pss_user_role_mapping(db_handle):
    Role_PssUser_mapping = db_handle.Table(
        'role_pss_user',
        db_handle.Column('pss_user_id', db_handle.Integer, db_handle.ForeignKey('pss_users.pss_user_id')),
        db_handle.Column('role_id', db_handle.Integer, db_handle.ForeignKey('roles.role_id'))
    )
    return Role_PssUser_mapping

def generate_pss_user_event_mapping(db_handle):
    Event_PssUser_mapping = db_handle.Table(
        'event_pss_user',
        db_handle.Column('pss_user_id', db_handle.Integer, db_handle.ForeignKey('pss_users.pss_user_id')),
        db_handle.Column('event_id', db_handle.Integer, db_handle.ForeignKey('events.event_id'))
    )
    return Event_PssUser_mapping

# FIXME : need to make it so users can change their info via email confirmation of changes

"""Model object for a Pss Users"""
def generate_pss_users_class(db_handle):
    Role_PssUser_mapping = generate_pss_user_role_mapping(db_handle)
    Event_PssUser_mapping = generate_pss_user_event_mapping(db_handle)
    
    class PssUsers(db_handle.Model):
        """Model object for Pss Users"""
        # pylint: disable=no-init
        # pylint can't find SQLAlchemy's __init__() method for some reason
        pss_user_id = db_handle.Column(db_handle.Integer, primary_key=True)
        username = db_handle.Column(db_handle.String(80), unique=True, nullable=False)    
        password_crypt = db_handle.Column(db_handle.String(134))
        has_picture = db_handle.Column(db_handle.Boolean(),default=False)
        ioniccloud_push_token=db_handle.Column(db_handle.String(500))        
        roles = db_handle.relationship(
           'Roles',
           secondary=Role_PssUser_mapping
        )
        event_roles = db_handle.relationship('EventUsersRoles')
        event_user = db_handle.relationship('EventUsers',uselist=False)
            
        events = db_handle.relationship(
           'Events',
           secondary=Event_PssUser_mapping
        )
        
        def crypt_password(self, password):
            """Encrypt a plaintext password and store it"""
            self.password_crypt = sha512_crypt.encrypt(password)

        def verify_password(self, password):
            """Check to see if a plaintext password matches our crypt"""
            return sha512_crypt.verify(password, self.password_crypt)
        
        def __repr__(self):
            return '<User %r>' % self.username
            
        @staticmethod
        def is_authenticated():
            """Users are always authenticated"""
            return True
        
        @staticmethod
        def is_active():
            """Users are always active"""
            return True
        
        @staticmethod
        def is_anonymous():
            """No anon users"""
            return False

        def get_id(self):
            """Get the user's id"""
            return self.pss_user_id
        
    return PssUsers
    
