from configobj import ConfigObj

def assign_loaded_config(app,public_config_filename,secret_config_filename):    
    app.td_secret_config = ConfigObj(secret_config_filename)
    app.td_config = ConfigObj(public_config_filename)    
    if 'flask_secret_key' not in app.td_secret_config or app.td_secret_config['flask_secret_key'] == "":        
        raise Exception("You didn't configure your flask secret key!")
    app.secret_key = app.td_secret_config['flask_secret_key']
    if 'sqlite' not in app.td_config:
        app.td_config['sqlite']=False
 
