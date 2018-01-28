from flask_restless.helpers import to_dict
from werkzeug.exceptions import BadRequest, Unauthorized
from lib_v2 import blueprints,permissions
from flask import jsonify,current_app,request
from flask_login import current_user
from lib_v2.serializers import generic
from lib_v2.queue_helpers import remove_player_with_notification
import json
from lib_v2.serializers import generic
from routes_v2.queue import add_player_to_tournament_machine_queue_route


@blueprints.test_blueprint.route('/<int:event_id>/admin/scores/<int:player_id>',methods=['GET'])
def admin_get_scores(event_id,player_id):    
    return jsonify({'data':[generic.serialize_score(score) for score in current_app.table_proxy.get_scores(event_id,player_id)]})
