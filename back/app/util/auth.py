from flask_login import current_user,LoginManager
from flask_principal import identity_loaded, RoleNeed, UserNeed

def generate_user_loader(app):    
    @app.Login_Manager.user_loader    
    def load_user(userid):    
        return app.tables.User.query.get(int(userid))

def init_login_manager(app):
    Login_Manager = LoginManager()
    Login_Manager.init_app(app)
    app.Login_Manager = Login_Manager
    generate_user_loader(app)

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

    
