from flask import jsonify,current_app,request, Flask
from app.blueprints import meta_admin_blueprint
from app.util import db_util

import json

#FIXME : needs protection
@meta_admin_blueprint.route('/meta_admin/db',methods=['POST'])
def route_meta_admin_create_db():
    dummy_app = Flask('dummy_app')
    input_data = json.loads(request.data)
    db_util.create_db_and_tables(dummy_app, input_data['db_name'])
    del dummy_app
    return jsonify({'data':input_data['db_name']})    

@meta_admin_blueprint.route('/meta_admin/test_db',methods=['POST'])
def route_meta_admin_wipe_test_db():
    if not current_app.config['DEBUG']:
        return jsonify({'data':None})
    dummy_app = Flask('dummy_app')    
    db_util.create_db_and_tables(dummy_app, 'test', use_sqlite=True, drop_tables=True)
    del dummy_app
    return jsonify({'data':'test'})    
