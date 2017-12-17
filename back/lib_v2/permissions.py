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
        
