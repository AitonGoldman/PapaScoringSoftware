from lib.serializer import roles
from marshmallow_sqlalchemy import field_for
from marshmallow import fields

def generate_pss_user_serializer(app):    
    roles_schema = roles.generate_roles_serializer(app)
    class pss_user_schema(app.ma.ModelSchema):                
        roles = app.ma.Nested(roles_schema,many=True)
        password_crypt = field_for(app.tables.PssUsers, 'password_crypt',load_only=True)
        class Meta:
            model = app.tables.PssUsers
    return pss_user_schema
