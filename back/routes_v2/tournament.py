from werkzeug.exceptions import BadRequest, Unauthorized
from lib_v2 import blueprints,permissions
from flask import jsonify,current_app,request
from flask_login import current_user
from lib_v2.serializers import generic
from routes_v2.tournament_machine import create_tournament_machine_route
#from routes_v2.event import handle_img_upload
from shutil import copyfile

import json

def handle_img_upload(input_data):
    event_img_folders='/Users/agoldma/git/github/TD/front_v2/www/assets/imgs/'
    if 'img_file' in input_data and input_data['img_file'] and input_data['has_pic']:
        copyfile(current_app.config['UPLOAD_FOLDER']+"/"+input_data['img_file'],event_img_folders+"/"+input_data['img_file'])
        input_data['img_url']='/assets/imgs/%s'%(input_data['img_file'])



def create_tournament_route(request,tables_proxy,event_id=None,commit=True):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Submitted information is missing required fields')    
    #put tournament create logic here
    if input_data.get('multi_division_tournament',None) is True:
        return tables_proxy.create_multi_division_tournament(input_data['tournament']['tournament_name'],
                                                             int(input_data['division_count']),        
                                                             input_data['tournament'],event_id,commit=commit)
    else:        
        handle_img_upload(input_data['tournament'])
        return [tables_proxy.create_tournament(input_data['tournament'],event_id,commit=commit)]
    

def edit_tournament_route(request,app,event_id):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Submitted information is missing required fields')
    #put tournament edit logic here
    tournament = app.table_proxy.edit_tournament(input_data,False)
    handle_img_upload(input_data)
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
    new_tournaments = create_tournament_route(request,current_app.table_proxy,event_id=event_id)
    current_app.table_proxy.commit_changes()
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
    current_app.table_proxy.commit_changes()
    tournament_dict=generic.serialize_tournament_public(tournament)
    return jsonify({'data':tournament_dict})

#FIXME : MOVE TO SEPERATE WIZARD FILE
@blueprints.test_blueprint.route('/wizard/tournament/tournament_machines',methods=['POST'])
def wizard_tournament_create():        
    orig_data = request.data
    tournament = json.loads(orig_data)['tournament']
    print tournament['tournament']
    permission = permissions.CreateTournamentPermission(tournament['tournament']['event_id'])    
    if not permission.can():
        raise Unauthorized('You are not authorized to create an event')
    
    event = current_app.table_proxy.get_event_by_event_id(tournament['tournament']['event_id'])
    tournament_data_string = json.dumps(json.loads(orig_data)['tournament'])
    request.data=tournament_data_string
    #FIXME : add check for multiple tournaments
    tournaments = create_tournament_route(request,current_app.table_proxy,commit=False)
    event.tournaments.append(tournaments[0])
    tournament_machines = json.loads(orig_data)['tournament_machines']
    for tournament_machine in tournament_machines:
        tournament_machine_string = json.dumps(tournament_machine)
        request.data=tournament_machine_string
        create_tournament_machine_route(request,current_app.table_proxy,None,tournaments[0])
    current_app.table_proxy.db_handle.session.commit()
    return jsonify({'data':generic.serialize_event_public(event)})


@blueprints.test_blueprint.route('/<int:event_id>/tournaments',methods=['GET'])
def get_all_tournaments(event_id):            
    tournaments_list=[]
    permission = permissions.CreateTournamentPermission(event_id)    
    tournaments = current_app.table_proxy.get_tournaments(event_id)
    for tournament in tournaments:
        if permission.can():
            tournament_dict=generic.serialize_tournament_private(tournament)            
        else:
            tournament_dict=generic.serialize_tournament_public(tournament)        
        tournaments_list.append(tournament_dict)
    return jsonify({'data':tournaments_list})


@blueprints.test_blueprint.route('/<int:event_id>/tournament/<int:tournament_id>',methods=['GET'])
def get_tournament(event_id,tournament_id):
    tournament = current_app.table_proxy.get_tournament_by_tournament_id(tournament_id)
    if tournament is None:
        raise BadRequest('Tournament does not exist')
    permission = permissions.CreateTournamentPermission(event_id)    
    tournament_dict=None
    if permission.can():
        tournament_dict=generic.serialize_tournament_private(tournament)            
    else:
        tournament_dict=generic.serialize_tournament_public(tournament)            
    return jsonify({'data':tournament_dict})
