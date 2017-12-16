from werkzeug.exceptions import BadRequest, Unauthorized
from lib_v2 import blueprints,permissions
from flask import jsonify,current_app,request
from flask_login import current_user
from lib_v2.serializers import generic
import json

def create_tournament_route(request,tables_proxy,event_id):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Submitted information is missing required fields')    
    #put tournament create logic here
    if input_data.get('multi_division_tournament',None) is True:
        return tables_proxy.create_multi_division_tournament(input_data['multi_division_tournament_name'],input_data['division_count'],
                                                             input_data['tournament'],event_id)
    else:        
        return [tables_proxy.create_tournament(input_data['tournament'],event_id,True)]
    

def edit_tournament_route(request,app,event_id):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Submitted information is missing required fields')
    #put tournament edit logic here
    tournament = app.table_proxy.edit_tournament(input_data,False)
    if input_data.get('use_stripe',None):
        api_key = app.event_settings[event_id].stripe_api_key
        app.stripe_proxy.set_tournament_stripe_prices(tournament,api_key,input_data.get('stripe_sku',None),
                                                      input_data.get('discount_stripe_sku',None))
    else:    
        app.table_proxy.clear_stripe_prices_from_tournament(tournament)
    return tournament

@blueprints.test_blueprint.route('/<int:event_id>/tournament',methods=['POST'])
def create_tournament(event_id):            
    permission = permissions.CreateTournamentPermission(event_id)    
    if not permission.can():
        raise Unauthorized('You are not authorized to create tournaments for this event')        
    new_tournaments = create_tournament_route(request,current_app.table_proxy,event_id)
    tournament_dicts = []
    for new_tournament in new_tournaments:
        tournament_dicts.append(generic.serialize_tournament_public(new_tournament))
    return jsonify({'data':tournament_dicts})

@blueprints.test_blueprint.route('/<int:event_id>/tournament',methods=['PUT'])
def edit_tournament(event_id):            
    permission = permissions.CreateTournamentPermission(event_id)    
    if not permission.can():
        raise Unauthorized('You are not authorized to edit tournaments for this event')        
    tournament = edit_tournament_route(request,current_app,event_id)
    tournament_dict=generic.serialize_tournament_public(tournament)
    return jsonify({'data':tournament_dict})
