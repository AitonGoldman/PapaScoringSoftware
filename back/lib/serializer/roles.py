from lib.serializer import event

#FIXME : rename this to user_event_roles mapper
def generate_event_roles_serializer(app):
    class event_roles_schema(app.ma.ModelSchema):
        class Meta:
            model = app.tables.PssUsersEventsRoles
    return event_roles_schema

#FIXME : need actual event roles serializer (for EventRoles table)

def generate_roles_serializer(app):        
    class roles_schema(app.ma.ModelSchema):
        class Meta:
            model = app.tables.Roles
    return roles_schema
