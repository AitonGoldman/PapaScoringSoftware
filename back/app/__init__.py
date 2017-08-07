from lib.flask_lib.dispatch import PathDispatcher
from lib.PssConfig import PssConfig
from lib.DbInfo import DbInfo


pss_config = PssConfig()
pss_config.get_db_info().check_database_exists()
App = PathDispatcher()

