from dispatch import PathDispatcher
import pss_config
from lib import db_util
from lib.db_info import DbInfo

pss_config.check_db_connection_env_vars_set()
#FIXME : instance config should be a class with methods to do all this shit (here and in dispatch and app_build)
instance_config = pss_config.get_pss_instance_config()                                
db_info = DbInfo(instance_config)    
db_util.check_database_exists(instance_config,db_info)
App = PathDispatcher()

