from dispatch import PathDispatcher
import pss_config

pss_config.check_db_connection_env_vars_set()
App = PathDispatcher()

