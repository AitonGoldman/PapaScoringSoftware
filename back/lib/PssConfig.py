from configobj import ConfigObj
import os 
import lib
from lib.DbInfo import DbInfo
class PssConfig():    
    def __init__(self):
        self.db_info = DbInfo(
            os.getenv('db_type',None),
            os.getenv('db_username',None),
            os.getenv('db_password',None),
            os.getenv('pss_db_name',None)            
        )
        self.pss_admin_event_name=os.getenv('pss_admin_event_name','pss_admin')            

    def get_db_info(self,db_name=None):
        if db_name:
            self.db_info.db_name=db_name
        return self.db_info
    
    def get_event_config_from_db(self, app):
        config_dict={}
        for event in app.tables.Events.query.all():                
            if event.name == app.name:
                #FIXME : this could be much prettier
                columns_dict = event.__dict__
                columns_dict.pop('_sa_instance_state',None)                
                for param in columns_dict.keys():                    
                    config_dict[param]=getattr(event,param)
                return config_dict
        return None
    
    def set_event_config_from_db(self, app):            
        config_dict = self.get_event_config_from_db(app)            
        if config_dict is None:
            raise Exception('event %s does not exist' % app.name)    
        app.event_config = config_dict        
        if 'flask_secret_key' not in app.event_config or app.event_config['flask_secret_key'] is None:
            raise Exception("You didn't configure your flask secret key!")    
        app.secret_key = app.event_config['flask_secret_key']
        for key,value in app.event_config.iteritems():
            if os.getenv(key,None):
                app.event_config[key]=os.getenv(key)
        return config_dict
        
