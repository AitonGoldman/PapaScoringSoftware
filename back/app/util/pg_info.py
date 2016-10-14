class PgInfo():
    def __init__(self,pg_username,pg_password,pg_hostname):
        self.pg_username=pg_username
        self.pg_password=pg_password
        self.pg_hostname=pg_hostname

def build_PgInfo(app):
    if 'sqlite' in app.td_config and app.td_config['sqlite'] is True:
        return None
    #FIXME : make it possible to specify any db - don't just assume postgres
    if 'pg_username' in  app.td_secret_config and 'pg_password' in app.td_secret_config:
        pg_info = PgInfo(app.td_secret_config['pg_username'],
                         app.td_secret_config['pg_password'],
                         None)
    else:
        pg_info = None
        
    return pg_info
