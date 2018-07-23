from flask import Flask
from lib_v2.PssConfig  import PssConfig
from lib_v2.TableProxy import TableProxy
import os,sys
from lib_v2 import bootstrap,roles_constants

if len(sys.argv) > 1:
    db_name=sys.argv[1]
    admin_password=sys.argv[2]    
else:
    print "didn't specify db name..."
    sys.exit(1)

os.environ['pss_db_name']=db_name
pss_config = PssConfig()

real_app = Flask('dummy')

pss_config.get_db_info().create_db_and_tables(real_app,True)
db_handle = pss_config.get_db_info().create_db_handle(real_app)
table_proxy=TableProxy()
table_proxy.initialize_tables(db_handle)
#bootstrap.bootstrap_pss_admin_event(tables,'pss_admin')
#bootstrap.bootstrap_roles(tables)
table_proxy.create_role(roles_constants.TOURNAMENT_DIRECTOR)
table_proxy.create_role(roles_constants.SCOREKEEPER)
table_proxy.create_role(roles_constants.DESKWORKER)

table_proxy.create_user('test_user_admin',
                        'test_first_name',
                        'test_last_name',
                        admin_password,
                        event_creator=True,
                        commit=True)

pss_config.get_db_info().load_machines_from_json(real_app,test=False,table_proxy=table_proxy)

