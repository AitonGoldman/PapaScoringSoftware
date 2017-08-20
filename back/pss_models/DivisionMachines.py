def generate_division_machines_class(db_handle,event_name):
    class DivisionMachines(db_handle.Model):        
        # pylint: disable=no-init
        # pylint can't find SQLAlchemy's __init__() method for some reason                
        __tablename__="division_machines_"+event_name                

        division_machine_id = db_handle.Column(db_handle.Integer, primary_key=True)
        division_machine_name = db_handle.Column(db_handle.String(1000))                
        division_machine_abbreviation = db_handle.Column(db_handle.String(10))
        division_id=db_handle.Column('division_id', db_handle.Integer, db_handle.ForeignKey('divisions_'+event_name+'.division_id'))
        machine_id=db_handle.Column('machine_id', db_handle.Integer, db_handle.ForeignKey('machines.machine_id'))
        player_id=db_handle.Column('player_id', db_handle.Integer, db_handle.ForeignKey('players.player_id'))
        team_id=db_handle.Column('team_id', db_handle.Integer, db_handle.ForeignKey('teams_'+event_name+'.team_id'))
        active=db_handle.Column(db_handle.Boolean,default=False)
        removed=db_handle.Column(db_handle.Boolean)        
    return DivisionMachines
    
