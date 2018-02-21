from werkzeug.exceptions import BadRequest, Unauthorized
from lib_v2 import blueprints,permissions
from flask import jsonify,current_app,request
from flask_login import current_user
from lib_v2.serializers import generic
from routes_v2.tournament_machine import create_tournament_machine_route
from routes_v2.player import get_event_player_route
#from routes_v2.event import handle_img_upload
from shutil import copyfile

import json

def handle_img_upload(input_data):
    print "in handle img for tourneys..."
    event_img_folders=current_app.config['IMG_HTTP_SRV_DIR']
    
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
    handle_img_upload(input_data)    

    tournament = app.table_proxy.get_tournament_by_tournament_id(input_data['tournament_id'])
    original_stripe_sku = tournament.stripe_sku
    original_discount_stripe_sku = tournament.discount_stripe_sku
    
    tournament = app.table_proxy.edit_tournament(input_data,False)
    
    if input_data.get('use_stripe',None):        
        stripe_sku = input_data.get('stripe_sku',None)
        discount_stripe_sku = input_data.get('discount_stripe_sku',None)                
        if (stripe_sku and original_stripe_sku!=stripe_sku) or (discount_stripe_sku and original_discount_stripe_sku!=discount_stripe_sku):            
            api_key = app.event_settings[event_id].stripe_api_key
            app.stripe_proxy.set_tournament_stripe_prices(tournament,api_key,
                                                          stripe_sku, discount_stripe_sku)            
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
    tournament_machines = json.loads(orig_data)['tournament_machines']
    tournament_machines_sqlalchemy_objects=[]
    for tournament_machine in tournament_machines:
        tournament_machine_string = json.dumps(tournament_machine)
        request.data=tournament_machine_string
        tournament_machines_sqlalchemy_objects.append(create_tournament_machine_route(request,current_app.table_proxy,None,tournaments[0]))
    for tournament_machine in tournament_machines_sqlalchemy_objects:
        current_app.table_proxy.create_queue_for_tournament_machine(tournament_machine,tournaments[0].queue_size,event.event_id)
    current_app.table_proxy.commit_changes()

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
        finals = current_app.table_proxy.get_finals_by_tournament_id(tournament.tournament_id)
        # if finals:
        #     tournament_dict['finals_ids']=[]
        #     for final in finals:
        #         tournament_dict['finals_ids'].append({'final_id':final.final_id,'final_name':final.name})
        add_finals_to_tournament_dict(tournament_dict,tournament,current_app)
        tournaments_list.append(tournament_dict)
    return jsonify({'data':tournaments_list})

def add_finals_to_tournament_dict(tournament_dict,tournament, app):
    finals = app.table_proxy.get_finals_by_tournament_id(tournament.tournament_id)
    if finals:
        tournament_dict['finals_ids']=[]
        for final in finals:
            tournament_dict['finals_ids'].append({'final_id':final.final_id,'final_name':final.name,'number_of_rounds':final.number_of_rounds})
    
def get_all_tournaments_and_tournament_machines_route(event_id,app):
    tournaments_list=[]    
    tournaments = app.table_proxy.get_tournaments(event_id)

    queues = app.table_proxy.get_all_queues(event_id)
    for tournament in tournaments:        
        tournament_dict=generic.serialize_tournament_public(tournament,generic.TOURNAMENT_AND_TOURNAMENT_MACHINES)            
        for tournament_machine in tournament_dict['tournament_machines']:                        
            tournament_machine['queues']=[generic.serialize_queue(queue,generic.QUEUE_AND_PLAYER) for queue in queues[tournament_machine['tournament_machine_id']]]
            tournament_machine['queues'].sort(key=lambda x: x['position'])
            
            tournament_machine['queue_length']=len([queue for queue in tournament_machine['queues'] if queue.get('player',None)])
            if tournament_machine.get('player_id',None):
                tournament_machine['queue_length']= tournament_machine['queue_length'] + 1           
        add_finals_to_tournament_dict(tournament_dict,tournament,app)           
        tournaments_list.append(tournament_dict)
    return tournaments_list

@blueprints.test_blueprint.route('/<int:event_id>/tournaments/tournament_machines',methods=['GET'])
def get_all_tournaments_and_tournament_machines(event_id):                
    tournaments_list=get_all_tournaments_and_tournament_machines_route(event_id,current_app)
    return jsonify({'data':tournaments_list})

@blueprints.test_blueprint.route('/<int:event_id>/tournaments/tournament_machines/event_player/<int:event_player_id>',methods=['GET'])
def get_all_tournaments_and_tournament_machines_and_event_player(event_id,event_player_id):                
    tournaments_list=get_all_tournaments_and_tournament_machines_route(event_id,current_app)
    event_player_info = get_event_player_route(current_app,event_id,event_player_id)    
    return jsonify({'data':tournaments_list,
                    'player':event_player_info['data'],
                    'tournament_calculated_price_lists_for_player':event_player_info['tournament_calculated_lists'],
                    'player_ticket_counts':event_player_info['tournament_counts']})

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
