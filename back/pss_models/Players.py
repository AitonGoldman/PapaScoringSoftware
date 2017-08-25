from passlib.hash import sha512_crypt

def generate_player_event_mapping(db_handle):
    Event_Player_mapping = db_handle.Table(
        'event_player',
        db_handle.Column('player_id', db_handle.Integer, db_handle.ForeignKey('players.player_id')),
        db_handle.Column('event_id', db_handle.Integer, db_handle.ForeignKey('events.event_id'))
    )
    return Event_Player_mapping

def generate_player_role_mapping(db_handle,event_name):
    PlayerRole_Player_mapping = db_handle.Table(
        'player_role_player_'+event_name,        
        db_handle.Column('player_id', db_handle.Integer, db_handle.ForeignKey('players.player_id')),
        db_handle.Column('player_role_id', db_handle.Integer, db_handle.ForeignKey('player_roles.player_role_id'))
    )
    return PlayerRole_Player_mapping

# FIXME : need to make it so users can change their info via email confirmation of changes

"""Model object for a Player"""
def generate_players_class(db_handle,event_name):
    
    Event_Player_mapping = generate_player_event_mapping(db_handle)
    PlayerRole_Player_mapping = generate_player_role_mapping(db_handle,event_name)
    
    class Players(db_handle.Model):
        """Model object for Pss Users"""
        # pylint: disable=no-init
        # pylint can't find SQLAlchemy's __init__() method for some reason
        player_id = db_handle.Column(db_handle.Integer, primary_key=True)        
        first_name = db_handle.Column(db_handle.String(80), nullable=False)    
        last_name = db_handle.Column(db_handle.String(80), nullable=False)    
        extra_title = db_handle.Column(db_handle.String(80))    
        ifpa_id = db_handle.Column(db_handle.Integer)                
        has_picture = db_handle.Column(db_handle.Boolean(),default=False)
        ioniccloud_push_token=db_handle.Column(db_handle.String(500))        
        team_id = db_handle.Column('team_id', db_handle.Integer, db_handle.ForeignKey('teams_'+event_name+'.team_id'))

        player_roles = db_handle.relationship(
            'PlayerRoles',
            secondary=PlayerRole_Player_mapping
        )

        event_player = db_handle.relationship('EventPlayers',uselist=False)

        team = db_handle.relationship('Teams',uselist=False)
            
        events = db_handle.relationship(
           'Events',
           secondary=Event_Player_mapping
        )
        
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
            if self.event_player:
                return self.event_player.active
            else:
                return True
            
        @staticmethod
        def is_anonymous():
            """No anon users"""
            return False

        def get_id(self):
            """Get the user's id"""
            return "player_%s"%self.player_id
        
    return Players
    
