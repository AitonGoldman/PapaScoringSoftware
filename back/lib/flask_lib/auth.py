from flask_login import current_user,LoginManager,_get_user
from flask_principal import identity_loaded, RoleNeed, UserNeed
from flask import current_app

#FIXME : generate probably not needed
def generate_pss_user_loader(app):    
    @app.login_manager.user_loader    
    def load_user(userid):
        if isinstance( userid, ( int, long ) ):
            return app.tables.PssUsers.query.get(int(userid))            
        elif "player" in userid:
            userid = userid.replace("player_","")
            return app.tables.Players.query.get(int(userid))            
    return load_user
    
def generate_pss_user_identity_loaded(app):
    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        """Set up the Flask-Principal stuff for this user"""        
        if current_user.is_anonymous():                        
            return
        #if hasattr(current_user,'player_id'):            
        #    identity.provides.add(UserNeed(current_user.player_id))            
        #else:
        ##print type(current_user).__name__
        if hasattr(current_user,'player_roles'):
            identity.provides.add(UserNeed(current_user.player_id))            
        else:
            identity.provides.add(UserNeed(current_user.pss_user_id))
        if hasattr(current_user, 'admin_roles'):
            for role in current_user.admin_roles:
                identity.provides.add(RoleNeed(role.name))
        if hasattr(current_user, 'event_roles'):
            for event_role in current_user.event_roles:
                identity.provides.add(RoleNeed(event_role.name))
        if hasattr(current_user, 'player_roles'):
            for player_role in current_user.player_roles:
                identity.provides.add(RoleNeed(player_role.name))
                
    return on_identity_loaded
