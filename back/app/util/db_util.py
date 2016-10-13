from sqlalchemy_utils import create_database, database_exists
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine.reflection import Inspector
from app.types import ImportedTables

def create_db_and_tables(app, db_name, use_sqlite=False, drop_tables=False):    
    db_url = generate_db_url(db_name, use_sqlite)
    if not database_exists(db_url):        
        create_database(db_url)
    #FIXME : need to create dummy app to handle table creation         
    db_handle = create_db_handle(db_url,app)        
    app.tables = ImportedTables(db_handle)
    create_TD_tables(db_handle, drop_tables=drop_tables)
    db_handle.engine.dispose()

def create_db_handle(db_url,flask_app):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_url    
    db_handle = SQLAlchemy(flask_app)
    return db_handle

def create_db_handle_no_app():
    db_handle = SQLAlchemy()
    return db_handle


def create_TD_tables(db_handle,drop_tables=False):
    db_handle.reflect()
    if drop_tables:
        db_handle.drop_all()
    print db_handle.create_all()    

def check_table_exists(db_handle):
    db_handle.reflect()    
    if "role" in db_handle.metadata.tables:        
        return True
    else:
        return False

# FIXME : need to generate db_url by comparing "name" to good list of dbs
def generate_db_url(db_name, use_sqlite=False):
    if use_sqlite:
        return "sqlite:////tmp/%s.db" % db_name
    else:
        return "postgresql://tom:tomPassword@localhost/%s" % db_name

def app_db_handle(app):
    return app.tables.db_handle

def app_db_tables(app):
    return app.tables


def check_if_ranking_funcs_exists(db_handle):
    result = db_handle.execute("SELECT prosrc FROM pg_proc WHERE proname = 'papa_scoring_func';")
    if not result.fetchone():
        DB.engine.execute("CREATE FUNCTION papa_scoring_func(rank real) RETURNS real AS $$ BEGIN IF rank = 1 THEN RETURN 100; ELSIF rank = 2 THEN RETURN 90; ELSIF rank = 3 THEN RETURN 85; ELSIF rank < 88 THEN  RETURN 100-rank-12; ELSIF rank >= 88 THEN RETURN 0; END IF; END; $$ LANGUAGE plpgsql;")
        DB.engine.execute("CREATE FUNCTION papa_scoring_finals_func(rank real) RETURNS real AS $$  BEGIN IF rank = 1 THEN RETURN 3; ELSIF rank = 2 THEN RETURN 2; ELSIF rank = 3 THEN RETURN 1; ELSIF rank = 4 THEN RETURN 0; END IF; END; $$ LANGUAGE plsgsql;")    
