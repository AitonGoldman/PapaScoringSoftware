def generate_event_role_mappings_class(db_handle):    
    class EventRoleMappings(db_handle.Model):        
        pss_user_id=db_handle.Column('pss_user_id', db_handle.Integer, db_handle.ForeignKey('pss_users.pss_user_id'),primary_key=True)
        event_role_id=db_handle.Column('event_role_id', db_handle.Integer, db_handle.ForeignKey('event_roles.event_role_id'),primary_key=True)
        event_id=db_handle.Column('event_id', db_handle.Integer, db_handle.ForeignKey('events.event_id'))                
    return EventRoleMappings   
    

