from app.util.app_build import get_meta_admin_app, get_admin_app
from app.util.dispatch import PathDispatcher

App = PathDispatcher(get_meta_admin_app(), get_admin_app)

