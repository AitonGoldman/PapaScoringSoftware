from flask import jsonify,current_app,request, Flask
from blueprints import meta_admin_blueprint
from util import db_util, td_config
from util.db_info import DbInfo
from util.permissions import Admin_permission
from time import sleep
import orm_creation
import json
from orm_creation import RolesEnum
import orm_creation
from orm_creation import create_stanard_roles_and_users,create_queue
import os
import random

@meta_admin_blueprint.route('/meta_admin/external_url/<event_name>',methods=['GET'])
def route_get_external_url(event_name):        
    event_file = open('/var/www/html/replay_2017/'+event_name+'.json') 
    event_file_contents = event_file.read()
    event_file.close()
    
    input_data = json.loads(event_file_contents)
    #print input_data
    return jsonify({'data':input_data})    
    #return jsonify({})


@meta_admin_blueprint.route('/meta_admin/events',methods=['GET'])
def route_get_list_of_events():        
    event_file = open(current_app.td_config['EVENT_FILE_PATH']) 
    event_file_contents = event_file.read()
    event_file.close()
    
    input_data = json.loads(event_file_contents)
    #print input_data
    return jsonify({'data':input_data})    
    #return jsonify({})

@meta_admin_blueprint.route('/meta_admin/test_db_with_tournaments/players/<int:init_players>',methods=['POST'])
def route_meta_admin_create_db_and_tournaments(init_players):    
    dummy_app = Flask('dummy_app')    
    db_config = td_config.get_db_config()    
    db_info = DbInfo(db_config)            
    db_util.create_db_and_tables(dummy_app, 'test', db_info , drop_tables=True)    
    db_handle = dummy_app.tables.db_handle
    create_stanard_roles_and_users(dummy_app)
    db_util.load_machines_from_json(dummy_app)
    orm_creation.init_papa_tournaments_divisions(dummy_app)
    orm_creation.init_papa_tournaments_division_machines(dummy_app)        
    if init_players == 1:
        orm_creation.init_papa_players(dummy_app,short=True,number_of_a_players=200)
    
    db_handle.engine.dispose()
    del dummy_app
    return jsonify({'data':'test'})    

@meta_admin_blueprint.route('/meta_admin/test_db_wipe',methods=['POST'])
def route_meta_admin_wipe_test_db():        
    db_config = td_config.get_db_config()    
    db_info = DbInfo(db_config)            
    db_util.drop_database('test',db_info)
    return jsonify({'data':'test'})    

@meta_admin_blueprint.route('/meta_admin/healthcheck',methods=['GET'])
def route_meta_admin_health_check():    
    return jsonify({'data':'METAADMIN_HEALTHY'})    
