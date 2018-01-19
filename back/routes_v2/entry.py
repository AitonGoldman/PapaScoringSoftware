from flask_restless.helpers import to_dict
from werkzeug.exceptions import BadRequest, Unauthorized
from lib_v2 import blueprints,permissions
from flask import jsonify,current_app,request
from flask_login import current_user
from lib_v2.serializers import generic
from lib_v2.queue_helpers import remove_player_with_notification
import json
from lib_v2.serializers import generic

def void_ticket_route(input_data,event_id,app,current_user):
    player = app.table_proxy.get_player(event_id,player_id=input_data['player_id'])
    tournament_machine = app.table_proxy.get_tournament_machine_by_id(input_data['tournament_machine_id'])    
    if app.table_proxy.void_ticket(event_id,player,tournament_machine) is False:
        raise BadRequest('Failed to void ticket')
    app.table_proxy.remove_player_from_machine(tournament_machine)
    

def record_score_route(input_data,event_id,app,current_user):
    score=int(input_data['score'])
    player = app.table_proxy.get_player(event_id,player_id=input_data['player_id'])
    tournament_machine = app.table_proxy.get_tournament_machine_by_id(input_data['tournament_machine_id'])
    tournament = app.table_proxy.get_tournament_by_tournament_id(tournament_machine.tournament_id)            
    token_count = app.table_proxy.get_available_token_count_for_tournament(event_id,player,tournament)
    if token_count < 1:
        raise BadRequest('Tried to record a score without any tokens available')
    app.table_proxy.mark_token_as_used(event_id,player,tournament)
    app.table_proxy.remove_player_from_machine(tournament_machine)
    app.table_proxy.record_score(event_id,player,tournament_machine,score)
    
def start_player_on_machine_route(input_data,event_id, app, current_user):
    player = app.table_proxy.get_player(event_id,player_id=input_data['player_id'])
    tournament_machine = app.table_proxy.get_tournament_machine_by_id(input_data['tournament_machine_id'])
    if tournament_machine.player_id:
        raise BadRequest('Tried to start game when someone is already playing!')
    if app.table_proxy.start_player_on_machine(event_id,tournament_machine,player) is False:
        raise BadRequest('Tried to start game without tokens')
    
    audit_log_params={
        'action':'Player started on machine',
        'player_id':player.player_id,        
        'player_initiated':False,        
        'description':'Player %s started on machine %s by %s' % (player,tournament_machine.tournament_machine_name,current_user),
        'tournament_machine_id':tournament_machine.tournament_machine_id,
        'event_id':event_id
    }
    app.table_proxy.create_audit_log(audit_log_params,event_id)    

def start_player_on_machine_from_queue_route(input_data,event_id, app, current_user):
    player = app.table_proxy.get_player(event_id,player_id=input_data['player_id'])
    tournament_machine = app.table_proxy.get_tournament_machine_by_id(input_data['tournament_machine_id'])
    if tournament_machine.player_id:
        raise BadRequest('Tried to start game when someone is already playing!')
    head_of_queue = app.table_proxy.get_sorted_queue_for_tournament_machine(tournament_machine)[0]
    if head_of_queue.player_id != player.player_id:
        raise BadRequest('The player is not at the head of the queue.  Please try again')
    # check that player is at top of queue
    remove_player_with_notification(player,app,tournament_machine, event_id)
    # remove player from queue

    # add player to machine
    if app.table_proxy.start_player_on_machine(event_id,tournament_machine,player) is False:
        raise BadRequest('Tried to start game without tokens')
    
    audit_log_params={
        'action':'Player started on machine from queue',
        'player_id':player.player_id,        
        'player_initiated':False,        
        'description':'Player %s started on machine %s by %s from queue' % (player,tournament_machine.tournament_machine_name,current_user),
        'tournament_machine_id':tournament_machine.tournament_machine_id,
        'event_id':event_id
    }
    app.table_proxy.create_audit_log(audit_log_params,event_id)    
    
