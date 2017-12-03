from flask_restless.helpers import to_dict

PSS_USER_PRIVATE_FIELDS=['password_crypt']
EVENT_PRIVATE_FIELDS=['stripe_api_key','stripe_public_key','ionic_profile','ionic_api_key','ifpa_api_key']

class serializer_v2():
    def __init__(self, private_fields):
        self.private_fields=private_fields                
        
    def serialize_model(self,model,show_private_fields=False):
        generic_model_dict = {}
        for c in model.__table__.columns:
            if c.primary_key:
                continue            
            if len(c.foreign_keys) > 0:
                continue
            if c.name in self.private_fields and show_private_fields is False:
                continue            
            generic_model_dict[c.name]=getattr(model,c.name)
        return generic_model_dict

def serialize_pss_user_public(model):
    pss_user_dict=serializer_v2(PSS_USER_PRIVATE_FIELDS).serialize_model(model)
    pss_user_dict['full_user_name']=pss_user_dict['first_name']+' '+pss_user_dict['last_name']
    if model.extra_title:
        pss_user_dict['full_user_name']=pss_user_dict['full_user_name']+' '+pss_user_dict['extra_title']
    return pss_user_dict

def serialize_event_public(model):
    event_dict=serializer_v2(EVENT_PRIVATE_FIELDS).serialize_model(model)    
    return event_dict

