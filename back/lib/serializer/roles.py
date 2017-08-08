def generate_roles_serializer(app):        
    class roles_schema(app.ma.ModelSchema):
        class Meta:
            model = app.tables.Roles
    return roles_schema
