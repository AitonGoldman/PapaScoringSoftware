from sqlalchemy_utils import create_database, database_exists
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine.reflection import Inspector


def create_db_handle(db_url,db_name,flask_app):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_url    
    db_handle = SQLAlchemy(flask_app)
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
        
def check_if_ranking_funcs_exists(db_handle):
    result = db_handle.execute("SELECT prosrc FROM pg_proc WHERE proname = 'papa_scoring_func';")
    if not result.fetchone():
        DB.engine.execute("CREATE FUNCTION papa_scoring_func(rank real) RETURNS real AS $$ BEGIN IF rank = 1 THEN RETURN 100; ELSIF rank = 2 THEN RETURN 90; ELSIF rank = 3 THEN RETURN 85; ELSIF rank < 88 THEN  RETURN 100-rank-12; ELSIF rank >= 88 THEN RETURN 0; END IF; END; $$ LANGUAGE plpgsql;")
        DB.engine.execute("CREATE FUNCTION papa_scoring_finals_func(rank real) RETURNS real AS $$  BEGIN IF rank = 1 THEN RETURN 3; ELSIF rank = 2 THEN RETURN 2; ELSIF rank = 3 THEN RETURN 1; ELSIF rank = 4 THEN RETURN 0; END IF; END; $$ LANGUAGE plsgsql;")    
