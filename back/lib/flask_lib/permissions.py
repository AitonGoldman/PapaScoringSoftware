from flask_principal import Permission,RoleNeed,UserNeed

pss_admin_permission = Permission(RoleNeed('pss_admin'))
pss_event_permission = Permission(RoleNeed('pss_user'),RoleNeed('pss_admin'))
