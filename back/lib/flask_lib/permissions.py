from flask_principal import Permission,RoleNeed,UserNeed

#FIXME : use constants
create_pss_user_permissions = Permission(RoleNeed('pss_admin'))
create_pss_event_user_permissions = Permission(RoleNeed('tournament_director'))
create_pss_event_permissions = Permission(RoleNeed('pss_user'),RoleNeed('pss_admin'))
