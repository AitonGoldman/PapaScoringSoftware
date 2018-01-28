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

def admin_edit_ticket_route(event_id,app,current_user,player_id,score_id):
    score = app.table_proxy.get_score(event_id,player_id,score_id)
    score.voided=score.voided==False
    
    

@blueprints.test_blueprint.route('/<int:event_id>/admin/token/<int:player_id>/<int:tournament_id>/<int:number_tokens_to_void>',methods=['DELETE'])
def admin_void_ticket(event_id,player_id,tournament_id,number_tokens_to_void):
    permission = permissions.CreateTournamentPermission(event_id)    
    if not permission.can():            
        raise Unauthorized('You are not authorized to void unused tokens')            
            
    admin_void_ticket_route(event_id,current_app,current_user,player_id,tournament_id,number_tokens_to_void)
    current_app.table_proxy.commit_changes()
    return jsonify({})

@blueprints.test_blueprint.route('/<int:event_id>/admin/entry/<int:player_id>/<int:score_id>',methods=['PUT'])
def admin_edit_ticket(event_id,player_id,score_id):
    permission = permissions.CreateTournamentPermission(event_id)    
    if not permission.can():            
        raise Unauthorized('You are not authorized to edit scores')                         

    admin_edit_ticket_route(event_id,current_app,current_user,player_id,score_id)
    current_app.table_proxy.commit_changes()
    return jsonify({})

@blueprints.test_blueprint.route('/<int:event_id>/admin/entry/<int:player_id>/<int:tournament_machine_id>/<int:score>',methods=['PUT'])
def admin_add_score(event_id,player_id,tournament_machine_id,score):
    permission = permissions.CreateTournamentPermission(event_id)    
    if not permission.can():            
        raise Unauthorized('You are not authorized to add new scores')                         
    player = current_app.table_proxy.get_player(event_id,player_id=player_id)
    tournament_machine = current_app.table_proxy.get_tournament_machine_by_id(tournament_machine_id)
    new_score = current_app.table_proxy.record_score(event_id,player,tournament_machine,score)    
    current_app.table_proxy.commit_changes()
    return jsonify({'data':generic.serialize_score(new_score)})
