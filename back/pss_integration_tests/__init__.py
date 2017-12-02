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
        test_app = app_build.build_app(Flask('pss'))
        
