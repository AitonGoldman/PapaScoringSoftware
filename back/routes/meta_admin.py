from flask import jsonify,current_app,request, Flask
from blueprints import meta_admin_blueprint
from util import db_util, td_config
from util.db_info import DbInfo
from util.permissions import Admin_permission
from time import sleep
import json

def generate_test_user(username,dummy_app,db_handle,roles=[]):
    
    user = dummy_app.tables.User(
        username=username        
    )
    user.crypt_password(username)
    db_handle.session.add(user)
    db_handle.session.commit()
    user = dummy_app.tables.User.query.filter_by(username=username).first()
    for role in roles:
        role = dummy_app.tables.Role.query.filter_by(name=role).first()        
        user.roles.append(role)
        db_handle.session.commit()


@meta_admin_blueprint.route('/meta_admin/db',methods=['PUT'])
def route_meta_admin_wipe_db():    
    db_config = td_config.get_db_config()    
    db_info = DbInfo(db_config)            
    db_util.drop_database('test',db_info)
    return jsonify({'data':'test'})    
        
@meta_admin_blueprint.route('/meta_admin/db',methods=['POST'])
def route_meta_admin_create_db():    
    dummy_app = Flask('dummy_app')    
    db_config = td_config.get_db_config()    
    db_info = DbInfo(db_config)            
    db_util.create_db_and_tables(dummy_app, 'test', db_info , drop_tables=True)        
    db_handle = dummy_app.tables.db_handle
    for role in ['admin','desk','scorekeeper','void']:
        db_handle.session.add(dummy_app.tables.Role(name=role))
        db_handle.session.commit()
    
    generate_test_user('test_admin',dummy_app, db_handle,['admin','scorekeeper','desk','void'])            
    generate_test_user('test_scorekeeper',dummy_app, db_handle,['scorekeeper','void'])                
    generate_test_user('test_desk',dummy_app, db_handle,['desk','void'])            
    db_handle.engine.dispose()
    del dummy_app
    return jsonify({'data':'test'})    

@meta_admin_blueprint.route('/meta_admin/healthcheck',methods=['GET'])
def route_meta_admin_health_check():    
    return jsonify({'data':'METAADMIN_HEALTHY'})    
