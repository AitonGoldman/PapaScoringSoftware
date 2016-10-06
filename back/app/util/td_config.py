from configobj import ConfigObj

def get_config(filename):
    return ConfigObj(filename)

def assign_loaded_config(app,public_config_filename,secret_config_filename):    
    app.td_secret_config = get_config(secret_config_filename)
    app.td_config = get_config(public_config_filename)    
    if 'flask_secret_key' not in app.td_secret_config or app.td_secret_config['flask_secret_key'] == "":
        raise Exception("You didn't configure your flask secret key!")
    app.secret_key = app.td_secret_config['flask_secret_key']

 
