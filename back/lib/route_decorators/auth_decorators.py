from functools import wraps
from flask import current_app
from flask_login import current_user
from werkzeug.exceptions import Unauthorized

def check_current_user_is_active(f):
    @wraps(f)
    def new_f(*args,**kwargs):
        if current_user.is_active() is False:
            raise Unauthorized('Player is not active')
        return f(*args,**kwargs)
    return new_f

