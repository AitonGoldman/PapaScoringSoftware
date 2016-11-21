from util import db_util
from routes.utils import check_roles_exist

def create_roles(app,custom_roles=[]):
    roles = ['admin','desk','scorekeeper','void','player']                    
    db_handle = app.tables.db_handle
    if len(custom_roles)>0:
        roles = custom_roles
    for role in roles:
        db_handle.session.add(app.tables.Role(name=role))
        db_handle.session.commit()

def create_user(app,username,password,roles=[]):
    db = db_util.app_db_handle(app)
    tables = db_util.app_db_tables(app)
    new_user = tables.User(
        username=username
    )
    
    new_user.crypt_password(password)
    db.session.add(new_user)

    if len(roles)>0:
        check_roles_exist(app.tables, roles)
        for role_id in roles:            
            existing_role = tables.Role.query.filter_by(role_id=role_id).first()            
            new_user.roles.append(existing_role)
    
    db.session.commit()                        
    return new_user
    
        
