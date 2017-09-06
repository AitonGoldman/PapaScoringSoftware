from lib.serializer import generic
from flask_restless.helpers import to_dict

ALL='all'
MINIMUM_EVENT='minimum_event'

def generate_event_to_dict_serializer(type_of_serializer):
    def serialize_minimal_event(event_model):
        serialized_event = {}
        serialized_event['event_id']=event_model.event_id
        serialized_event['event_name']=event_model.name
        return serialized_event
    if type_of_serializer == MINIMUM_EVENT:
        return serialize_minimal_event
