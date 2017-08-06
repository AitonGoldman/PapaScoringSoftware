import os 
from Events import generate_events_class

class ImportedTables():
    def __init__(self,db_handle,app_name):
        self.Events = generate_events_class(db_handle)        
        
        
 
