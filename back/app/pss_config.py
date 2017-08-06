from configobj import ConfigObj
import os 
import lib


def get_empty_config_dict():
    config_dict = {}
    config_dict['flask_secret_key']=None
    config_dict['number_unused_tickets_allowed']=15
    config_dict['stripe_api_key']=None
    config_dict['stripe_public_key']=None    
    config_dict['queue_bump_amount']=1    
    config_dict['ionic_profile']=None
    config_dict['ionic_api_key']=None    
    #config_dict['EVENT_FILE_PATH']=None
    config_dict['sendgrid_api_key']=None
    #PAY ATTENTION - THIS VALUE IS HERE TO REMIND YOU TO SET IT
    #                WHEN IT GETS USED, IT GETS PULLED STRAIGHT FROM ENV VAR
    config_dict['player_id_seq_start']=None

    return config_dict

def get_config_values_from_db(app):    
    config_dict = get_empty_config_dict()    
    for event in app.tables.Events.query.all():
        if event.name == app.name:
            for param in config_dict.keys():
                config_dict[param]=getattr(event,param)                
    return config_dict
    
def get_db_config():
    if os.getenv('DB_TYPE',None) is None or os.getenv('DB_USERNAME',None) is None or os.getenv('DB_PASSWORD',None) is None:
        #FIXME : needs to be cleaner
        pass
    
    return {"DB_TYPE":os.getenv('DB_TYPE',None),
            "DB_USERNAME":os.getenv('DB_USERNAME',None),
            "DB_PASSWORD":os.getenv('DB_PASSWORD',None)
    }    

def get_pss_instance_config():
    config = {}
    config['pss_admin_event_name']=os.getenv('pss_admin_event_name',None)
    db_config=get_db_config()
    config.update(db_config)
    return config
    
def set_event_config_from_db(app):            
    config_dict = get_config_values_from_db(app)        
    app.event_config = config_dict
    if app.event_config['flask_secret_key'] is None:
        raise Exception("You didn't configure your flask secret key!")    
    app.secret_key = app.event_config['flask_secret_key']
    return config_dict
