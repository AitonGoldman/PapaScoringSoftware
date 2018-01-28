def generate_tournament_machines_class(db_handle):
    class TournamentMachines(db_handle.Model):        
        # pylint: disable=no-init
        # pylint can't find SQLAlchemy's __init__() method for some reason                        

        tournament_machine_id = db_handle.Column(db_handle.Integer, primary_key=True)
        tournament_machine_name = db_handle.Column(db_handle.String(1000))                
        tournament_machine_abbreviation = db_handle.Column(db_handle.String(10))
        tournament_id=db_handle.Column('tournament_id', db_handle.Integer, db_handle.ForeignKey('tournaments.tournament_id'))
        machine_id=db_handle.Column('machine_id', db_handle.Integer, db_handle.ForeignKey('machines.machine_id'))
        player_id=db_handle.Column('player_id', db_handle.Integer, db_handle.ForeignKey('players.player_id'))
        team_id=db_handle.Column('team_id', db_handle.Integer, db_handle.ForeignKey('teams.team_id'))
        active=db_handle.Column(db_handle.Boolean,default=True)
        removed=db_handle.Column(db_handle.Boolean,default=False)
        event_id=db_handle.Column('event_id', db_handle.Integer, db_handle.ForeignKey('events.event_id'))
        #queue = db_handle.relationship('Queues')        
        img_url=db_handle.Column(db_handle.String(100))
        total_play_time=db_handle.Column(db_handle.Integer,default=0)
        total_number_of_players=db_handle.Column(db_handle.Integer,default=0)
        time_of_game_start = db_handle.Column(db_handle.DateTime)

    return TournamentMachines
    
