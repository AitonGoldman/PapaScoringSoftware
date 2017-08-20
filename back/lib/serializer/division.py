from lib.serializer import roles,event,generic
from flask_restless.helpers import to_dict

ALL='all'

def generate_division_to_dict_serializer(type_of_serializer):
    def serialize_full_division(division_model):
        generic_serializer = generic.generate_generic_serializer(generic.ALL)
        serialized_division = to_dict(division_model)                        
        serialized_division['division_machines']=[generic_serializer(division_machine) for division_machine in division_model.division_machines]
        serialized_division['tournament']=generic_serializer(division_model.tournament)
        return serialized_division        
    if type_of_serializer == ALL:
        return serialize_full_division
