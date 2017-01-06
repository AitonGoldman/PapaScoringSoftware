# pylint: disable=no-name-in-module
# pylint can't read the types from passlib.hash
"""Model object for a user"""
from passlib.hash import sha512_crypt
from sqlalchemy.exc import ArgumentError
from flask_restless.helpers import to_dict
#from app.types import util

def generate_user_role_mapping(db_handle):
    Role_User_mapping = db_handle.Table(
        'role_user',
        db_handle.Column('user_id', db_handle.Integer, db_handle.ForeignKey('user.user_id')),
        db_handle.Column('role_id', db_handle.Integer, db_handle.ForeignKey('role.role_id'))
    )
    return Role_User_mapping

def generate_user_class(db_handle):
    Role_User_mapping = generate_user_role_mapping(db_handle)
    class User(db_handle.Model):
        # pylint: disable=no-init
        # pylint can't find SQLAlchemy's __init__() method for some reason
        """Model object for a user"""
        user_id = db_handle.Column(db_handle.Integer, primary_key=True)
        username = db_handle.Column(db_handle.String(80), unique=True, nullable=False)    
        password_crypt = db_handle.Column(db_handle.String(134))
        has_picture = db_handle.Column(db_handle.Boolean(),default=False)
        is_player = db_handle.Column(db_handle.Boolean(),default=True)
        pin = db_handle.Column(db_handle.Integer)
        ioniccloud_push_token=db_handle.Column(db_handle.String(500))
        roles = db_handle.relationship(
           'Role',
           secondary=Role_User_mapping
        )
        player = db_handle.relationship('Player',uselist=False)
        def crypt_password(self, password):
            """Encrypt a plaintext password and store it"""
            self.password_crypt = sha512_crypt.encrypt(password)

        def verify_password(self, password):
            """Check to see if a plaintext password matches our crypt"""
            if self.is_player:
                return int(password) == self.pin
            else:
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
            return self.user_id

        def to_dict_simple(self):            
            user = to_dict(self)
            del user['password_crypt']
            del user['pin']            
            #user['roles'] = [r.name for r in self.roles]
            if self.is_player:
                user['player']=self.player.to_dict_simple()
            if self.roles:
                user['roles'] = [r.to_dict_simple() for r in self.roles]        
            return user
    return User
        
