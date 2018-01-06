from flask_restless.helpers import to_dict

PSS_USER_PRIVATE_FIELDS=['password_crypt']
EVENT_PRIVATE_FIELDS=['stripe_api_key','stripe_public_key','ionic_profile','ionic_api_key','ifpa_api_key']
TOURNAMENT_PRIVATE_FIELDS=[]
TOURNAMENT_MACHINE_PRIVATE_FIELDS=[]
PLAYER_PRIVATE_FIELDS=['pin','ioniccloud_push_token']
PSS_USER_ONLY='pss_user_only'
PSS_USER_WITH_ROLES='pss_user_with_roles'

PLAYER_ONLY='player_only'
PLAYER_AND_EVENTS='player_and_events'

TOURNAMENT_ONLY='tournament_only'
META_TOURNAMENT_ONLY='meta_tournament_only'
TOURNAMENT_MACHINE_ONLY='tournament_machine_only'

class serializer_v2():
    def __init__(self, private_fields):
        self.private_fields=private_fields                
        
    def serialize_model(self,model,show_private_fields=False):
        generic_model_dict = {}
        for c in model.__table__.columns:
            if len(c.foreign_keys) > 0:
                continue
            if c.name in self.private_fields and show_private_fields is False:
                continue            
            generic_model_dict[c.name]=getattr(model,c.name)
        return generic_model_dict

def serialize_pss_user_public(model,type=PSS_USER_ONLY):
    pss_user_dict=serializer_v2(PSS_USER_PRIVATE_FIELDS).serialize_model(model)
    pss_user_dict['full_user_name']=pss_user_dict['first_name']+' '+pss_user_dict['last_name']
    if model.extra_title:
        pss_user_dict['full_user_name']=pss_user_dict['full_user_name']+' '+pss_user_dict['extra_title']
    #FIXME : event_roles should be controlled by type arg
    pss_user_dict['event_roles']=[to_dict(event_role) for event_role in model.event_roles]
    if type==PSS_USER_ONLY:
        return pss_user_dict

def serialize_tournament_public(model,type=TOURNAMENT_ONLY):
    tournament_dict=serializer_v2(TOURNAMENT_PRIVATE_FIELDS).serialize_model(model)
    if type==TOURNAMENT_ONLY:
        return tournament_dict
    
def serialize_tournament_private(model,type=TOURNAMENT_ONLY,show_private_fields=True):
    tournament_dict=serializer_v2(TOURNAMENT_PRIVATE_FIELDS).serialize_model(model)
    if type==TOURNAMENT_ONLY:
        return tournament_dict

    
def serialize_meta_tournament_public(model,type=META_TOURNAMENT_ONLY):
    meta_tournament_dict=serializer_v2([]).serialize_model(model)
    if type==META_TOURNAMENT_ONLY:
        return meta_tournament_dict
    
def serialize_player_public(model,type_of=PLAYER_ONLY):
    player_dict=serializer_v2(PLAYER_PRIVATE_FIELDS).serialize_model(model)
    player_dict['player_full_name']=model.__repr__()
    
    if type_of==PLAYER_ONLY:
        return player_dict
    if type_of==PLAYER_AND_EVENTS:
        print model.__repr__()
        player_dict['events']=[serialize_event_players_info_public(event_info_instance) for event_info_instance in model.event_info]
        return player_dict

def serialize_player_private(model,type_of=PLAYER_ONLY):
    player_dict=serializer_v2([]).serialize_model(model)
    if type_of==PLAYER_AND_EVENTS:            
        if model.event_info:
            player_dict['events']=[serialize_event_players_info_public(event_info_instance) for event_info_instance in model.event_info]
    player_dict['player_full_name']=model.__repr__()
    return player_dict


def serialize_event_players_info_public(model,type=None):    
    event_info = serializer_v2([]).serialize_model(model)
    event_info['event_id']=model.event_id
    return event_info

def serialize_tournament_machine_public(model,type=TOURNAMENT_MACHINE_ONLY):
    tournament_machine_dict=serializer_v2(TOURNAMENT_MACHINE_PRIVATE_FIELDS).serialize_model(model)
    if type==TOURNAMENT_MACHINE_ONLY:
        return tournament_machine_dict
    
def serialize_event_public(model):
    event_dict=serializer_v2(EVENT_PRIVATE_FIELDS).serialize_model(model)    
    return event_dict

def serialize_event_private(model):
    event_dict=serializer_v2(EVENT_PRIVATE_FIELDS).serialize_model(model,True)    
    return event_dict

