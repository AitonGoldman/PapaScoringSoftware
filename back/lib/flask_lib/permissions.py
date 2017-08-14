from flask_principal import Permission,RoleNeed,UserNeed
from lib import roles_constants

create_pss_user_permissions = Permission(RoleNeed(roles_constants.PSS_ADMIN))
create_pss_event_user_permissions = Permission(RoleNeed(roles_constants.TOURNAMENT_DIRECTOR))
create_pss_event_permissions = Permission(RoleNeed(roles_constants.PSS_USER),RoleNeed(roles_constants.PSS_ADMIN))
