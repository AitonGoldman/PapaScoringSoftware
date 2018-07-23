def generate_event_roles_class(db_handle):    
    class EventRoles(db_handle.Model):
        event_role_id=db_handle.Column(db_handle.Integer,primary_key=True)
        event_role_name=db_handle.Column(db_handle.String(80))
    return EventRoles
