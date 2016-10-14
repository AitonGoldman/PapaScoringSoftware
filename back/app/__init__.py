from app.util import app_build 
from app.util.dispatch import PathDispatcher
#FIXME : this should be moved to a different module path from the utils, so that it doesn't get loaded
#        everytime we include one of the submodules
App = PathDispatcher(app_build.get_meta_admin_app, app_build.get_admin_app)

