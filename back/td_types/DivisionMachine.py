"""Model object for a game machine in a specific division"""

from flask_restless.helpers import to_dict

def generate_division_machine_class(db_handle):
    class DivisionMachine(db_handle.Model):
        """Model object for a game machine"""
        # pylint: disable=no-init
        # pylint can't find SQLAlchemy's __init__() method for some reason    
        removed = db_handle.Column(db_handle.Boolean, default=False)
        division_machine_id = db_handle.Column(db_handle.Integer, primary_key=True)
        #FIXME : need constraint on machine_id + division_id    
        avg_play_time = db_handle.Column(db_handle.String(255))
        machine_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'machine.machine_id'
        ))
        player_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'player.player_id'
        ))

        division_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'division.division_id'
        ))
        # queue_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
        #     'queue.queue_id'
        # ))        
        #finals_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
        #    'finals.finals_id'
        #))    
        team_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'team.team_id'
        ))    
        division = db_handle.relationship(
            'Division',
            foreign_keys=[division_id]
        )    
        machine = db_handle.relationship(
            'Machine',
            foreign_keys=[machine_id]
        )
        team = db_handle.relationship(
            'Team',
            foreign_keys=[team_id]
        )
        queue = db_handle.relationship(
            'Queue'
        )    
        
        player = db_handle.relationship('Player')    
                
        def to_dict_simple(self):
            division_machine = to_dict(self)
            division_machine['division_machine_name'] = self.machine.machine_name
            division_machine['team_tournament']= self.division.team_tournament
            division_machine['abbreviation'] = self.machine.abbreviation        
            if self.player_id:
                division_machine['player']={'player_id':self.player_id,'player_name': "%s %s" % (self.player.first_name,self.player.last_name)}
            if self.team_id:
                division_machine['team']={'team_id':self.team_id,'team_name': "%s" % (self.team.team_name)}
                
            return division_machine
        
    return DivisionMachine
            

