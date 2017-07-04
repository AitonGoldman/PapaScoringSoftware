from blueprints import admin_login_blueprint,admin_manage_blueprint
from flask import jsonify,current_app,request
import json
from werkzeug.exceptions import BadRequest,Conflict
import os

@admin_manage_blueprint.route('/version/<version>',methods=['GET'])
def route_check_version(version):                
    return jsonify({'data':True})


