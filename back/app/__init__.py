"""
This is what gets called by gunicorn when it starts up a worker thread.  
Specifically, gunicorn users the PathDispatcher to process all incoming requests.
"""

from lib.flask_lib.dispatch import PathDispatcher
from lib.PssConfig import PssConfig
from lib.DbInfo import DbInfo


pss_config = PssConfig()
pss_config.get_db_info().check_database_exists()
App = PathDispatcher()

