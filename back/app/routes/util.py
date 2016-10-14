from app.blueprints import admin_manage_blueprint
from flask import jsonify

@admin_manage_blueprint.route('/util/healthcheck',methods=['GET'])
def route_healthcheck():    
    return jsonify({'data':'HEALTHY'})
