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
        machine_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'machine.machine_id'
        ))
        division_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'division.division_id'
        ))
        #finals_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
        #    'finals.finals_id'
        #))    
        #team_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
        #    'team.team_id'
        #))    
        #player_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
        #    'player.player_id'
        #))    
        division = db_handle.relationship(
            'Division',
            foreign_keys=[division_id]
        )    
        machine = db_handle.relationship(
            'Machine',
            foreign_keys=[machine_id]
        )
        #team = db_handle.relationship(
        #    'Team',
        #    foreign_keys=[team_id]
        #)    
        #player = db_handle.relationship('Player')    
                
        def to_dict_simple(self):
            division_machine = to_dict(self)
            division_machine['division_machine_name'] = self.machine.machine_name
            division_machine['abbreviation'] = self.machine.abbreviation        
            return division_machine
        
        #def to_dict_with_player(self):
        #    machine = to_dict(self)
        #    if self.player:
        #        machine['player'] = self.player.to_dict_simple()
    return DivisionMachine
            

