from lib.serializer import queue,generic
from flask_restless.helpers import to_dict

ALL='all'

def generate_tournament_machine_to_dict_serializer(type_of_serializer):
    
    def serialize_full_tournament_machine(tournament_machine_model):
        generic_serializer = generic.generate_generic_serializer(generic.ALL)        
        queue_serializer = queue.generate_queue_to_dict_serializer(queue.ALL)
        serialized_tournament_machine = to_dict(tournament_machine_model)                                
        queue_list = [q for q in tournament_machine_model.queue]
        serialized_tournament_machine['queue']=[]
        for queue_instance in queue_list:
            serialized_queue = queue_serializer(queue_instance)
            #serialized_queue = generic_serializer(queue)            
            # if queue.player_id:
            #     serialized_queue['player']="%s" % queue.player
            serialized_tournament_machine['queue'].append(serialized_queue)
        return serialized_tournament_machine        
    if type_of_serializer == ALL:
        return serialize_full_tournament_machine
