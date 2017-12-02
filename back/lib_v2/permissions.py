from flask_principal import Permission
import needs

class EventCreatorPermission(Permission):
    def __init__(self):
        need = needs.EventCreatorLoginRoleNeed()
        super(EventCreatorPermission, self).__init__(need)
