from flask import Flask
from lib_v2.PssConfig  import PssConfig
from lib_v2.TableProxy import TableProxy
import os,sys
from lib import bootstrap,roles_constants,orm_factories

if len(sys.argv) > 1:
    db_name=sys.argv[1]
else:
    print "didn't specify db name..."
    sys.exit(1)

os.environ['pss_db_name']=db_name
pss_config = PssConfig()

real_app = Flask('dummy')

pss_config.get_db_info().create_db_and_tables(real_app,True)
db_handle = pss_config.get_db_info().create_db_handle(real_app)
#tables = pss_config.get_db_info().getImportedTables(real_app,'pss_admin')
table_proxy=TableProxy()
table_proxy.initialize_tables(db_handle)
#bootstrap.bootstrap_pss_admin_event(tables,'pss_admin')
#bootstrap.bootstrap_roles(tables)

table_proxy.create_user('test_pss_admin_user',
                        'test_first_name',
                        'test_last_name',
                        'password',
                        event_creator=True,
                        commit=True)

if len(sys.argv) == 1:
    sys.exit()

#pss_config.get_db_info().load_machines_from_json(real_app,test=False)

