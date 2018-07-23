from functools import wraps
from flask import current_app

def load_tables(f):
    @wraps(f)
    def new_f(*args,**kwargs):
        return f(current_app.tables,*args,**kwargs)
    return new_f

