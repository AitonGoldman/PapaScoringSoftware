from configobj import ConfigObj
import os 
def get_configs(public_config_filename=None,
                secret_config_filename=None):
    if public_config_filename is None:
        public_config_filename=os.getenv('td_public_config_filename','app/td_public.py')
    if secret_config_filename is None:
        secret_config_filename=os.getenv('td_secret_config_filename','app/td_secret.py')
    secret_config=ConfigObj(secret_config_filename)
    public_config=ConfigObj(public_config_filename)
    if 'sqlite' not in public_config:
        public_config['sqlite']=False
    return secret_config,public_config
    
def assign_loaded_config(app,
                         public_config_filename=None,
                         secret_config_filename=None,
                         flask_config_filename=None):    
    if flask_config_filename is None:
        flask_config_filename=os.getenv('flask_config_filename',None)
        if flask_config_filename:
            app.config.from_pyfile(flask_config_filename)
    secret_config,public_config = get_configs(public_config_filename,secret_config_filename)
    app.td_secret_config = secret_config
    app.td_config = public_config
    if 'flask_secret_key' not in app.td_secret_config or app.td_secret_config['flask_secret_key'] == "":
        raise Exception("You didn't configure your flask secret key!")
    app.secret_key = app.td_secret_config['flask_secret_key']
    return secret_config,public_config
