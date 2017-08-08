from lib.serializer import roles

def generate_pss_user_serializer(app):    
    roles_schema = roles.generate_roles_serializer(app)
    class pss_user_schema(app.ma.ModelSchema):
        roles = app.ma.Nested(roles_schema,many=True)
        class Meta:
            model = app.tables.PssUsers
    return pss_user_schema
