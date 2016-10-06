from app.blueprints import admin_login_blueprint
from flask import jsonify,current_app,request
import json
from werkzeug.exceptions import BadRequest,Conflict
from app.util import db_util

@admin_login_blueprint.route('/user',methods=['POST'])
def route_add_user():
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)

    input_data = json.loads(request.data)
    for key in ['username','password']:
        if key not in input_data:
            raise BadRequest("You did not specify a username and/or a password")        
    user = tables.User.query.filter_by(username=input_data['username']).first()
    if user is not None:
        raise Conflict('Duplicate username')
    new_user = tables.User(
        username=input_data['username']        
    )
    new_user.crypt_password(input_data['password'])
    #if 'roles' not in user_data:
    #    abort(422)        
    db.session.add(new_user)
    #for role_id,role_name in user_data['roles'].iteritems():
    #    role = Role.query.filter_by(role_id=role_id).first()
    #    if role is not None:            
    #        new_user.roles.append(role)
    #    else:
    #        abort(422)
    db.session.commit()                        
    return jsonify(new_user.to_dict_simple())
    
