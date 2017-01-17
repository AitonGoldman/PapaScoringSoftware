from blueprints import admin_login_blueprint,admin_manage_blueprint
from flask import jsonify,current_app,request
import json
from werkzeug.exceptions import BadRequest,Conflict
from util import db_util
from util.permissions import Admin_permission,Scorekeeper_permission
from flask_login import login_required,current_user
from routes.utils import fetch_entity,check_player_team_can_start_game,set_token_start_time,calc_audit_log_remaining_tokens
from orm_creation import create_entry
import datetime
from routes.audit_log_utils import create_audit_log

@admin_manage_blueprint.route('/entry/division_machine/<division_machine_id>/score/<int:score>',methods=['POST'])
@login_required
@Scorekeeper_permission.require(403)
def route_add_score(division_machine_id, score):        
    #machine_data = json.loads(request.data)
    if score <= 0:
        raise BadRequest('Invalid score was entered')
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)                
    division_machine = fetch_entity(tables.DivisionMachine,division_machine_id)
    token = None
    if division_machine.player_id:        
        token = tables.Token.query.filter_by(division_machine_id=division_machine_id,used=False,player_id=division_machine.player_id).first()
    if division_machine.team_id:        
        token = tables.Token.query.filter_by(division_machine_id=division_machine_id,used=False,team_id=division_machine.team_id).first()
    if token is None:        
        raise BadRequest('Tried to add a score without starting a game.')        
    if division_machine.player_id:        
        entry = create_entry(current_app,
                             division_machine.division_machine_id,
                             division_machine.division_id,
                             score=score,
                             player_id=division_machine.player_id)
    if division_machine.team_id:        
        entry = create_entry(current_app,
                             division_machine.division_machine_id,
                             division_machine.division_id,
                             score=score,team_id=division_machine.team_id)

    token.used=True
    token.used_date = datetime.datetime.now()    
    player_id=division_machine.player_id
    team_id=division_machine.team_id
    division_machine.player_id=None
    division_machine.team_id=None
    db.session.commit()
    create_audit_log("Score Added",datetime.datetime.now(),
                     "",user_id=current_user.user_id,
                     player_id=player_id,team_id=team_id,
                     division_machine_id=division_machine.division_machine_id,
                     entry_id=entry.entry_id,token_id=token.token_id)    

    if player_id:
        tokens_left_string = calc_audit_log_remaining_tokens(player_id)
    if team_id:
        tokens_left_string = calc_audit_log_remaining_tokens(None,team_id)
    create_audit_log("Ticket Summary",datetime.datetime.now(),
                     tokens_left_string,user_id=current_user.user_id,
                     player_id=player_id,team_id=team_id)
    return jsonify({'data':entry.to_dict_simple()})

@admin_manage_blueprint.route('/entry/division_machine/<division_machine_id>/void',methods=['PUT'])
@login_required
@Scorekeeper_permission.require(403)
def route_void_score(division_machine_id):        
    print "poop"
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)                
    division_machine = fetch_entity(tables.DivisionMachine,division_machine_id)
    token = None
    if division_machine.player_id:
        token = tables.Token.query.filter_by(division_machine_id=division_machine_id,used=False,player_id=division_machine.player_id).first()
    if division_machine.team_id:
        token = tables.Token.query.filter_by(division_machine_id=division_machine_id,used=False,team_id=division_machine.team_id).first()        
    if token is None:
        raise BadRequest('Tried to void a ticket that does not exist')
    player_id = division_machine.player_id
    team_id = division_machine.team_id

    token.used=True
    token.used_date = datetime.datetime.now()
    token.voided=True
    db.session.commit()
    create_audit_log("Score Voided",datetime.datetime.now(),
                     "",user_id=current_user.user_id,
                     player_id=player_id,team_id=team_id,
                     division_machine_id=division_machine.division_machine_id,
                     token_id=token.token_id)    

    if division_machine.player_id:
        tokens_left_string = calc_audit_log_remaining_tokens(division_machine.player_id)
    if division_machine.team_id:
        tokens_left_string = calc_audit_log_remaining_tokens(None,division_machine.team_id)
    create_audit_log("Ticket Summary",datetime.datetime.now(),
                     tokens_left_string,user_id=current_user.user_id,
                     player_id=player_id,team_id=team_id)

    division_machine.player_id=None
    division_machine.team_id=None    
    db.session.commit()
    
    return jsonify({'data':token.to_dict_simple()})

@admin_manage_blueprint.route('/entry/division_machine/<division_machine_id>/jagoff',methods=['PUT'])
@login_required
@Scorekeeper_permission.require(403)
def route_jagoff(division_machine_id):        
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)                
    division_machine = fetch_entity(tables.DivisionMachine,division_machine_id)
    token = None
    if division_machine.player_id:
        token = tables.Token.query.filter_by(division_machine_id=division_machine_id,used=False,player_id=division_machine.player_id).first()
    if division_machine.team_id:
        token = tables.Token.query.filter_by(division_machine_id=division_machine_id,used=False,team_id=division_machine.team_id).first()        
    if token is None:
        raise BadRequest('Tried to decalre a jagoff inapropriately')
    player_id = division_machine.player_id
    if player_id:
        player = fetch_entity(tables.Player,player_id)
        if player.asshole_count:
            player.asshole_count = player.asshole_count+1
        else:
            player.asshole_count = 1            
    team_id = division_machine.team_id
    if team_id:
        team = fetch_entity(tables.Team,team_id)
        if team.asshole_count:
            team.asshole_count = team.asshole_count+1
        else:
            team.asshole_count = 1            

    division_machine.player_id=None
    division_machine.team_id=None

    token.used=True
    token.used_date = datetime.datetime.now()
    token.voided=True
    db.session.commit()

    create_audit_log("Jagoff Declared",datetime.datetime.now(),
                     "",user_id=current_user.user_id,
                     player_id=player_id,team_id=team_id,
                     division_machine_id=division_machine.division_machine_id,
                     token_id=token.token_id)    

    if player_id:
        tokens_left_string = calc_audit_log_remaining_tokens(player_id)
    if team_id:
        tokens_left_string = calc_audit_log_remaining_tokens(None,team_id)
    create_audit_log("Ticket Summary",datetime.datetime.now(),
                     tokens_left_string,user_id=current_user.user_id,
                     player_id=player_id,team_id=team_id)
        
    return jsonify({'data':token.to_dict_simple()})


@admin_manage_blueprint.route('/entry/player/<player_id>',methods=['GET'])
@login_required
@Admin_permission.require(403)
def route_get_player_entries(player_id):        
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)                    
    player_entries = tables.Entry.query.filter_by(player_id=player_id).all()    
    return jsonify({'data':{player_entry.entry_id:player_entry.to_dict_simple() for player_entry in player_entries}})

