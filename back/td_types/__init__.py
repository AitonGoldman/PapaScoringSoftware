from Role import generate_role_class
from User import generate_user_class
from Tournament import generate_tournament_class
from Division import generate_division_class
from Machine import generate_machine_class
from DivisionMachine import generate_division_machine_class
from MetaDivision import generate_meta_division_class
from TeamPlayerMapping import generate_player_team_mapping
from Player import generate_player_class
from Team import generate_team_class
from Token import generate_token_class
class ImportedTables():
    def __init__(self,db_handle):
        self.Role = generate_role_class(db_handle)        
        self.User = generate_user_class(db_handle)        
        self.Tournament = generate_tournament_class(db_handle)
        self.Division = generate_division_class(db_handle)
        self.Machine = generate_machine_class(db_handle)
        self.DivisionMachine = generate_division_machine_class(db_handle)
        self.MetaDivision = generate_meta_division_class(db_handle)
        self.TeamPlayerMapping = generate_player_team_mapping(db_handle)
        self.Team = generate_team_class(db_handle,self.TeamPlayerMapping)
        self.Player = generate_player_class(db_handle,self.TeamPlayerMapping)
        self.Token = generate_token_class(db_handle)
        self.db_handle = db_handle
        
 
