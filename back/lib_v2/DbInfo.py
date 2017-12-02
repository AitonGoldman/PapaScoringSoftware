from sqlalchemy_utils import create_database, database_exists, drop_database as sql_utils_drop_database
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine.reflection import Inspector
#from pss_models import ImportedTables
from lib_v2.TableProxy import TableProxy
import os
from flask import Flask

POSTGRES_TYPE='postgres'
SQLITE_TYPE='sqlite'

class DbInfo():    
    def __init__(self,
                 db_type,
                 db_username,
                 db_password,
                 db_name,
                 db_host_and_port=None):
        if db_type is None or db_username is None or db_password is None or db_name is None:            
            raise Exception('tried to create DbInfo without enough connection information')
        if db_type in [POSTGRES_TYPE,SQLITE_TYPE]:
            self.db_type = db_type
        else:
            raise Exception('Unknown type of database passed into DbInfo contructor')
        self.db_username=db_username
        self.db_password=db_password
        self.db_name=db_name
        
        if db_host_and_port:
            self.db_host=db_host_and_port
        else:
            self.db_host='localhost'
    
    # FIXME : need to generate db_url by comparing "name" to good list of dbs
    def generate_db_url(self):
        if self.db_type == SQLITE_TYPE:
            db_url= "sqlite:////tmp/%s.db" % self.db_name    
        if self.db_type == POSTGRES_TYPE:
            db_url="postgresql://%s:%s@localhost/%s" % (self.db_username,self.db_password,self.db_name)
        return db_url

    def check_database_exists(self):        
        db_url = self.generate_db_url()
        if not database_exists(db_url):        
            raise Exception('You are trying to access a database that does not exist')

    def getImportedTablesForEvent(self, event_name):
        app=Flask(event_name)
        db_handle=self.create_db_handle(app)
        app.tables = ImportedTables(db_handle,event_name,"pss_admin")
        return app        
    
    def create_db_handle(self,flask_app):
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = self.generate_db_url()    
        db_handle = SQLAlchemy(flask_app)
        return db_handle

    def create_db_and_tables(self, app, drop_tables=False):            
        db_url = self.generate_db_url()                
        if not database_exists(db_url):
            create_database(db_url)
        db_handle = self.create_db_handle(app)
        if self.db_type == POSTGRES_TYPE:
            self.check_if_ranking_funcs_exists(db_handle)
        #app.tables = ImportedTables(db_handle,app.name,None)
        app.tables = TableProxy()
        app.tables.initialize_tables(db_handle)
        self.create_PSS_tables(db_handle, drop_tables=drop_tables)
        db_handle.engine.dispose()

    def create_PSS_tables(self, db_handle,drop_tables=False):
        db_handle.reflect()
        if drop_tables:            
            db_handle.drop_all()            
            db_handle.session.commit()            
        db_handle.create_all()            
        
    def check_if_ranking_funcs_exists(self,db_handle):    
        result = db_handle.engine.execute("SELECT prosrc FROM pg_proc WHERE proname = 'papa_scoring_func';")
        if not result.fetchone():
            db_handle.engine.execute("CREATE FUNCTION papa_scoring_func(rank real) RETURNS real AS $$ BEGIN IF rank = 1 THEN RETURN 100; ELSIF rank = 2 THEN RETURN 90; ELSIF rank = 3 THEN RETURN 85; ELSIF rank < 88 THEN  RETURN 100-rank-12; ELSIF rank >= 88 THEN RETURN 0; END IF; END; $$ LANGUAGE plpgsql;")

    def getImportedTables(self,app,pss_admin_site_name):
        db_handle = self.create_db_handle(app)
        return ImportedTables(db_handle,app.name,pss_admin_site_name)

    def load_machines_from_json(self,app,test=False):            
        from data_files.machine_list_abbreviations import machines
        from data_files.machine_list_test import test_machines

        machines_to_load = machines
        if test:
            machines_to_load = test_machines
        for machine in machines_to_load:
            if app.tables.Machines.query.filter_by(machine_name=machine['machine_name']).first():
                continue
            new_machine = app.tables.Machines(
                machine_name=machine['machine_name']
            )
            if 'abbreviation' in machine:
                new_machine.abbreviation = machine['abbreviation']
            else:
                new_machine.abbreviation = machine['machine_name'][0:4]
            
            app.tables.db_handle.session.add(new_machine)
        app.tables.db_handle.session.commit()
    
    
