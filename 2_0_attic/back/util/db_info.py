#FIXME : rename as DbInfo
class DbInfo():
    def __init__(self, db_config):
        self.db_username=db_config['DB_USERNAME'] if 'DB_USERNAME' in db_config else None
        self.db_password=db_config['DB_PASSWORD'] if 'DB_PASSWORD' in db_config else None
        self.db_hostname=None
        self.db_type=db_config['DB_TYPE']
        if self.db_type == 'postgres' and (self.db_username is None or self.db_password is None):
            raise Exception('DbInfo needs db username and db password')

    def is_sqlite(self):
        return True if self.db_type == 'sqlite' else False

    def is_postgres(self):
        return True if self.db_type == 'postgres' else False
        
    
