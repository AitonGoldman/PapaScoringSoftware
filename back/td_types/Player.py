from flask_restless.helpers import to_dict

def generate_player_role_mapping(db_handle):
    Role_Player_mapping = db_handle.Table(
        'role_player',
        db_handle.Column('player_id', db_handle.Integer, db_handle.ForeignKey('player.player_id')),
        db_handle.Column('role_id', db_handle.Integer, db_handle.ForeignKey('role.role_id'))
    )
    return Role_Player_mapping


def generate_player_class(db_handle,Team_Player_mapping):    
    Role_Player_mapping = generate_player_role_mapping(db_handle)
    #Team_Player_mapping = generate_player_team_mapping(db_handle)
    class Player(db_handle.Model):
        player_id = db_handle.Column(db_handle.Integer,primary_key=True)
        asshole_count = db_handle.Column(db_handle.Integer)
        bump_count = db_handle.Column(db_handle.Integer)        
        first_name = db_handle.Column(db_handle.String(1000))
        last_name = db_handle.Column(db_handle.String(1000))
        
        ifpa_ranking = db_handle.Column(db_handle.Integer)
        email_address = db_handle.Column(db_handle.String(120))
        active = db_handle.Column(db_handle.Boolean, default=True)
        pin = db_handle.Column(db_handle.Integer, db_handle.Sequence(name='player_pin_seq',start=1234,increment=13))
        user_id = db_handle.Column(db_handle.Integer,db_handle.ForeignKey('user.user_id'))
        linked_division_id = db_handle.Column(db_handle.Integer,
                                            db_handle.ForeignKey(
                                                'division.division_id'))
        roles = db_handle.relationship(
           'Role',
           secondary=Role_Player_mapping
        )
        teams = db_handle.relationship(
            'Team',
            secondary=Team_Player_mapping,
            lazy='joined'
        )
        user = db_handle.relationship('User')
        division_machine = db_handle.relationship('DivisionMachine', uselist=False)
        linked_division = db_handle.relationship('Division', uselist=False)

        @staticmethod
        def is_authenticated():
            """Players are always authenticated"""
            return True

        @staticmethod
        def is_active():
            """Players are always active"""
            return True

        @staticmethod
        def is_anonymous():
            """No anon players"""
            return False

        def get_full_name(self):
            return "%s %s"%(self.first_name,self.last_name)
        def get_id(self):
            """Get the players's id"""
            return self.player_id
    
        def gen_pin(self):        
            self.pin = self.player_id
        
        def to_dict_simple(self):
            player_dict = to_dict(self)
            player_dict['pin']=None
            player_dict['full_name']=self.get_full_name()
            if self.roles:
                player_dict['roles']={role.role_id:role.to_dict_simple() for role in self.roles}
            if self.linked_division_id:
                #player_dict['linked_division']=self.linked_division.to_dict_simple()
                player_dict['linked_division_name']=self.linked_division.get_tournament_name(self.linked_division.tournament)
            if self.division_machine:                
                player_dict['division_machine']={'division_machine_id':self.division_machine.division_machine_id,'division_machine_name':self.division_machine.machine.machine_name}
            if self.teams:
                player_dict['teams']=[team.to_dict_simple() for team in self.teams]
            return player_dict
            
    return Player
