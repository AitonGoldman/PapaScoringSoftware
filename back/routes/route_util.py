from blueprints import admin_manage_blueprint
from flask import jsonify, current_app


@admin_manage_blueprint.route('/util/healthcheck',methods=['GET'])
def route_healthcheck():
    users = [u.to_dict_simple() for u in current_app.tables.User.query.all()]                        
    return jsonify({'data':{'status':'HEALTHY','user_count':len(users)}})
