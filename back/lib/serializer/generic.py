from flask_restless.helpers import to_dict

ALL='all'

def generate_generic_serializer(type_of_serializer):    
    def serialize_generic_model(generic_model):
        return to_dict(generic_model)
    if type_of_serializer == ALL:
        return serialize_generic_model
