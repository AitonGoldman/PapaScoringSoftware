from flask_principal import Permission
import needs

class EventCreatorPermission(Permission):
    def __init__(self,event_id=None):
        login_need = needs.EventCreatorRoleNeed()
        super(EventCreatorPermission, self).__init__(login_need)

class EventEditPermission(Permission):
    def __init__(self,event_id):        
        edit_need = needs.EventEditNeed(event_id)
        super(EventEditPermission, self).__init__(edit_need)
        
class CreateEventUserPermission(Permission):
    def __init__(self,event_id):        
        create_event_user_need = needs.TournamentDirectorRoleNeed(event_id)
        event_editor_need = needs.EventEditNeed(event_id)        
        super(CreateEventUserPermission, self).__init__(create_event_user_need,event_editor_need)

class CreatePlayerPermission(Permission):
    def __init__(self,event_id):        
        td_create_player_need = needs.TournamentDirectorRoleNeed(event_id)
        desk_create_player_need = needs.DeskworkerRoleNeed(event_id)        
        event_editor_need = needs.EventEditNeed(event_id)        
        super(CreatePlayerPermission, self).__init__(td_create_player_need,event_editor_need,desk_create_player_need)
        
class CreateTournamentPermission(Permission):
    def __init__(self,event_id):        
        create_tournament_need = needs.TournamentDirectorRoleNeed(event_id)
        event_editor_need = needs.EventEditNeed(event_id)        
        super(CreateTournamentPermission, self).__init__(create_tournament_need,event_editor_need)
        
class CreateTournamentMachinePermission(Permission):
    def __init__(self,event_id):        
        create_tournament_need = needs.TournamentDirectorRoleNeed(event_id)
        event_editor_need = needs.EventEditNeed(event_id)        
        super(CreateTournamentMachinePermission, self).__init__(create_tournament_need,event_editor_need)
        
class DeskTokenPurchasePermission(Permission):
    def __init__(self,event_id):        
        td_token_purchase_need = needs.TournamentDirectorRoleNeed(event_id)
        desk_token_purchase_need = needs.DeskworkerRoleNeed(event_id)        
        event_editor_need = needs.EventEditNeed(event_id)                 
        super(DeskTokenPurchasePermission, self).__init__(td_token_purchase_need,desk_token_purchase_need,event_editor_need)

class QueuePermission(Permission):
    def __init__(self,event_id):        
        td_queue_need = needs.TournamentDirectorRoleNeed(event_id)
        desk_queue_need = needs.DeskworkerRoleNeed(event_id)        
        score_queue_need = needs.ScorekeeperRoleNeed(event_id)        
        event_editor_need = needs.EventEditNeed(event_id)                 
        super(QueuePermission, self).__init__(td_queue_need,desk_queue_need,score_queue_need,event_editor_need)

class ScorekeeperPermission(Permission):
    def __init__(self,event_id):        
        td_need = needs.TournamentDirectorRoleNeed(event_id)        
        score_need = needs.ScorekeeperRoleNeed(event_id)        
        event_editor_need = needs.EventEditNeed(event_id)                 
        super(ScorekeeperPermission, self).__init__(td_need,score_need,event_editor_need)
        
class PlayerQueuePermission(Permission):
    def __init__(self,event_id):        
        player_queue_need = needs.PlayerRoleNeed(event_id)
        super(PlayerQueuePermission, self).__init__(player_queue_need)
        
class PlayerTokenPurchasePermission(Permission):
    def __init__(self,event_id):        
        player_token_purchase_need = needs.PlayerRoleNeed(event_id)
        super(PlayerTokenPurchasePermission, self).__init__(player_token_purchase_need)
        
