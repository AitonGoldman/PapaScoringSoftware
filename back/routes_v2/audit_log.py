from flask_restless.helpers import to_dict
from werkzeug.exceptions import BadRequest, Unauthorized
from lib_v2 import blueprints,permissions
from flask import jsonify,current_app,request
from flask_login import current_user
from lib_v2.serializers import generic
import json
from lib_v2.serializers import generic

@blueprints.test_blueprint.route('/<int:event_id>/audit_log/<int:player_id>',methods=['GET'])
def get_audit_logs(event_id,player_id):
    permission = permissions.CreateTournamentPermission(event_id)    
    if not permission.can():            
        raise Unauthorized('You are not authorized to get audit logs')            
    player = current_app.table_proxy.get_player(event_id,player_id=player_id)        
    audit_logs = [to_dict(audit_log) for audit_log in current_app.table_proxy.get_audit_logs(event_id,player_id)]
    return jsonify({'data':audit_logs})
