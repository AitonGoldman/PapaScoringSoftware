from flask import Blueprint, render_template, abort, Flask
from jinja2 import TemplateNotFound
from sqlalchemy_utils import create_database, database_exists
from app import td_public,td_secret
from app.util import db_util
from app.util.dispatch import PathDispatcher
import os
from app.types import ImportedTables

admin_login_blueprint = Blueprint('admin_login',__name__)
from app import routes


if not hasattr(td_secret,'flask_secret_key') or td_secret.flask_secret_key=="":
    raise Exception("You didn't configure your flask secret key!")

# FIXME : need to handle loading secrets seperately for each app
# FIXME : need to check master db for db names before automatically creating
def get_admin_app(name):
    app = Flask(name)
    app.config.from_pyfile('app/td_flask.py')
    app.register_blueprint(admin_login_blueprint)
    db_url="postgresql://tom:tomPassword@localhost/%s" % name
    if not database_exists(db_url):        
        create_database(db_url)        
    db_handle = db_util.create_db_handle(db_url,name,app)        
    app.tables = ImportedTables(db_handle)
    if db_util.check_table_exists(db_handle) is False:
        db_util.create_TD_tables(app.tables.db_handle)        
    
    return app


App = PathDispatcher(None, get_admin_app)
