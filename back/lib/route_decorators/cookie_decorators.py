from functools import wraps
from flask import current_app,request
from flask_login import current_user
import json
import urllib

def process_cookie_counts(f):
    @wraps(f)
    def new_f(*args,**kwargs):
        raw_cookie = request.cookies.get('credentials_cookie')
        if raw_cookie:
            cookie_credentials = json.loads(urllib.unquote(raw_cookie))
            if 'pss_admin' in cookie_credentials and 'wizard_stack_indexes' in cookie_credentials['pss_admin']:                
                current_user.wizard_stack_indexes = json.dumps(cookie_credentials['pss_admin']['wizard_stack_indexes'])
                current_app.tables.db_handle.session.commit()
        return f(*args,**kwargs)
    return new_f


