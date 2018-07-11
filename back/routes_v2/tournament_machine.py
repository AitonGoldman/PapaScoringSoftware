from werkzeug.exceptions import BadRequest, Unauthorized
from lib_v2 import blueprints,permissions
from flask import jsonify,current_app,request
from flask_login import current_user
from lib_v2.serializers import generic
from flask_restless.helpers import to_dict
import json
from shutil import copyfile
from routes_v2.player import get_event_player_route

def handle_img_upload(input_data):
    print "in handle img upload..."    
    event_img_folders=current_app.config['IMG_HTTP_SRV_DIR']

    if input_data.get('img_file',None) and input_data.get('has_pic',None):
        print "in handle img upload...and processing"
        copyfile(current_app.config['UPLOAD_FOLDER']+"/"+input_data['img_file'],event_img_folders+"/"+input_data['img_file'])
        input_data['img_url']='/assets/imgs/%s'%(input_data['img_file'])


def create_tournament_machine_route(request,tables_proxy,event_id,tournament=None):
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
        if tournament is None:
            raise BadRequest('No tournament id specified')
            
    tournament_machine = tables_proxy.create_tournament_machine(machine,tournament)
    if(event_id):
        tables_proxy.create_queue_for_tournament_machine(tournament_machine,tournament.queue_size,event_id)
    return tournament_machine

def edit_tournament_machine_route(request,app,event_id):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Submitted information is missing required fields')
    #put tournament edit logic here
    handle_img_upload(input_data)
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
    new_tournament_machine = create_tournament_machine_route(request,current_app.table_proxy,event_id)
    current_app.table_proxy.commit_changes()
    return jsonify({'data':generic.serialize_tournament_machine_public(new_tournament_machine)})

@blueprints.test_blueprint.route('/<int:event_id>/tournament_machine',methods=['PUT'])
def edit_tournament_machine(event_id):            
    #FIXME : need to muck with queues if queue length is changed, or queuing is turned off
    permission = permissions.CreateTournamentPermission(event_id)    
    if not permission.can():
        raise Unauthorized('You are not authorized to edit tournaments for this event')        
    edited_tournament_machine = edit_tournament_machine_route(request,current_app,event_id)
    tournament_machine_dict=generic.serialize_tournament_machine_public(edited_tournament_machine)
    current_app.table_proxy.commit_changes()
    return jsonify({'data':tournament_machine_dict})

@blueprints.test_blueprint.route('/<int:event_id>/<int:tournament_id>/tournament_machines/machines',methods=['GET'])
def get_tournament_machines_and_machines(event_id,tournament_id):                
    machines_list=[]
    tournament_machines_list=[]
    machines = current_app.table_proxy.get_all_machines()
    tournament_machines = current_app.table_proxy.get_tournament_machines(tournament_id)
    for machine in machines:        
        machines_list.append(to_dict(machine))
    for tournament_machine in tournament_machines:        
        tournament_machines_list.append(to_dict(tournament_machine))        
        
    return jsonify({'data':{'machines_list':machines_list,'tournament_machines_list':tournament_machines_list}})


@blueprints.test_blueprint.route('/<int:event_id>/<int:tournament_id>/tournament_machine/<int:tournament_machine_id>',methods=['GET'])
def get_tournament_machine(event_id,tournament_id,tournament_machine_id):
    queues = current_app.table_proxy.get_all_queues(event_id)    
    tournament_machine = current_app.table_proxy.get_tournament_machine_by_id(tournament_machine_id)
    tournament_machine_dict = generic.serialize_tournament_machine_public(tournament_machine,generic.TOURNAMENT_MACHINE_AND_QUEUES_AND_PLAYER)    
    if tournament_machine_dict.get('player_id',None):
        player = current_app.table_proxy.get_player(event_id,player_id=tournament_machine_dict['player_id'])
        player_id_for_event = [event_player for event_player in player.event_info if event_player.event_id == event_id][0].player_id_for_event
        event_player_info = get_event_player_route(current_app,event_id,player_id_for_event)
        tournament_machine_dict['tournament_counts']=event_player_info['tournament_counts']        
    return jsonify({'data':tournament_machine_dict})
    
    
@blueprints.test_blueprint.route('/<int:event_id>/<int:tournament_id>/tournament_machines',methods=['GET'])
def get_tournament_machines(event_id,tournament_id):                    
    tournament_machines_list=[]    
    tournament = current_app.table_proxy.get_tournament_by_tournament_id(tournament_id)
    if tournament:
        tournament_name=tournament.tournament_name
    else:
        tournament_name=None
    tournament_machines = current_app.table_proxy.get_tournament_machines(tournament_id)
    for tournament_machine in tournament_machines:        
        tournament_machines_list.append(to_dict(tournament_machine))        
    event_players_list = [generic.serialize_player_public(event_player) for event_player in current_app.table_proxy.get_all_event_players(event_id) if event_player.has_pic is True]
        
    return jsonify({'data':tournament_machines_list,'event_players':event_players_list,'tournament_name':tournament_name})

