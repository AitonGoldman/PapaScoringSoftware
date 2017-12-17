import routes_v2
from lib_v2.PssConfig import PssConfig
from lib_v2 import app_build
from flask import Flask
test_app=None

def static_setup(db_name):
    global test_app    
    if test_app is None:                
        pss_config = PssConfig()                        
        pss_config.get_db_info(db_name=db_name).create_db_and_tables(Flask('pss'),True)        
        #FIXME : bleh - need to add an argument to app_builder so that it takes a db_name        
        test_app = app_build.build_app(Flask('pss'))        
        pss_config.get_db_info(db_name=db_name).load_machines_from_json(test_app,True)
