from flask_restless.helpers import to_dict
from lib.flask_lib import blueprints
from lib.flask_lib.permissions import create_player_permissions
from flask import jsonify,current_app,request
from werkzeug.exceptions import BadRequest,Unauthorized,Conflict
from flask_login import login_user, logout_user, current_user
import json
from lib import orm_factories
#from lib.serializer.pss_user import generate_pss_user_to_dict_serializer
from lib.serializer.player import generate_player_to_dict_serializer
from lib import serializer
from lib.route_decorators.db_decorators import load_tables
from sqlalchemy.orm import joinedload



def create_player_route(request, app):            
    tables = app.tables
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('No info in request')        
    if 'first_name' not in input_data or 'last_name' not in input_data or 'ifpa_ranking' not in input_data:        
        raise BadRequest('Information missing')
    
    existing_player=tables.Players.query.filter_by(first_name=input_data['first_name'],last_name=input_data['last_name']).first()
    #FIXME : needs to be more extensive of a check (i.e. check actual name, etc)
    if existing_player is not None:
        raise Conflict('Player already exists.')
    new_player = orm_factories.create_player(app,
                                             input_data['first_name'],
                                             input_data['last_name'],
                                             input_data['ifpa_ranking'])
    
    
    tables.db_handle.session.add(new_player)
    tables.db_handle.session.commit()
    return new_player

def add_existing_player_to_event_route(input_data,player,app):
    tables = app.tables
    if 'ifpa_ranking' not in input_data:
        raise BadRequest('missing ifpa ranking')    
    #FIXME : should do better player checking (i.e. force submission of first_name/lastname and check that against existing user?)
    orm_factories.populate_player(app,
                                  player,
                                  input_data['ifpa_ranking'])
    tables.db_handle.session.commit()
    return player

def change_existing_player_in_event_route(player, app, input_data):
    tables = app.tables    
    # FIXME : need ability to use email confirmation for edit player (see http://pythonhosted.org/itsdangerous/ for details on generating token)
    tables.db_handle.session.commit()
    return player

@blueprints.event_blueprint.route('/player',methods=['POST'])
@load_tables
@create_player_permissions.require(403)
def create_player(tables):                
    new_player = create_player_route(request,current_app)
    player_serializer = generate_player_to_dict_serializer(serializer.player.ALL)
    player_dict=player_serializer(new_player)
    return jsonify({'new_player':player_dict})
    

@blueprints.event_blueprint.route('/player',methods=['PUT'])
@load_tables
@create_player_permissions.require(403)
def add_existing_player_to_event(tables):                    
    input_data = json.loads(request.data)
    player = tables.Players.query.filter_by(player_id=input_data['player_id']).first()
    if player is None:
        raise BadRequest('No such player')
    event = tables.Events.query.filter_by(name=current_app.name).first()    
    if event not in player.events:
        modified_player = add_existing_player_to_event_route(input_data,player,current_app)        
    else:
        modified_player = change_existing_player_in_event_route(player, current_app, input_data)
    player_serializer = generate_player_to_dict_serializer(serializer.player.ALL)    
    user_dict=player_serializer(modified_player)
    return jsonify({'existing_player_added_to_event':user_dict})

@blueprints.event_blueprint.route('/player',methods=['GET'])
@blueprints.pss_admin_event_blueprint.route('/player',methods=['GET'])
@load_tables
def get_existing_players(tables):                
    existing_players = tables.Players.query.options(joinedload("player_roles"),joinedload("events"),joinedload("event_player")).all()
    pss_player_serializer = generate_player_to_dict_serializer(serializer.player.ALL)
    existing_players_list = []
    for existing_player in existing_players:        
        user_dict = pss_player_serializer(existing_player)                
        existing_players_list.append(user_dict)
    
    return jsonify({'existing_players':existing_players_list})


@blueprints.event_blueprint.route('/event_player',methods=['GET'])
@load_tables
def get_existing_event_players(tables):                
    existing_players = tables.Players.query.options(joinedload("player_roles"),joinedload("events"),joinedload("event_player")).filter(tables.Players.event_player!=None).all()
    player_serializer = generate_player_to_dict_serializer(serializer.player.ALL)
    existing_players_list = []
    for existing_player in existing_players:        
        user_dict = player_serializer(existing_player)                
        existing_players_list.append(user_dict)
    
    return jsonify({'existing_event_players':existing_players_list})

@blueprints.event_blueprint.route('/event_player/<player_id>',methods=['GET'])
@load_tables
def get_existing_event_player(tables,player_id):                
    existing_player = tables.Players.query.options(joinedload("player_roles"),joinedload("events"),joinedload("event_player")).filter_by(player_id=player_id).first()
    if existing_player is None:
        raise BadRequest('Player does not exist')
    if existing_player is not None and existing_player.event_player is None:
        raise BadRequest('Player is not in this event')
    player_serializer = generate_player_to_dict_serializer(serializer.player.ALL)
    user_dict = player_serializer(existing_player)                            
    return jsonify({'existing_player':user_dict})

@blueprints.pss_admin_event_blueprint.route('/player/<player_id>',methods=['GET'])
@load_tables
def get_existing_player(tables,player_id):                
    existing_player = tables.Players.query.options(joinedload("player_roles"),joinedload("events"),joinedload("event_player")).filter_by(player_id=player_id).first()
    player_serializer = generate_player_to_dict_serializer(serializer.player.ALL)
    user_dict = player_serializer(existing_player)                            
    return jsonify({'existing_player':user_dict})
    

