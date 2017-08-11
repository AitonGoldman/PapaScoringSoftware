from lib.PssConfig import PssConfig

def create_user(flask_app,username,password,roles,commit=False):
    tables=flask_app.tables
    user = tables.PssUsers(username=username)
    event_user = tables.EventUsers()
    event_user.crypt_password(password)
    user.event_user = event_user
    tables.db_handle.session.add(user)
    for role in roles:
        user.roles.append(role)        
    if commit:
        tables.db_handle.session.commit()

def create_event(flask_app,is_pss_admin_app=False):
    pss_config = PssConfig()
    # if is_pss_admin_app:
    #     tables = pss_config.get_db_info().getImportedTables(flask_app,"unimportant")
    #     admin_event = tables.Events(name=flask_app.name,flask_secret_key='poop')
    #     tables.db_handle.session.add(admin_event)
    #     tables.db_handle.session.commit()                

