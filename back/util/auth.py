from flask_login import current_user,LoginManager,_get_user
from flask_principal import identity_loaded, RoleNeed, UserNeed
from flask import current_app

def generate_user_loader(app):    
    @app.login_manager.user_loader    
    def load_user(userid):
        if current_app.td_config['PLAYER_LOGIN'] == "1":
            return app.tables.Player.query.get(int(userid))
        else:
            return app.tables.User.query.get(int(userid))
    return load_user
    
    
def generate_identity_loaded(app):
    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        """Set up the Flask-Principal stuff for this user"""        
        if current_user.is_anonymous():            
            return
        if hasattr(current_user,'player_id'):
            identity.provides.add(UserNeed(current_user.player_id))            
        else:
            identity.provides.add(UserNeed(current_user.user_id))
        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))
    return on_identity_loaded
