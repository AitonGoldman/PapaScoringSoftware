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

def admin_void_ticket_route(event_id,app,current_user,player_id,tournament_id, number_tokens_to_void):
    player = app.table_proxy.get_player(event_id,player_id=player_id)    
    tournament = app.table_proxy.get_tournament_by_tournament_id(tournament_id)
    tokens = app.table_proxy.get_tokens_by_tournament(event_id,player,tournament)
    if len(tokens)< number_tokens_to_void:
        raise BadRequest('Not enough tickets to void')
    current_app.table_proxy.void_tickets_without_checking(tokens[0:number_tokens_to_void])
    

@blueprints.test_blueprint.route('/<int:event_id>/admin/token/<int:player_id>/<int:tournament_id>/<int:number_tokens_to_void>',methods=['DELETE'])
def admin_void_ticket(event_id,player_id,tournament_id,number_tokens_to_void):
    admin_void_ticket_route(event_id,current_app,current_user,player_id,tournament_id,number_tokens_to_void)
    current_app.table_proxy.commit_changes()
    return jsonify({})
