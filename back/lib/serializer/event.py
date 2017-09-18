from lib.serializer import generic
from flask_restless.helpers import to_dict

ALL='all'
MINIMUM_EVENT='minimum_event'

def generate_event_to_dict_serializer(type_of_serializer):
    def serialize_full_event(event_model):
        serialized_event = to_dict(event_model)                        
        return serialized_event
        
    def serialize_minimal_event(event_model):
        serialized_event = {}
        serialized_event['event_id']=event_model.event_id
        serialized_event['event_name']=event_model.name
        serialized_event['wizard_configured']=event_model.wizard_configured
        serialized_event['event_creator_pss_user_id']=event_model.event_creator_pss_user_id
        serialized_event['active']=event_model.active
        serialized_event['force_ifpa_lookup']=event_model.force_ifpa_lookup        
        serialized_event['has_pic']=event_model.has_pic                
        if event_model.has_pic:
            serialized_event['img_url']=event_model.img_url
            
            #    serialized_event['image_path']='/img/events/%s/%s.jpg' % (event_model.event_id,event_model.event_id)
            
        return serialized_event
    if type_of_serializer == MINIMUM_EVENT:
        return serialize_minimal_event
    if type_of_serializer == ALL:
        return serialize_full_event
