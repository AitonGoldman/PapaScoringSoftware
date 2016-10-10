from flask_principal import Permission,RoleNeed,UserNeed

Admin_permission = Permission(RoleNeed('admin'))
Desk_permission = Permission(RoleNeed('desk'))
Scorekeeper_permission = Permission(RoleNeed('scorekeeper'))
    
