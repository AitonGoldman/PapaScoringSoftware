from werkzeug.exceptions import BadRequest

def fetch_entity(model_class,model_id):
    found_entity = model_class.query.get(model_id)
    if found_entity is None:
        error_arg_list = (model_id, model_class.__name__, model_class.__name__, model_id)
        raise BadRequest("Expecting url param %s with valid %s id but could not find valid %s with id %s" % error_arg_list)
    return found_entity
