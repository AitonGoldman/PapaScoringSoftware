from werkzeug.exceptions import BadRequest, Unauthorized
from lib_v2 import blueprints,permissions
from flask import jsonify,current_app,request
from flask_login import current_user
from lib_v2.serializers import generic
import json

def create_tournament_machine_route(request,tables_proxy):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Submitted information is missing required fields')    
    #put tournament create logic here
    if input_data.get('machine_id',None):
        machine = tables_proxy.get_machine_by_id(input_data.get('machine_id'))
    else:
        raise BadRequest('No machine id specified')
    if input_data.get('tournament_id',None):
        tournament = tables_proxy.get_tournament_by_tournament_id(input_data.get('tournament_id'))
    else:
        raise BadRequest('No tournament id specified')    
    return tables_proxy.create_tournament_machine(machine,tournament)

def edit_tournament_machine_route(request,app,event_id):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Submitted information is missing required fields')
    #put tournament edit logic here
    tournament = app.table_proxy.edit_tournament_machine(input_data,False)
    if input_data.get('use_stripe',None):
        api_key = app.event_settings[event_id].stripe_api_key
        app.stripe_proxy.set_tournament_stripe_prices(tournament,api_key,input_data.get('stripe_sku',None),
                                                      input_data.get('discount_stripe_sku',None))
    else:    
        app.table_proxy.clear_stripe_prices_from_tournament(tournament)
    return tournament

@blueprints.test_blueprint.route('/<int:event_id>/tournament_machine',methods=['POST'])
def create_tournament_machine(event_id):            
    permission = permissions.CreateTournamentMachinePermission(event_id)    
    if not permission.can():
        raise Unauthorized('You are not authorized to manage tournament machines for this event')        
    new_tournament_machine = create_tournament_machine_route(request,current_app.table_proxy)
    current_app.table_proxy.commit_changes()
    return jsonify({'data':generic.serialize_tournament_machine_public(new_tournament_machine)})

@blueprints.test_blueprint.route('/<int:event_id>/tournament_machine',methods=['PUT'])
def edit_tournament_machine(event_id):            
    permission = permissions.CreateTournamentPermission(event_id)    
    if not permission.can():
        raise Unauthorized('You are not authorized to edit tournaments for this event')        
    edited_tournament_machine = edit_tournament_machine_route(request,current_app,event_id)
    tournament_machine_dict=generic.serialize_tournament_machine_public(edited_tournament_machine)
    current_app.table_proxy.commit_changes()
    return jsonify({'data':tournament_machine_dict})
