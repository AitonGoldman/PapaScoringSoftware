from flask import jsonify,current_app,request, Flask
from flask.ext.sqlalchemy import get_debug_queries
from app.blueprints import meta_admin_blueprint
from werkzeug.exceptions import BadRequest
from sqlalchemy_utils import create_database, database_exists
from app.util import db_util

import json

@meta_admin_blueprint.route('/meta_admin/db',methods=['POST'])
def route_meta_admin_create_db():
    dummy_app = Flask('dummy_app')
    input_data = json.loads(request.data)
    db_url = db_util.generate_db_url(input_data['db_name'])
    if not database_exists(db_url):        
        create_database(db_url)
    #FIXME : need to create dummy app to handle table creation         
    db_handle = db_util.create_db_handle(db_url,dummy_app)
    db_util.create_TD_tables(db_handle)
    db_handle.engine.dispose()
    del dummy_app
    return jsonify({'databases':[input_data['db_name']]})
    

# @default_blueprint.route('/', defaults={'path': ''})
# @default_blueprint.route('/<path:path>')
# def catch_all(path):
#     raise BadRequest('The event you are trying to access does not exist')            
