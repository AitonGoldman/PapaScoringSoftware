from passlib.hash import sha512_crypt

"""Model object for a Player"""
def generate_players_class(db_handle):        
    class Players(db_handle.Model):
        """Model object for Pss Users"""
        # pylint: disable=no-init
        # pylint can't find SQLAlchemy's __init__() method for some reason
        player_id = db_handle.Column(db_handle.Integer, primary_key=True)        
        first_name = db_handle.Column(db_handle.String(80), nullable=False)    
        last_name = db_handle.Column(db_handle.String(80), nullable=False)    
        extra_title = db_handle.Column(db_handle.String(80))    
        ifpa_id = db_handle.Column(db_handle.Integer)                
        has_pic = db_handle.Column(db_handle.Boolean(),default=False)
        img_url=db_handle.Column(db_handle.String(150))                
        ioniccloud_push_token=db_handle.Column(db_handle.String(500))                
        pin=db_handle.Column(db_handle.Integer)
        
        def __repr__(self):
            existing_player_name = self.first_name+" "+self.last_name
            if self.extra_title:
                existing_player_name = existing_player_name + " " + self.extra_title
            
            return existing_player_name

            #return '<Player %r>' % self.first_name+" "+self.last_name
            
        @staticmethod
        def is_authenticated():
            """Users are always authenticated"""
            return True
                
        def is_active(self):            
            return True
            
        @staticmethod
        def is_anonymous():
            """No anon users"""
            return False

        def get_id(self):
            """Get the user's id"""
            return "player_%s"%self.player_id

        def verify_pin(self, pin):
            if self.pin!=pin:
                return False
            return True
        
    return Players
    
