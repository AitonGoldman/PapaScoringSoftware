from flask import jsonify,current_app,request, Flask
from blueprints import meta_admin_blueprint
from util import db_util, td_config
from util.db_info import DbInfo
from util.permissions import Admin_permission
from time import sleep
#from orm_creation import create_roles, create_team
import orm_creation
import json

def create_stanard_roles_and_users(app):
    orm_creation.create_roles(app)
    orm_creation.create_user(app,'test_admin', 'test_admin',['1','2','3','4','6'])            
    orm_creation.create_user(app,'test_scorekeeper', 'test_scorekeeper',['3','4'])                
    orm_creation.create_user(app,'test_desk', 'test_desk',['2','4','6'])            

#FIXME : needs protection
#FIXME : need to pull db creation out into seperate function
@meta_admin_blueprint.route('/meta_admin/db',methods=['POST'])
def route_meta_admin_create_db():    
    dummy_app = Flask('dummy_app')
    input_data = json.loads(request.data)
    db_config = td_config.get_db_config()    
    db_util.create_db_and_tables(dummy_app, input_data['db_name'], DbInfo(db_config))
    del dummy_app
    return jsonify({'data':input_data['db_name']})    

@meta_admin_blueprint.route('/meta_admin/test_db_with_tournaments_and_player_and_team',methods=['POST'])
def route_meta_admin_create_db_and_tournaments_and_player_and_team():    
    dummy_app = Flask('dummy_app')    
    db_info = DbInfo({'DB_TYPE':'sqlite'})
    db_util.create_db_and_tables(dummy_app, 'test', db_info , drop_tables=True)
    db_url = db_util.generate_db_url('test', db_info)
    db_handle = dummy_app.tables.db_handle
    db_util.init_papa_tournaments_divisions(dummy_app.tables)
    create_stanard_roles_and_users(dummy_app)
    test_player = generate_test_player('aiton','goldman',dummy_app,db_handle)
    test_player.linked_division_id=1
    test_player_two = generate_test_player('doug','polka',dummy_app,db_handle)
    test_player.linked_division_id=1
    db_handle.session.commit()    
    orm_creation.create_team(dummy_app,{'team_name':'test_team','players':['1']})
    db_util.load_machines_from_json(dummy_app,True)
    db_handle.engine.dispose()
    del dummy_app
    return jsonify({'data':'test'})    

@meta_admin_blueprint.route('/meta_admin/test_db_with_tournaments',methods=['POST'])
def route_meta_admin_create_db_and_tournaments():    
    dummy_app = Flask('dummy_app')    
    db_info = DbInfo({'DB_TYPE':'sqlite'})
    db_util.create_db_and_tables(dummy_app, 'test', db_info , drop_tables=True)
    db_url = db_util.generate_db_url('test', db_info)
    db_handle = dummy_app.tables.db_handle
    create_stanard_roles_and_users(dummy_app)
    db_util.load_machines_from_json(dummy_app,True)
    db_util.init_papa_tournaments_divisions(dummy_app.tables)
    db_handle.engine.dispose()
    del dummy_app
    return jsonify({'data':'test'})    

@meta_admin_blueprint.route('/meta_admin/test_db_with_machines',methods=['POST'])
def route_meta_admin_create_db_and_load_machines():    
    dummy_app = Flask('dummy_app')    
    db_info = DbInfo({'DB_TYPE':'sqlite'})
    db_util.create_db_and_tables(dummy_app, 'test', db_info , drop_tables=True)
    db_url = db_util.generate_db_url('test', db_info)
    db_handle = dummy_app.tables.db_handle
    create_stanard_roles_and_users(dummy_app)
    db_util.load_machines_from_json(dummy_app,True)
    db_handle.engine.dispose()
    del dummy_app
    return jsonify({'data':'test'})    

@meta_admin_blueprint.route('/meta_admin/test_db',methods=['POST'])
def route_meta_admin_wipe_test_db():    
    dummy_app = Flask('dummy_app')    
    db_info = DbInfo({'DB_TYPE':'sqlite'})
    db_util.create_db_and_tables(dummy_app, 'test', db_info , drop_tables=True)
    db_url = db_util.generate_db_url('test', db_info)
    db_handle = dummy_app.tables.db_handle
    create_stanard_roles_and_users(dummy_app)
    db_util.load_machines_from_json(dummy_app,True)
    db_handle.engine.dispose()
    del dummy_app
    return jsonify({'data':'test'})    

@meta_admin_blueprint.route('/meta_admin/healthcheck',methods=['GET'])
def route_meta_admin_health_check():    
    return jsonify({'data':'METAADMIN_HEALTHY'})    