@blueprints.test_blueprint.route('/<int:event_id>/entry',methods=['POST'])
def start_player_on_machine(event_id):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('No info in request')        
    scorekeeper_permission = permissions.ScorekeeperPermission(event_id)
    if scorekeeper_permission.can():
        if input_data['action'] == 'start':
            start_player_on_machine_route(input_data,event_id,current_app,current_user)
        if input_data['action'] == 'start_from_queue':            
            start_player_on_machine_from_queue_route(input_data,event_id,current_app,current_user)
            pass
    else:
        raise Unauthorized('You are not authorized to start a player on a machine')
    #total_cost = sum(int(summary[2]['price']) for summary in purchase_summary)
    #generic_serializer = generate_generic_serializer(serializer.generic.ALL)
    #return jsonify({'new_token_purchase':generic_serializer(new_token_purchase),
    #                'purchase_summary':purchase_summary,
    #                'total_cost':new_token_purchase.total_cost})
    current_app.table_proxy.commit_changes()
    return jsonify({})

@blueprints.test_blueprint.route('/<int:event_id>/entry',methods=['PUT'])
def change_entry(event_id):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('No info in request')        
    scorekeeper_permission = permissions.ScorekeeperPermission(event_id)
    if scorekeeper_permission.can():
        if input_data['action'] == 'record_score':
            print "recording score..."
            record_score_route(input_data,event_id,current_app,current_user)
    else:
        raise Unauthorized('You are not authorized to do this')
    #total_cost = sum(int(summary[2]['price']) for summary in purchase_summary)
    #generic_serializer = generate_generic_serializer(serializer.generic.ALL)
    #return jsonify({'new_token_purchase':generic_serializer(new_token_purchase),
    #                'purchase_summary':purchase_summary,
    #                'total_cost':new_token_purchase.total_cost})
    current_app.table_proxy.commit_changes()
    tournament = current_app.table_proxy.get_tournament_by_tournament_id(input_data['tournament_id'])
    player= current_app.table_proxy.get_player(event_id, player_id=input_data['player_id'])    
    tournament_counts = current_app.table_proxy.get_available_token_count_for_tournament(event_id,player,tournament)
    tournament_machine = current_app.table_proxy.get_tournament_machine_by_id(input_data['tournament_machine_id'])
    tournament_machine_dict=generic.serialize_tournament_machine_public(tournament_machine,generic.TOURNAMENT_MACHINE_AND_QUEUES)                
    return jsonify({'data':tournament_machine_dict,
                    'tournament_counts':tournament_counts})


@blueprints.test_blueprint.route('/<int:event_id>/entry',methods=['DELETE'])
def void_ticket(event_id):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('No info in request')        
    scorekeeper_permission = permissions.ScorekeeperPermission(event_id)
    if scorekeeper_permission.can():
        void_ticket_route(input_data,event_id,current_app,current_user)
    else:
        raise Unauthorized('You are not authorized to void a ticket')
    #total_cost = sum(int(summary[2]['price']) for summary in purchase_summary)
    #generic_serializer = generate_generic_serializer(serializer.generic.ALL)
    #return jsonify({'new_token_purchase':generic_serializer(new_token_purchase),
    #                'purchase_summary':purchase_summary,
    #                'total_cost':new_token_purchase.total_cost})
    current_app.table_proxy.commit_changes()
    tournament = current_app.table_proxy.get_tournament_by_tournament_id(input_data['tournament_id'])
    player= current_app.table_proxy.get_player(event_id, player_id=input_data['player_id'])    
    tournament_counts = current_app.table_proxy.get_available_token_count_for_tournament(event_id,player,tournament)
    tournament_machine = current_app.table_proxy.get_tournament_machine_by_id(input_data['tournament_machine_id'])
    tournament_machine_dict=generic.serialize_tournament_machine_public(tournament_machine,generic.TOURNAMENT_MACHINE_AND_QUEUES)                
    return jsonify({'data':tournament_machine_dict,
                    'tournament_counts':tournament_counts})

    return jsonify({})

