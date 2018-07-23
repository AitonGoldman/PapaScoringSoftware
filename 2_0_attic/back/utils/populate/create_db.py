from util import db_util
from flask import Flask
from util.db_info import DbInfo
from util import td_config
from routes.orm_creation import create_stanard_roles_and_users, init_papa_players
from td_types import ImportedTables

import os,sys
real_app = Flask('dummy_app')
if len(sys.argv) > 1:
    poop_db_name=sys.argv[1]
else:
    print "didn't specify db name..."
    sys.exit(1)
if len(sys.argv) > 2:
    real_app = Flask(sys.argv[1])
    db_config = td_config.get_db_config()
    db_info = DbInfo(db_config)
    db_url = db_util.generate_db_url(sys.argv[1],db_info)
    db_handle = db_util.create_db_handle(db_url, real_app)
    real_app.tables = ImportedTables(db_handle)

    init_papa_players(real_app)
else:
    db_util.create_db_and_tables(real_app,poop_db_name,DbInfo({'DB_TYPE':'postgres','DB_USERNAME':os.getenv('DB_USERNAME'),'DB_PASSWORD':os.getenv('DB_PASSWORD')}),drop_tables=False)
    create_stanard_roles_and_users(real_app)
    db_util.load_machines_from_json(real_app)
    
