from lib.serializer import roles,event,generic
from flask_restless.helpers import to_dict

ALL='all'

def generate_token_puchase_to_dict_serializer(type_of_serializer):
    def serialize_full_token_purchase(token_purchase_model):
        generic_serializer = generic.generate_generic_serializer(generic.ALL)
        serialized_token_purchase = to_dict(token_purchase_model)                        
        return serialized_token_purchase        
    if type_of_serializer == ALL:
        return serialize_full_token_purchase
