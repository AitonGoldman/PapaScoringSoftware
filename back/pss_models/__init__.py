import os 
from Events import generate_events_class
from Roles import generate_roles_class
from EventRoles import generate_event_roles_class

from PssUsers import generate_pss_users_class, generate_pss_user_role_mapping
from PssUsersEventRoles import generate_pss_users_event_roles_class

class ImportedTables():
    def __init__(self,db_handle,app_name,pss_event_admin_name):
        self.Events = generate_events_class(db_handle)        
        #FIXME : rename Roles to AdminRoles (or something less generic)
        self.Roles = generate_roles_class(db_handle)
        self.EventRoles = generate_event_roles_class(db_handle)        
        self.PssUsers = generate_pss_users_class(db_handle)
        self.PssUsersEventsRoles = generate_pss_users_event_roles_class(db_handle)
        
        self.db_handle=db_handle
 
