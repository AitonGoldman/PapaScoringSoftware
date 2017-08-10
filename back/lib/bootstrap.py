import os
from base64 import b64encode
from lib import roles
def initialize_admin_event(tables):
    pass

def bootstrap_roles(tables):
    role_admin=tables.Roles(name=roles.PSS_ADMIN,admin_role=True)
    role_user=tables.Roles(name=roles.PSS_USER,admin_role=True)
    role_player=tables.Roles(name=roles.PSS_PLAYER,admin_role=True)
    
    role_tournament_director=tables.EventRoles(name='tournament_director')
    role_scorekeeper=tables.EventRoles(name='scorekeeper')
    role_deskworker=tables.EventRoles(name='deskworker')
    role_scorekeeper_deskworker=tables.EventRoles(name='scorekeeper_deskworker')
    #role_player=tables.EventRoles(name='player')

    tables.db_handle.session.add(role_admin)
    tables.db_handle.session.add(role_user)
    tables.db_handle.session.add(role_scorekeeper)
    tables.db_handle.session.add(role_deskworker)
    tables.db_handle.session.add(role_scorekeeper_deskworker)
    #tables.db_handle.session.add(role_tournament_director)

    tables.db_handle.session.commit()    
    
def bootstrap_pss_admin_event(tables):        
    secret_key=b64encode(os.urandom(24)).decode('utf-8')        
    admin_event = tables.Events(
        name='pss_admin',
        flask_secret_key=secret_key
    )
    tables.db_handle.session.add(admin_event)
    tables.db_handle.session.commit()
        
        
    
