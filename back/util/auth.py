from flask_login import current_user,LoginManager,_get_user
from flask_principal import identity_loaded, RoleNeed, UserNeed


def generate_user_loader(app):    
    @app.login_manager.user_loader    
    def load_user(userid):    
        return app.tables.User.query.get(int(userid))
    return load_user
    
    
def generate_identity_loaded(app):
    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        """Set up the Flask-Principal stuff for this user"""        
        if current_user.is_anonymous():            
            return
        identity.user = current_user
        identity.provides.add(UserNeed(current_user.user_id))
                    
        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))
    return on_identity_loaded
