from lib import db_util
from flask import Flask
from lib.db_info import DbInfo
from pss_models import ImportedTables
import os,sys

def get_db_config():
    return {"DB_TYPE":os.getenv('DB_TYPE',None),
            "DB_USERNAME":os.getenv('DB_USERNAME',None),
            "DB_PASSWORD":os.getenv('DB_PASSWORD',None)
    }    


if len(sys.argv) > 1:
    db_name=sys.argv[1]
else:
    print "didn't specify db name..."
    sys.exit(1)


real_app = Flask('dummy_app')
# db_config = get_db_config()    
# db_info = DbInfo(db_config)    
# db_url = db_util.generate_db_url(db_name,db_info)    
# db_handle = db_util.create_db_handle(real_app,db_url)

db_util.create_db_and_tables(real_app,db_name,DbInfo({'DB_TYPE':'postgres','DB_USERNAME':os.getenv('DB_USERNAME'),'DB_PASSWORD':os.getenv('DB_PASSWORD')}),drop_tables=False)
 
    
