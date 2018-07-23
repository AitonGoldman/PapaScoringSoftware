from collections import namedtuple
from functools import partial

from flask.ext.login import current_user
from flask.ext.principal import identity_loaded, Permission, RoleNeed, UserNeed
from lib import roles_constants

PssRouteNeed = namedtuple('pss_route_need', ['method', 'value'])
AdminNeed = partial(PssRouteNeed, roles_constants.PSS_ADMIN)
UserNeed = partial(PssRouteNeed, roles_constants.PSS_ADMIN)

class EventCreatorPermission(Permission):
    def __init__(self, event_id):
        need = EventEditorNeed(event_id)
        super(EventCreatorPermission, self).__init__(need)

def generate_pss_user_identity_loaded(app):                                
    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        #print "####################"
        #print "IN IDENTITY LOADED"
        # Set the identity user object
        #identity.user = current_user
        if current_user.is_anonymous():                        
            return
    
        #identity.provides.add(UserNeed(current_user.pss_user_id))        
        #user = app.tables.PssUsers.query.filter_by(pss_user_id=current_user.pss_user_id).first()        
        #events = [event for event in app.tables.Events.query.filter(app.tables.Events.event_id.in_(user.events))]
        #events = [event for event in user.events]
        #for event in events:
        for event in current_user.events:                    
            identity.provides.add(EventEditorNeed(event.event_id))
        app.tables.db_handle.session.close_all()
