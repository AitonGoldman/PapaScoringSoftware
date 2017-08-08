from flask import Flask
from lib.PssConfig  import PssConfig
from pss_models import ImportedTables
import os,sys


if len(sys.argv) > 1:
    db_name=sys.argv[1]
else:
    print "didn't specify db name..."
    sys.exit(1)

os.environ['pss_db_name']=db_name
pss_config = PssConfig()

real_app = Flask('dummy_app')

pss_config.get_db_info().create_db_and_tables(real_app,True)
pss_config.get_db_info().bootstrap_pss_admin_event(real_app,"pss_admin")
db_handle = pss_config.get_db_info().create_db_handle(real_app)
tables = ImportedTables(db_handle, db_name, "whatever")                                    
role_admin=tables.Roles(name='pss_admin')
role_test=tables.Roles(name='pss_user')
tables.db_handle.session.add(role_admin)
tables.db_handle.session.add(role_test)
new_pss_user = tables.PssUsers(username='test_pss_user')
new_pss_user.crypt_password('password')
tables.db_handle.session.add(new_pss_user)
new_pss_user.roles.append(role_admin)
new_pss_user.roles.append(role_test)
tables.db_handle.session.commit()

    
