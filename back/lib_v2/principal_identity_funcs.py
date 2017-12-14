from flask_principal import identity_loaded
from flask_login import current_user
from lib_v2 import needs,roles_constants

def generate_pss_user_loader(app):
    @app.login_manager.user_loader    
    def load_user(userid):        
        if isinstance( userid, ( int, long ) ):
            return app.table_proxy.PssUsers.query.get(int(userid))            
        elif "player" in userid:
            userid = userid.replace("player_","")
            return app.table_proxy.Players.query.get(int(userid))            
    return load_user

def generate_pss_user_identity_loaded(app):
    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        """Set up the Flask-Principal stuff for this user"""        
        if current_user.is_anonymous():                        
            return
        if current_user.event_creator:            
            identity.provides.add(needs.EventCreatorRoleNeed())
            for event in current_user.events_created:
                if event.event_creator_pss_user_id == current_user.pss_user_id:
                    identity.provides.add(needs.EventEditNeed(event.event_id))
        else:
            for event_role in current_user.event_roles:
                if event_role.event_role_name == roles_constants.TOURNAMENT_DIRECTOR:
                    identity.provides.add(needs.TournamentDirectorRoleNeed(event_role.event_id))
                if event_role.event_role_name == roles_constants.SCOREKEEPER:
                    identity.provides.add(needs.ScorekeeperRoleNeed(event_role.event_id))
                if event_role.event_role_name == roles_constants.DESKWORKER:
                    identity.provides.add(needs.DeskworkerRoleNeed(event_role.event_id))
                if event_role.event_role_name == roles_constants.PLAYER:
                    identity.provides.add(needs.PlayerRoleNeed(event_role.event_id))
                    
    return on_identity_loaded
