from lib_v2.serializers import generic
from flask_restless.helpers import to_dict

ALL='all'

def generate_pss_user_to_dict_serializer(type_of_serializer):
    def serialize_full_pss_user(pss_user_model):
        generic_serializer = generic.generate_generic_serializer(generic.ALL)
        serialized_pss_user = to_dict(pss_user_model)                
        serialized_pss_user.pop('password_crypt',None)
        serialized_pss_user['full_user_name']=pss_user_model.first_name+" "+pss_user_model.last_name
        if pss_user_model.extra_title:
            serialized_pss_user['full_user_name']=serialized_pss_user['full_user_name']+" "+pss_user_model.extra_title    
        return serialized_pss_user        
    if type_of_serializer == ALL:
        return serialize_full_pss_user
