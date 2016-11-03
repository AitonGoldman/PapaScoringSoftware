from Role import generate_role_class
from User import generate_user_class
from Tournament import generate_tournament_class
from Division import generate_division_class

class ImportedTables():
    def __init__(self,db_handle):
        self.Role = generate_role_class(db_handle)        
        self.User = generate_user_class(db_handle)        
        self.Tournament = generate_tournament_class(db_handle)
        self.Division = generate_division_class(db_handle)
        self.db_handle = db_handle

 
