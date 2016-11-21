from werkzeug.exceptions import BadRequest

def fetch_entity(model_class,model_id):
    found_entity = model_class.query.get(model_id)    
    if found_entity is None:        
        error_arg_list = (model_id, model_class.__name__, model_class.__name__, model_id)
        raise BadRequest("Expecting url param %s with valid %s id but could not find valid %s with id %s" % error_arg_list)
    return found_entity

def check_roles_exist(tables, roles):
    for role_id in roles:
        existing_role = tables.Role.query.filter_by(role_id=role_id).first()
        if existing_role is None:            
            raise BadRequest('Role with id %s does not exist' % role_id)
