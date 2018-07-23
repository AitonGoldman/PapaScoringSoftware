def generate_queues_class(db_handle,event_name):
    class Queues(db_handle.Model):
        __tablename__="queues_"+event_name                
        queue_id = db_handle.Column(db_handle.Integer, primary_key=True)
        position = db_handle.Column(db_handle.Integer)
        bumped = db_handle.Column(db_handle.Boolean, default=False)
        tournament_machine_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'tournament_machines_'+event_name+'.tournament_machine_id'
        ))
        player_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'players.player_id'
        ))        
        parent_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'queues_'+event_name+'.queue_id'
        ))
        queue_child = db_handle.relationship('Queues',uselist=False)                    

        player = db_handle.relationship(
            'Players',
            foreign_keys=[player_id]
        )    
        tournament_machine = db_handle.relationship(
            'TournamentMachines', uselist=False,
            foreign_keys=[tournament_machine_id]
        )    

        # def to_dict_simple(self):
        #     queue = to_dict(self)
        #     queue['player']={'player_id':self.player_id,'player_name': "%s %s" % (self.player.first_name,self.player.last_name)}
        #     queue['division_machine']={'division_machine_id':self.division_machine.division_machine_id,'division_machine_name':self.division_machine.machine.machine_name}
        #     if len(self.division_machine.queue) > 0:
        #         for potential_queue_head in self.division_machine.queue:
        #             if potential_queue_head.parent_id is None:
        #                 queue_node = potential_queue_head
        #     else:
        #         queue_node = None
        #     queue_position = 1                        
        #     while queue_node and len(queue_node.queue_child)>0  and queue_node != self:                                
        #         queue_position = queue_position + 1
        #         queue_node = queue_node.queue_child[0]                
        #     if queue_node is None:
        #         queue['queue_position']="This Should Not Happen"                
        #     else:
        #         queue['queue_position']=queue_position
        #     return queue        
    return Queues
