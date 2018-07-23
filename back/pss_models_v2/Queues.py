def generate_queues_class(db_handle):
    class Queues(db_handle.Model):        
        queue_id = db_handle.Column(db_handle.Integer, primary_key=True)
        position = db_handle.Column(db_handle.Integer)
        bumped = db_handle.Column(db_handle.Boolean, default=False)
        tournament_machine_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'tournament_machines.tournament_machine_id'
        ))
        event_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'events.event_id'
        ))
        player_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'players.player_id'
        ))        
        parent_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'queues.queue_id'
        ))
        #queue_child = db_handle.relationship('Queues',uselist=False)                    

        #player = db_handle.relationship(
        #    'Players',
        #    foreign_keys=[player_id]
        #)    
        #tournament_machine = db_handle.relationship(
        #    'TournamentMachines', uselist=False,
        #    foreign_keys=[tournament_machine_id]
        #)    

    return Queues
