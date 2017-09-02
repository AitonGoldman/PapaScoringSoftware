from flask_principal import Permission,RoleNeed,UserNeed
from lib import roles_constants

create_pss_user_permissions = Permission(RoleNeed(roles_constants.PSS_ADMIN))
create_pss_event_user_permissions = Permission(RoleNeed(roles_constants.TOURNAMENT_DIRECTOR))
create_pss_event_permissions = Permission(RoleNeed(roles_constants.PSS_USER),RoleNeed(roles_constants.PSS_ADMIN))
create_player_permissions = Permission(RoleNeed(roles_constants.TOURNAMENT_DIRECTOR),RoleNeed(roles_constants.DESKWORKER))
create_tournament_permissions = Permission(RoleNeed(roles_constants.TOURNAMENT_DIRECTOR))
event_user_buy_tickets_permissions = Permission(RoleNeed(roles_constants.TOURNAMENT_DIRECTOR),RoleNeed(roles_constants.DESKWORKER))
player_buy_tickets_permissions = Permission(RoleNeed(roles_constants.PSS_PLAYER))
player_add_to_queue_permissions = Permission(RoleNeed(roles_constants.PSS_PLAYER),RoleNeed(roles_constants.TOURNAMENT_DIRECTOR),RoleNeed(roles_constants.DESKWORKER),RoleNeed(roles_constants.SCOREKEEPER))
clear_tournament_queue_permissions = Permission(RoleNeed(roles_constants.TOURNAMENT_DIRECTOR))
bump_down_queue_permissions = Permission(RoleNeed(roles_constants.TOURNAMENT_DIRECTOR),RoleNeed(roles_constants.DESKWORKER),RoleNeed(roles_constants.SCOREKEEPER))

ifpa_lookup_permissions=Permission(RoleNeed(roles_constants.TOURNAMENT_DIRECTOR),RoleNeed(roles_constants.DESKWORKER))
