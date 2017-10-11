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
            if 'pss_admin' in cookie_credentials and 'cookie_counts' in cookie_credentials['pss_admin']:
                cookie_counts = cookie_credentials['pss_admin']['cookie_counts']
                current_user.cookie_counts=json.dumps(cookie_counts)
                print current_user.cookie_counts
                current_app.tables.db_handle.session.commit()
        return f(*args,**kwargs)
    return new_f


