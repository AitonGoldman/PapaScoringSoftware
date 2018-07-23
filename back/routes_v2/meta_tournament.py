from werkzeug.exceptions import BadRequest, Unauthorized
from lib_v2 import blueprints,permissions
from flask import jsonify,current_app,request
from flask_login import current_user
from lib_v2.serializers import generic
import json

def create_meta_tournament_route(request,tables_proxy,event_id):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Submitted information is missing required fields')    
    #put tournament create logic here
    tournaments=[]
    for tournament_id in input_data['tournament_ids']:
        tournament = tables_proxy.get_tournament_by_tournament_id(tournament_id)
        if tournament is None:
            raise BadRequest('Bad tournament id specified')
        tournaments.append(tournament)
    return tables_proxy.create_meta_tournament(tournaments,input_data,event_id)
    

def edit_meta_tournament_route(request,app,event_id):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Submitted information is missing required fields')
    #put tournament edit logic here
    meta_tournament = app.table_proxy.get_meta_tournament_by_id(input_data['meta_tournament_id'])
    if meta_tournament is None:
        raise BadRequest('Bad metatournament id submitted')
    edited_meta_tournament = app.table_proxy.edit_meta_tournament(meta_tournament,input_data,False)
    if input_data.get('use_stripe',None):        
        api_key = app.event_settings[event_id].stripe_api_key
        app.stripe_proxy.set_tournament_stripe_prices(meta_tournament,api_key,input_data.get('stripe_sku',None),
                                                      input_data.get('discount_stripe_sku',None))
    else:    
        app.table_proxy.clear_stripe_prices_from_tournament(meta_tournament)
    return meta_tournament

@blueprints.test_blueprint.route('/<int:event_id>/meta_tournament',methods=['POST'])
def create_meta_tournament(event_id):            
    permission = permissions.CreateTournamentPermission(event_id)    
    if not permission.can():
        raise Unauthorized('You are not authorized to create meta tournaments for this event')        
    new_meta_tournament = create_meta_tournament_route(request,current_app.table_proxy,event_id)    
    current_app.table_proxy.commit_changes()
    return jsonify({'data':generic.serialize_meta_tournament_public(new_meta_tournament)})

@blueprints.test_blueprint.route('/<int:event_id>/meta_tournament',methods=['PUT'])
def edit_meta_tournament(event_id):            
    permission = permissions.CreateTournamentPermission(event_id)    
    if not permission.can():
        raise Unauthorized('You are not authorized to edit meta tournaments for this event')        
    meta_tournament = edit_meta_tournament_route(request,current_app,event_id)
    current_app.table_proxy.commit_changes()
    meta_tournament_dict=generic.serialize_meta_tournament_public(meta_tournament)
    return jsonify({'data':meta_tournament_dict})
