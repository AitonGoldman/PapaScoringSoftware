from util import db_util
from flask import Flask
from util.db_info import DbInfo
import os,sys
dummy_app = Flask('dummy_app')                
if len(sys.argv) > 1:
    poop_db_name=sys.argv[1]
else:
    print "didn't specify db name..."
    sys.exit(1)
db_util.create_db_and_tables(dummy_app,poop_db_name,DbInfo({'DB_TYPE':'postgres','DB_USERNAME':os.getenv('DB_USERNAME'),'DB_PASSWORD':os.getenv('DB_PASSWORD')}),drop_tables=False)
