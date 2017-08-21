def generate_tournament_machines_class(db_handle,event_name):
    class TournamentMachines(db_handle.Model):        
        # pylint: disable=no-init
        # pylint can't find SQLAlchemy's __init__() method for some reason                
        __tablename__="tournament_machines_"+event_name                

        tournament_machine_id = db_handle.Column(db_handle.Integer, primary_key=True)
        tournament_machine_name = db_handle.Column(db_handle.String(1000))                
        tournament_machine_abbreviation = db_handle.Column(db_handle.String(10))
        tournament_id=db_handle.Column('tournament_id', db_handle.Integer, db_handle.ForeignKey('tournaments_'+event_name+'.tournament_id'))
        machine_id=db_handle.Column('machine_id', db_handle.Integer, db_handle.ForeignKey('machines.machine_id'))
        player_id=db_handle.Column('player_id', db_handle.Integer, db_handle.ForeignKey('players.player_id'))
        team_id=db_handle.Column('team_id', db_handle.Integer, db_handle.ForeignKey('teams_'+event_name+'.team_id'))
        active=db_handle.Column(db_handle.Boolean,default=False)
        removed=db_handle.Column(db_handle.Boolean)        
    return TournamentMachines
    
