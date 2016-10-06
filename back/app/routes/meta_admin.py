from flask import jsonify
from app.blueprints import meta_admin_blueprint
from werkzeug.exceptions import BadRequest

@meta_admin_blueprint.route('/meta_admin')
def route_meta_admin():
    print "hi there"
    return jsonify({})
    

# @default_blueprint.route('/', defaults={'path': ''})
# @default_blueprint.route('/<path:path>')
# def catch_all(path):
#     raise BadRequest('The event you are trying to access does not exist')            
