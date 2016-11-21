def create_roles(app,custom_roles=[]):
    roles = ['admin','desk','scorekeeper','void','player']                    
    db_handle = app.tables.db_handle
    if len(custom_roles)>0:
        roles = custom_roles
    for role in roles:
        db_handle.session.add(app.tables.Role(name=role))
        db_handle.session.commit()

        
