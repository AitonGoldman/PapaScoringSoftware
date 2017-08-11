from lib.serializer import event

#FIXME : rename this to user_event_roles mapper
def generate_event_roles_serializer(app):
    class event_roles_schema(app.ma.ModelSchema):
        class Meta:
            model = app.tables.PssEventUsersRoles
    return event_roles_schema

def generate_roles_serializer(app):        
    class roles_schema(app.ma.ModelSchema):
        class Meta:
            model = app.tables.Roles
    return roles_schema
