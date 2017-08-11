from flask import Flask
from lib.PssConfig  import PssConfig
from pss_models import ImportedTables
import os,sys
from lib import bootstrap,roles

if len(sys.argv) > 1:
    db_name=sys.argv[1]
else:
    print "didn't specify db name..."
    sys.exit(1)

os.environ['pss_db_name']=db_name
pss_config = PssConfig()

real_app = Flask('pss_admin')

pss_config.get_db_info().create_db_and_tables(real_app,True)
db_handle = pss_config.get_db_info().create_db_handle(real_app)
tables = pss_config.get_db_info().getImportedTables(real_app,'pss_admin')
bootstrap.bootstrap_pss_admin_event(tables)
bootstrap.bootstrap_roles(tables)
new_pss_admin_user = tables.PssUsers(username='test_pss_admin_user')
new_pss_admin_event_user = tables.EventUsers()
new_pss_admin_event_user.crypt_password('password')
new_pss_admin_user.event_user=new_pss_admin_event_user
tables.db_handle.session.add(new_pss_admin_user)
new_pss_admin_user.roles.append(tables.Roles.query.filter_by(name=roles.PSS_ADMIN).first())

tables.db_handle.session.commit()

if len(sys.argv) == 1:
    sys.exit()

# need to bootstrap test env
# new_event = tables.Events(name="test_event")
# db_handle.session.add(new_event)
# pss_users_events_roles = tables.PssUsersEventsRoles()
# pss_users_events_roles.event=new_event
# pss_users_events_roles.role=role_tournament_director
# new_pss_user = tables.PssUsers(username='test_pss_user')
# new_pss_user.crypt_password('password2')
# tables.db_handle.session.add(new_pss_user)
# new_pss_user.roles.append(role_admin)

# tables.db_handle.session.commit()

# new_pss_user.event_roles.append(pss_users_events_roles)
# new_pss_user.events.append(new_event)
# db_handle.session.commit()

    
