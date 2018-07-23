from flask import Flask
from lib.PssConfig  import PssConfig
from pss_models import ImportedTables
import os,sys
from lib import bootstrap,roles,orm_factories

if len(sys.argv) > 1:
    db_name=sys.argv[1]
else:
    print "didn't specify db name..."
    sys.exit(1)

os.environ['pss_db_name']=db_name
pss_config = PssConfig()

real_app = Flask('pss_admin')
tables = pss_config.get_db_info().getImportedTables(real_app,'pss_admin')
real_app.tables=tables
metadata = real_app.tables.db_handle.metadata
metadata.reflect(tables.db_handle.engine)
all_tables = metadata.tables.keys()
for event in tables.Events.query.all():
    #if event.name 
    #FIXME : make this do something
    pass
