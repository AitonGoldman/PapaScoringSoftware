import os 
from Events import generate_events_class
from Roles import generate_roles_class
from EventRoles import generate_event_roles_class
from EventUsers import generate_event_users_class
from PssUsers import generate_pss_users_class

class ImportedTables():
    def __init__(self,db_handle,event_name,pss_event_admin_name):
        self.list_of_event_specific_tables=[]
        self.Events = generate_events_class(db_handle)        
        #FIXME : rename Roles to AdminRoles (or something less generic)
        self.Roles = generate_roles_class(db_handle)
        self.EventRoles = generate_event_roles_class(db_handle)        
        self.EventUsers = generate_event_users_class(db_handle,event_name)        
        self.PssUsers = generate_pss_users_class(db_handle,event_name)        
        
        self.db_handle=db_handle
    def get_list_of_event_specific_tables(self):
        #FIXME : make this do something
        pass
