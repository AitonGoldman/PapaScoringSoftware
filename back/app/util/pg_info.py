#FIXME : rename as DbInfo
class PgInfo():
    def __init__(self,pg_username=None,pg_password=None,pg_hostname=None,use_sqlite=False):
        self.pg_username=pg_username
        self.pg_password=pg_password
        self.pg_hostname=pg_hostname
        self.use_sqlite=use_sqlite

def build_PgInfo_from_config(secret_config,public_config):
    if 'sqlite' not in public_config:
        public_config['sqlite']=False
    new_pg_info = PgInfo()
    if 'pg_username' in  secret_config and 'pg_password' in secret_config:
        new_pg_info.pg_username=secret_config['pg_username']
        new_pg_info.pg_password=secret_config['pg_password']
    new_pg_info.use_sqlite=public_config['sqlite']
    return new_pg_info
    
