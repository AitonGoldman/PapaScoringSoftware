from flask_restless.helpers import to_dict
import datetime

def generate_queue_class(db_handle):
    class Queue(db_handle.Model):
        queue_id = db_handle.Column(db_handle.Integer, primary_key=True)
        division_machine_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'division_machine.division_machine_id'
        ))
        player_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'player.player_id'
        ))        
        parent_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'queue.queue_id'
        ))
        queue_child = db_handle.relationship('Queue')            
        player = db_handle.relationship(
            'Player',
            foreign_keys=[player_id]
        )    
        division_machine = db_handle.relationship(
            'DivisionMachine',
            foreign_keys=[division_machine_id]
        )    

        def to_dict_simple(self):
            queue = to_dict(self)
            queue['player']={'player_id':self.player_id,'player_name': "%s %s" % (self.player.first_name,self.player.last_name)}
            queue['division_machine']={'division_machine_id':self.division_machine.division_machine_id,'division_machine_name':self.division_machine.machine.machine_name}
            queue_node = self.division_machine.queue
            queue_position = 1                        
            while len(queue_node.queue_child)>0  and queue_node != self:                                
                queue_position = queue_position + 1
                queue_node = queue_node.queue_child[0]                
            if queue_node is None:
                queue['queue_position']="This Should Not Happen"                
            else:
                queue['queue_position']=queue_position
            return queue        
    return Queue
