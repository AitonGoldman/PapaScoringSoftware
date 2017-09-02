from lib.serializer import generic
from flask_restless.helpers import to_dict

ALL='all'

def generate_queue_to_dict_serializer(type_of_serializer):
    
    def serialize_full_queue(queue_model):
        generic_serializer = generic.generate_generic_serializer(generic.ALL)
        serialized_queue = to_dict(queue_model)                                
        if queue_model.player_id:
            serialized_queue['player']="%s" % queue_model.player
        return serialized_queue        
    if type_of_serializer == ALL:
        return serialize_full_queue
