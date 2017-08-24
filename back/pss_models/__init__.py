import os 
from Events import generate_events_class
from AdminRoles import generate_admin_roles_class
from EventRoles import generate_event_roles_class
from PlayerRoles import generate_player_roles_class
from EventUsers import generate_event_users_class
from PssUsers import generate_pss_users_class
from Players import generate_players_class
from EventPlayers import generate_event_players_class
from Teams import generate_teams_class
from MultiDivisionTournaments import generate_mutli_division_tournaments_class
from Tournaments import generate_tournaments_class
from MetaTournaments import generate_meta_tournaments_class
from Machines import generate_machines_class
from TournamentMachines import generate_tournament_machines_class
from Tokens import generate_tokens_class
from AuditLogs import generate_audit_logs_class


class ImportedTables():
    def __init__(self,db_handle,event_name,pss_event_admin_name):
        self.list_of_event_specific_tables=[]
        self.Events = generate_events_class(db_handle)                
        self.AdminRoles = generate_admin_roles_class(db_handle)
        self.EventRoles = generate_event_roles_class(db_handle)
        self.PlayerRoles = generate_player_roles_class(db_handle)                
        self.EventUsers = generate_event_users_class(db_handle,event_name)        
        self.PssUsers = generate_pss_users_class(db_handle,event_name)        
        self.Players = generate_players_class(db_handle,event_name)
        self.EventPlayers = generate_event_players_class(db_handle,event_name)
        self.Teams = generate_teams_class(db_handle,event_name)        
        self.Machines = generate_machines_class(db_handle,event_name)
        self.TournamentMachines = generate_tournament_machines_class(db_handle,event_name)
        self.MultiDivisionTournaments = generate_mutli_division_tournaments_class(db_handle,event_name)
        self.Tournaments = generate_tournaments_class(db_handle,event_name)
        self.MetaTournaments = generate_meta_tournaments_class(db_handle,event_name)
        self.Tokens = generate_tokens_class(db_handle,event_name)
        self.AuditLogs = generate_audit_logs_class(db_handle,event_name)        
        
        self.db_handle=db_handle
    def get_list_of_event_specific_tables(self):
        #FIXME : make this do something
        pass
