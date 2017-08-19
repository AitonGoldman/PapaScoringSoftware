from lib.serializer import event
from flask_restless.helpers import to_dict

#FIXME : rename this to user_event_roles mapper
def generate_event_roles_serializer(app):
    class event_roles_schema(app.ma.ModelSchema):
        class Meta:
            model = app.tables.EventRoles
    return event_roles_schema

def generate_admin_roles_serializer(app):        
    class admin_roles_schema(app.ma.ModelSchema):
        class Meta:
            model = app.tables.AdminRoles
    return admin_roles_schema
