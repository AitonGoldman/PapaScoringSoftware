from lib.serializer import roles,event,generic
from flask_restless.helpers import to_dict

ALL='all'

def generate_player_to_dict_serializer(type_of_serializer):
    def serialize_full_player(player_model):
        generic_serializer = generic.generate_generic_serializer(generic.ALL)
        serialized_player = to_dict(player_model)                        
        #serialized_pss_user['admin_roles']=[generic_serializer(role) for role in pss_user_model.admin_roles]
        serialized_player['player_roles']=[generic_serializer(role) for role in player_model.player_roles]
        serialized_player['events']=[generic_serializer(event) for event in player_model.events]        
        if player_model.event_player:
            serialized_player['event_player']=generic_serializer(player_model.event_player)        
            serialized_player['event_player'].pop('event_player_pin',None)        
        return serialized_player        
    if type_of_serializer == ALL:
        return serialize_full_player
