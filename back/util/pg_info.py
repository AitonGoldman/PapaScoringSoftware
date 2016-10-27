#FIXME : rename as DbInfo
class PgInfo():
    def __init__(self,pg_username=None,pg_password=None,pg_hostname=None,use_sqlite=False):
        self.pg_username=pg_username
        self.pg_password=pg_password
        self.pg_hostname=pg_hostname
        self.use_sqlite=use_sqlite

def build_PgInfo_from_config(secret_config,public_config):
    #FIXME : need to deal with pg hostname
    #FIXME : do config objects parse True/False properly?
    new_pg_info = PgInfo()
    if 'pg_username' in  secret_config and 'pg_password' in secret_config:
        new_pg_info.pg_username=secret_config['pg_username']
        new_pg_info.pg_password=secret_config['pg_password']
    if 'sqlite' not in public_config or public_config['sqlite'] is not True:
        raise Exception('Can not make PgInfo without pg username and pg password')        
    
    new_pg_info.use_sqlite=public_config['sqlite']
    return new_pg_info
    
