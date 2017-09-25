from flask_restless.helpers import to_dict
from lib.flask_lib import blueprints
from lib.flask_lib.permissions import create_player_permissions
from flask import jsonify,current_app,request
from werkzeug.exceptions import BadRequest,Unauthorized,Conflict
from flask_login import login_user, logout_user, current_user
import json
from lib import orm_factories,token_helpers
from lib.serializer.player import generate_player_to_dict_serializer
from lib import serializer
from lib.route_decorators.db_decorators import load_tables
from sqlalchemy.orm import joinedload
from lib.route_decorators.auth_decorators import check_current_user_is_active
import time

def check_multi_division_tournament_selection_is_valid(app, player):
    if player.event_player.multi_division_tournament_id is None:
        return
    tournament = app.tables.query.Tournaments.query.filter_by(tournament_id=player.event_player.multi_division_tournament_id)
    if tournament.require_selection_of_multidivision_tournament and player.multi_division_tournament_id is None:
        raise BadRequest('No division in the multi division tournament has been selected')
    if tournament.ifpa_rank_restriction and player.event_player and player.event_player.ifpa_ranking < tournament.ifpa_rank_restriction:
        raise BadRequest('Ifpa restrictions have been violated')    
    pass

def create_player_route(request, app):            
    tables = app.tables
    event = tables.Events.query.filter_by(name=app.name).first()
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('No info in request')        
    if 'first_name' not in input_data or 'last_name' not in input_data:        
        raise BadRequest('Information missing')
    if event.force_ifpa_lookup and 'ifpa_ranking' not in input_data:
        raise BadRequest('No ifpa ranking')
    if event.force_ifpa_lookup is not True and 'ifpa_ranking' not in input_data:
        input_data['ifpa_ranking']=999999
        
    if 'extra_title' in input_data:
        extra_title = input_data['extra_title']
    else:
        extra_title = None
    existing_player=tables.Players.query.filter_by(first_name=input_data['first_name'],
                                                   last_name=input_data['last_name'],
                                                   extra_title=extra_title).first()
    if existing_player is not None:
        raise Conflict('Player %s already exists.' % existing_player)
    
    new_player = orm_factories.create_player(app,
                                             input_data['first_name'],
                                             input_data['last_name'],
                                             input_data['ifpa_ranking'])
    if extra_title:
        new_player.extra_title=extra_title
    if 'ifpa_id' in input_data:
        new_player.ifpa_id=input_data['ifpa_id']
    check_multi_division_tournament_selection_is_valid(app, new_player)        
    if 'multi_division_tournament_id' in input_data:
        new_player.event_player.multi_division_tournament_id = input_data['multi_division_tournament_id']
        
    tables.db_handle.session.add(new_player)
    tables.db_handle.session.commit()
    return new_player

def add_existing_player_to_event_route(input_data,player,app):
    tables = app.tables
    event = tables.Events.query.filter_by(name=app.name).first()
    if event.force_ifpa_lookup and 'ifpa_ranking' not in input_data:
        raise BadRequest('No ifpa ranking')
    if event.force_ifpa_lookup is not True and 'ifpa_ranking' not in input_data:
        input_data['ifpa_ranking']=999999
    
    orm_factories.populate_player(app,
                                  player,
                                  input_data['ifpa_ranking'])
    if 'ifpa_id' in input_data:
        player.ifpa_id=input_data['ifpa_id']
        
    check_multi_division_tournament_selection_is_valid(app, player)
    
    if 'multi_division_tournament_id' in input_data:
        player.event_player.multi_division_tournament_id = input_data['multi_division_tournament_id']
    
    tables.db_handle.session.commit()
    return player

def change_existing_player_in_event_route(player, app, input_data):
    tables = app.tables    
    # FIXME : need ability to use email confirmation for edit player (see http://pythonhosted.org/itsdangerous/ for details on generating token)
    tables.db_handle.session.commit()
    return player

@blueprints.event_blueprint.route('/player',methods=['POST'])
@load_tables
@check_current_user_is_active
@create_player_permissions.require(403)
def create_player(tables):                
    new_player = create_player_route(request,current_app)
    player_serializer = generate_player_to_dict_serializer(serializer.player.ON_PLAYER_CREATE)
    player_dict=player_serializer(new_player)
    return jsonify({'new_player':player_dict})
    

@blueprints.event_blueprint.route('/player',methods=['PUT'])
@load_tables
@check_current_user_is_active
@create_player_permissions.require(403)
def add_existing_player_to_event(tables):                    
    input_data = json.loads(request.data)
    player = tables.Players.query.options(joinedload("player_roles"),
                                          joinedload("event_player"),
                                          joinedload("events")).filter_by(player_id=input_data['player_id']).first()
    if player is None:
        raise BadRequest('No such player')
    event = tables.Events.query.filter_by(name=current_app.name).first()    
    if event not in player.events:
        modified_player = add_existing_player_to_event_route(input_data,player,current_app)        
    else:
        modified_player = change_existing_player_in_event_route(player, current_app, input_data)
    player_serializer = generate_player_to_dict_serializer(serializer.player.ON_PLAYER_CREATE)    
    user_dict=player_serializer(modified_player)
    return jsonify({'new_player':user_dict})

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
    #existing_player = tables.Players.query.options(joinedload("player_roles"),joinedload("events"),joinedload("event_player"),joinedload('token')).filter_by(player_id=player_id).first()
    existing_player = tables.Players.query.options(joinedload("player_roles"),joinedload("events"),joinedload("event_player")).filter_by(player_id=player_id).first()
    tournament_token_count,meta_tournament_token_count = token_helpers.get_number_of_unused_tickets_for_player_in_all_tournaments(existing_player,current_app,remove_empty_tournaments=False)    
    if existing_player is None:
        raise BadRequest('Player does not exist')
    if existing_player is not None and existing_player.event_player is None:
        raise BadRequest('Player is not in this event')
    player_serializer = generate_player_to_dict_serializer(serializer.player.ALL)
    user_dict = player_serializer(existing_player)                            
    user_dict['tournament_tokens']=to_dict(tournament_token_count)
    user_dict['meta_tournament_tokens']=to_dict(meta_tournament_token_count)    
    return jsonify({'existing_player':user_dict})

@blueprints.pss_admin_event_blueprint.route('/player/<player_id>',methods=['GET'])
@load_tables
def get_existing_player(tables,player_id):                
    existing_player = tables.Players.query.options(joinedload("player_roles"),joinedload("events"),joinedload("event_player")).filter_by(player_id=player_id).first()
    if existing_player is None:
        raise BadRequest('Player does not exist')
    player_serializer = generate_player_to_dict_serializer(serializer.player.ALL)
    user_dict = player_serializer(existing_player)                            
    return jsonify({'existing_player':user_dict})
    

