from app.blueprints import default_blueprint
from werkzeug.exceptions import BadRequest

@default_blueprint.route('/metadmin')
def catch_all(path):
    return jsonify({'state':'metadmin'})
    

@default_blueprint.route('/', defaults={'path': ''})
@default_blueprint.route('/<path:path>')
def catch_all(path):
    raise BadRequest('The event you are trying to access does not exist')            
