from werkzeug.exceptions import BadRequest, Unauthorized
from lib_v2 import blueprints
from flask import jsonify,current_app,request
from lib_v2 import permissions
from flask_login import current_user
from lib_v2.serializers import generic
from routes_v2.tournament import create_tournament_route
from routes_v2.tournament_machine import create_tournament_machine_route
import json
from shutil import copyfile

def handle_img_upload(input_data):
    print "in handle img upload..."    
    event_img_folders=current_app.config['IMG_HTTP_SRV_DIR']
    if input_data.get('img_file',None) and input_data.get('has_pic',None):
        print "in handle img upload...and processing"
        copyfile(current_app.config['UPLOAD_FOLDER']+"/"+input_data['img_file'],event_img_folders+"/"+input_data['img_file'])
        input_data['img_url']='/assets/imgs/%s'%(input_data['img_file'])

    
def pss_event_create_route(request,tables_proxy,user,commit=True):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Submitted information is missing required fields')    
    # don't allow duplicate names    
    if tables_proxy.get_event_by_eventname(input_data['name']) is not None:
        raise BadRequest('Event already exists')
    handle_img_upload(input_data)    
    new_event = tables_proxy.create_event(user,input_data,commit)
    #tables_proxy.create_event_tables(new_event.event_id)
    return new_event

def pss_event_edit_route(request,tables_proxy):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Submitted information is missing required fields')    
    # don't allow duplicate names
    event = tables_proxy.get_event_by_eventname(input_data['name'])
    if event and event.event_id != int(input_data['event_id']):
        if tables_proxy.get_event_by_eventname(input_data['name']) is not None:
            raise BadRequest('Event name already exists')
    handle_img_upload(input_data)
    return tables_proxy.edit_event(input_data,True)            

@blueprints.test_blueprint.route('/events',methods=['get'])
def get_all_events():
    events = current_app.table_proxy.Events.query.filter_by(active=True).all()    
    events_list = []
    for event in events:
        permission = permissions.EventEditPermission(event.event_id)
        if permission.can():
            events_list.append(generic.serialize_event_private(event))
        else:
            events_list.append(generic.serialize_event_public(event))
    return jsonify({'data':events_list})

@blueprints.test_blueprint.route('/event/<int:event_id>',methods=['get'])
def get_event(event_id):
    event = current_app.table_proxy.Events.query.filter_by(event_id=event_id).first()    
    event_dict = []
    permission = permissions.EventEditPermission(event.event_id)
    if permission.can():
        event_dict=generic.serialize_event_private(event)
    else:
        event_dict=generic.serialize_event_public(event)
    return jsonify({'data':event_dict})

@blueprints.test_blueprint.route('/events/tournaments',methods=['GET'])
def get_all_events_and_tournaments():    
    events = current_app.table_proxy.Events.query.filter_by(active=True).all()    
    events_list = []
    for event in events:
        permission = permissions.EventEditPermission(event.event_id)
        if permission.can():            
            event_dict=generic.serialize_event_private(event)
            event_dict['event_creator_pss_user_id']=event.event_creator_pss_user_id
        else:            
            event_dict=generic.serialize_event_public(event)
            event_dict['event_creator_pss_user_id']=None            
        event_dict['tournaments']=[]        
        tournaments = current_app.table_proxy.Tournaments.query.filter_by(event_id=event.event_id).all()
        for tournament in tournaments:
            if permission.can():
                tournament_dict=generic.serialize_tournament_private(tournament)            
            else:
                tournament_dict=generic.serialize_tournament_public(tournament)        
            event_dict['tournaments'].append(tournament_dict)
        events_list.append(event_dict)
    return jsonify({'data':events_list})

@blueprints.test_blueprint.route('/event',methods=['POST'])
def event_create():    
    permission = permissions.EventCreatorPermission()    
    if not permission.can():
        raise Unauthorized('You are not authorized to create an event')
    event = pss_event_create_route(request,current_app.table_proxy,current_user)
    return jsonify({'data':generic.serialize_event_public(event)})

#FIXME : MOVE TO SEPERATE WIZARD FILE
@blueprints.test_blueprint.route('/wizard/event/tournament/tournament_machines',methods=['POST'])
def wizard_event_create():        
    permission = permissions.EventCreatorPermission()    
    if not permission.can():
        raise Unauthorized('You are not authorized to create an event')
    orig_data = request.data
    event_data_string = json.dumps(json.loads(orig_data)['event'])
    request.data=event_data_string
    event = pss_event_create_route(request,current_app.table_proxy,current_user,False)
    tournament_data_string = json.dumps(json.loads(orig_data)['tournament'])
    request.data=tournament_data_string
    #FIXME : add check for multiple tournaments
    tournaments = create_tournament_route(request,current_app.table_proxy,commit=False)
    event.tournaments.append(tournaments[0])
    tournament_machines = json.loads(orig_data)['tournament_machines']
    tournament_machines_sqlalchemy_objects=[]
    for tournament_machine in tournament_machines:
        tournament_machine_string = json.dumps(tournament_machine)
        request.data=tournament_machine_string
        tournament_machines_sqlalchemy_objects.append(create_tournament_machine_route(request,current_app.table_proxy,None,tournaments[0]))
        
    current_app.table_proxy.commit_changes()    
    #FIXME : this should not be a two part commit
    for tournament_machine in tournament_machines_sqlalchemy_objects:
        current_app.table_proxy.create_queue_for_tournament_machine(tournament_machine,tournaments[0].queue_size,event.event_id)
    current_app.table_proxy.commit_changes()
        
    return jsonify({'data':generic.serialize_event_public(event)})


@blueprints.test_blueprint.route('/event',methods=['PUT'])
def event_edit():
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Submitted information is missing required fields')
    permission = permissions.EventEditPermission(input_data['event_id'])
    if not permission.can():
        raise Unauthorized('You are not authorized to edit this event')        
    event = pss_event_edit_route(request,current_app.table_proxy)        
    return jsonify({'data':generic.serialize_event_public(event)})
    

