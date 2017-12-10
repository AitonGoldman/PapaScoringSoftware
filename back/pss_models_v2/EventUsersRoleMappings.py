def generate_event_users_role_mapping_class(db_handle,event_name):    
    class EventUsersRoleMappingClass(db_handle.Model):
        pss_user_id=db_handle.Column(db_handle.Integer, db_handle.ForeignKey('pss_users.pss_user_id'),primary_key=True)
        event_role_id=db_handle.Column(db_handle.Integer, db_handle.ForeignKey('event_roles.event_role_id'),primary_key=True)
        event_id=db_handle.Column(db_handle.Integer, db_handle.ForeignKey('events.event_id'),primary_key=True)
        event = db_handle.relationship(
            'Events'
        )
        event_role = db_handle.relationship(
            'EventRoles'
        )
        pss_user = db_handle.relationship(
            'PssUsers'
        )
        
    return TestClass
