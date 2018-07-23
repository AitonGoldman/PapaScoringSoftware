from blueprints import admin_login_blueprint,admin_manage_blueprint
from flask import jsonify,current_app,request
import json
from werkzeug.exceptions import BadRequest,Conflict
from util import db_util
from util.permissions import Admin_permission
from flask_login import login_required,current_user
from routes.utils import fetch_entity

@admin_manage_blueprint.route('/machine',methods=['GET'])
def route_get_machines():
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    machines = tables.Machine.query.all()
    return jsonify({'data': {machine.machine_id:machine.to_dict_simple() for machine in machines}})
