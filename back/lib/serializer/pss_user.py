from lib.serializer import roles,event,generic
from flask_restless.helpers import to_dict

ALL='all'

def generate_pss_user_to_dict_serializer(type_of_serializer):
    def serialize_full_pss_user(pss_user_model):
        generic_serializer = generic.generate_generic_serializer(generic.ALL)
        serialized_pss_user = to_dict(pss_user_model)                
        serialized_pss_user.pop('password_crypt',None)
        serialized_pss_user['admin_roles']=[generic_serializer(role) for role in pss_user_model.admin_roles]
        serialized_pss_user['event_roles']=[generic_serializer(role) for role in pss_user_model.event_roles]
        serialized_pss_user['events']=[generic_serializer(event) for event in pss_user_model.events]
        serialized_pss_user['event_user']=generic_serializer(pss_user_model.event_user)
        if serialized_pss_user['event_user'] is not None:
            serialized_pss_user['event_user'].pop('password_crypt',None)        
        return serialized_pss_user        
    if type_of_serializer == ALL:
        return serialize_full_pss_user
