from flask_principal import Permission,RoleNeed,UserNeed
from lib import roles

create_pss_user_permissions = Permission(RoleNeed(roles.PSS_ADMIN))
create_pss_event_user_permissions = Permission(RoleNeed(roles.TOURNAMENT_DIRECTOR))
create_pss_event_permissions = Permission(RoleNeed(roles.PSS_USER),RoleNeed(roles.PSS_ADMIN))