# def load_machines_from_json(app,test=False):    
#     from data_files.machine_list import machines
#     from data_files.machine_list_abbreviations import machines
#     from data_files.machine_list_test import test_machines

#     machines_to_load = machines
#     if test:
#         machines_to_load = test_machines
#     for machine in machines_to_load:
#         new_machine = app.tables.Machine(
#             machine_name=machine['machine_name']
#         )
#         if 'abbreviation' in machine:
#             new_machine.abbreviation = machine['abbreviation']

#         app.tables.db_handle.session.add(new_machine)
#         app.tables.db_handle.session.commit()
#         pass
        
    
# def drop_database(db_name,db_info):
#     db_url = generate_db_url(db_name, db_info)
#     sql_utils_drop_database(db_url)
    
# def create_db_and_tables(app, db_name, db_info, drop_tables=False):    
#     db_url = generate_db_url(db_name, db_info)
#     if not database_exists(db_url):        
#         create_database(db_url)
#     db_handle = create_db_handle(app,db_url)
#     if db_info.db_type == 'postgres':
#         check_if_ranking_funcs_exists(db_handle)
#     app.tables = ImportedTables(db_handle,db_name,None)
#     create_TD_tables(db_handle, drop_tables=drop_tables)
#     db_handle.engine.dispose()

# def create_db_handle(flask_app,db_url):
#     flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_url    
#     db_handle = SQLAlchemy(flask_app)
#     return db_handle
    
# def create_db_handle_no_app():
#     db_handle = SQLAlchemy()
#     return db_handle

# def create_TD_tables(db_handle,drop_tables=False):
#     db_handle.reflect()
#     if drop_tables:
#         db_handle.drop_all()
#         db_handle.session.commit()
#     db_handle.create_all()    

# def check_database_exists(instance_config,db_info):
#     #db_info = DbInfo(instance_config)    
#     db_url = generate_db_url(instance_config['pss_db_name'],db_info)
#     if not database_exists(db_url):        
#         raise Exception('You are trying to access a database that does not exist')                                            

# def check_table_exists(db_handle):
#     db_handle.reflect()    
#     if "role" in db_handle.metadata.tables:        
#         return True
#     else:
#         return False

# # FIXME : need to generate db_url by comparing "name" to good list of dbs
# def generate_db_url(db_name, db_info):
#     if db_name is None or db_name == "":
#         raise Exception("No db name specified while generating db url")

#     if db_info is None :
#         raise Exception("Missing postgress username or password while trying to build db url")       
#     if db_info.is_sqlite():
#         db_url= "sqlite:////tmp/%s.db" % db_name    
#     if db_info.is_postgres():        
#         db_url="postgresql://%s:%s@localhost/%s" % (db_info.db_username,db_info.db_password,db_name)
#     return db_url
            
# def app_db_handle(app):    
#     return app.tables.db_handle

# def app_db_tables(app):
#     return app.tables


# def check_if_ranking_funcs_exists(db_handle):    
#     result = db_handle.engine.execute("SELECT prosrc FROM pg_proc WHERE proname = 'papa_scoring_func';")
#     if not result.fetchone():
#         db_handle.engine.execute("CREATE FUNCTION papa_scoring_func(rank real) RETURNS real AS $$ BEGIN IF rank = 1 THEN RETURN 100; ELSIF rank = 2 THEN RETURN 90; ELSIF rank = 3 THEN RETURN 85; ELSIF rank < 88 THEN  RETURN 100-rank-12; ELSIF rank >= 88 THEN RETURN 0; END IF; END; $$ LANGUAGE plpgsql;")
        

    
        
