from flask_principal import Permission,RoleNeed,UserNeed

Admin_permission = Permission(RoleNeed('admin'))
Desk_permission = Permission(RoleNeed('desk'))
Scorekeeper_permission = Permission(RoleNeed('scorekeeper'))
Player_permission = Permission(RoleNeed('player'))    
Token_permission = Permission(RoleNeed('token'))
Queue_permission = Permission(RoleNeed('queue'))
InLineRegistration_permission = Permission(RoleNeed('in_line_registration'))
Page_permission = Permission(RoleNeed('page'))
