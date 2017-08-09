from lib.serializer import event

#FIXME : probably don't need a nest event here
def generate_event_roles_serializer(app):
    class event_roles_schema(app.ma.ModelSchema):
        class Meta:
            model = app.tables.PssUsersEventsRoles
    return event_roles_schema
    
def generate_roles_serializer(app):        
    class roles_schema(app.ma.ModelSchema):
        class Meta:
            model = app.tables.Roles
    return roles_schema
