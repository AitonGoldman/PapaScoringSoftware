from flask_principal import Permission,RoleNeed,UserNeed

create_pss_user_permissions = Permission(RoleNeed('pss_admin'))
create_pss_event_user_permissions = Permission(RoleNeed('tournament_director'))
