from lib.serializer import roles,event,generic
from flask_restless.helpers import to_dict

ALL='all'

def generate_tournament_to_dict_serializer(type_of_serializer):
    def serialize_full_tournament(tournament_model):
        generic_serializer = generic.generate_generic_serializer(generic.ALL)
        serialized_tournament = to_dict(tournament_model)                        
        serialized_tournament['tournament_machines']=[generic_serializer(tournament_machine) for tournament_machine in tournament_model.tournament_machines]
        serialized_tournament['tournament']=generic_serializer(tournament_model.tournament)
        return serialized_tournament        
    if type_of_serializer == ALL:
        return serialize_full_tournament
