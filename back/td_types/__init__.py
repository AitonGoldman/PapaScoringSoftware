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
from Queue import generate_queue_class
from Score import generate_score_class
from Entry import generate_entry_class
from AuditLog import generate_audit_log_class
from DivisionFinal import generate_division_final_class
from FinalsPlayer import generate_finals_player_class
from TicketPurchase import generate_ticket_purchase_class
from PurchaseSummary import generate_purchase_summary_class
from DivisionFinalRound import generate_division_final_round_class
from DivisionFinalMatch import generate_division_final_match_class
from FinalsMatchGameResult import generate_finals_match_game_result_class
from FinalsMatchPlayerResult import generate_finals_match_player_result_class
from FinalsMatchGamePlayerResult import generate_finals_match_game_player_result_class

class ImportedTables():
    def __init__(self,db_handle):
        self.Role = generate_role_class(db_handle)        
        self.User = generate_user_class(db_handle)        
        self.Tournament = generate_tournament_class(db_handle)
        self.Division = generate_division_class(db_handle)
        #self.DivisionFinal = generate_division_final_class(db_handle)                
        #self.FinalsPlayer = generate_finals_player_class(db_handle)
        self.Machine = generate_machine_class(db_handle)
        self.DivisionMachine = generate_division_machine_class(db_handle)
        self.MetaDivision = generate_meta_division_class(db_handle)
        self.TeamPlayerMapping = generate_player_team_mapping(db_handle)
        self.Team = generate_team_class(db_handle,self.TeamPlayerMapping)
        self.Player = generate_player_class(db_handle,self.TeamPlayerMapping,1)
        self.Token = generate_token_class(db_handle)
        self.Queue = generate_queue_class(db_handle)
        self.Score = generate_score_class(db_handle)
        self.Entry = generate_entry_class(db_handle)
        self.AuditLog = generate_audit_log_class(db_handle)
        self.TicketPurchase = generate_ticket_purchase_class(db_handle)
        self.PurchaseSummary = generate_purchase_summary_class(db_handle)
        self.DivisionFinal = generate_division_final_class(db_handle)
        self.FinalsPlayer = generate_finals_player_class(db_handle)
        self.DivisionFinalRound = generate_division_final_round_class(db_handle)
        self.DivisionFinalMatch = generate_division_final_match_class(db_handle)
        self.FinalsMatchGameResult = generate_finals_match_game_result_class(db_handle)
        self.FinalsMatchPlayerResult = generate_finals_match_player_result_class(db_handle)
        self.FinalsMatchGamePlayerResult = generate_finals_match_game_player_result_class(db_handle)

        self.db_handle = db_handle
        
 
