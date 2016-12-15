from blueprints import admin_login_blueprint,admin_manage_blueprint
from flask import jsonify,current_app,request
import json
from werkzeug.exceptions import BadRequest,Conflict,Forbidden
from util import db_util
from util.permissions import Admin_permission, Desk_permission, Token_permission
from flask_login import login_required,current_user
from routes.utils import fetch_entity,calc_audit_log_remaining_tokens
import os
from flask_restless.helpers import to_dict
import datetime

def get_existing_token_count(player_id=None,team_id=None,div_id=None,metadiv_id=None):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)

    query = None
    if div_id:
        query =  tables.Token.query.filter_by(division_id=div_id,paid_for=True,used=False)
    if metadiv_id:
        query = tables.Token.query.filter_by(metadivision_id=metadiv_id,paid_for=True,used=False)
    if player_id:
        query = query.filter_by(player_id=player_id)
    if team_id:
        query = query.filter_by(team_id=team_id)
    return query.count()

def check_linked_division(division_id, player_id=None, team_id=None):
    #FIXME : this should have actual contents
    pass
        
def check_add_token_for_max_tokens(num_tokens,div_id=None,metadiv_id=None,player_id=None,team_id=None):        
    if player_id:
        existing_token_count = get_existing_token_count(div_id=div_id,metadiv_id=metadiv_id,player_id=player_id)        
    if team_id:
        existing_token_count = get_existing_token_count(div_id=div_id,team_id=team_id)
    if metadiv_id:
        existing_token_count = get_existing_token_count(metadiv_id=metadiv_id,player_id=player_id)
        #FIXME : we assume metadivisions are not also team divisions
    if int(num_tokens) + int(existing_token_count) > int(current_app.td_config['MAX_TICKETS_ALLOWED_PER_DIVISION']):
        raise Conflict('Token add requested will push you over the max tokens for this division')


def check_add_token_request_is_valid(tokens_data, tables):
    if tokens_data.has_key('player_id') is False:
        raise BadRequest('No player_id specified')
    if tokens_data.has_key('divisions') is False and tokens_data.has_key('meta_divisions') is False and tokens_data.has_key('teams') is False:
        raise BadRequest('No divisions specified for tokens')
    player_id = tokens_data['player_id']
    if tokens_data.has_key('team_id'):
        team_id = tokens_data['team_id']
        team = fetch_entity(tables.Player,team_id)
    fetch_entity(tables.Player,tokens_data['player_id'])
    for div_id in tokens_data['divisions']:
        division=fetch_entity(tables.Division,div_id)
        if division.team_tournament is True:
            raise BadRequest('Tried to add a token for a single player in a team tournament')
        if division.meta_division_id is not None:
            raise BadRequest('Tried to add a division token to a metadivision')                    
        num_tokens = tokens_data['divisions'][div_id]
        check_add_token_for_max_tokens(num_tokens,div_id=div_id,player_id=player_id)        
    for div_id in tokens_data['teams']:
        division=fetch_entity(tables.Division,div_id)
        if division.team_tournament is False:
            raise BadRequest('Tried to add a token for a team in a non-team tournament')
        num_tokens = tokens_data['teams'][div_id]
        if int(num_tokens) > 0:
            check_add_token_for_max_tokens(num_tokens,div_id=div_id,team_id=team_id)        
    for metadiv_id in tokens_data['metadivisions']:
        meta_division=fetch_entity(tables.MetaDivision,metadiv_id)
        num_tokens = tokens_data['metadivisions'][metadiv_id]        
        check_add_token_for_max_tokens(num_tokens,metadiv_id=metadiv_id,player_id=player_id)                     
    
def create_division_tokens(num_tokens,div_id=None,metadiv_id=None,player_id=None,team_id=None, paid_for=1, comped=False, player_id_for_team_audit_log=None):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    tokens = []
    json_tokens = []
    for token_num in range(0,int(num_tokens)):
        new_token = tables.Token()    
        if player_id:
            new_token.player_id=player_id                    
        if team_id:
            new_token.team_id=team_id
        if div_id:
            new_token.division_id = div_id
        if metadiv_id:
            new_token.metadivision_id = metadiv_id
        new_token.paid_for = True if paid_for == 1 else False
        new_token.used=False
        new_token.comped=comped
        if hasattr(current_user,'user_id'):
            new_token.deskworker_id=current_user.user_id
        
        db.session.add(new_token)                
        db.session.commit()
        audit_log = tables.AuditLog()
        if paid_for == 1:
            audit_log.purchase_date = datetime.datetime.now()
        if player_id:
            audit_log.player_id = player_id
        if team_id:
            audit_log.team_id = team_id
            
        audit_log.token_id=new_token.token_id
        audit_log.deskworker_id=current_user.user_id
        audit_log.num_tokens_purchased_in_batch=num_tokens
        #FIXME : needs serious refactoring -
        #        we need to jump through these hoops because we want both team and player tokens to be looked up when creating the
        #        remaining tokens part of the audit log 
        if player_id is None:
            if player_id_for_team_audit_log is not None:
                player_id_for_calc_remaining_tokens = player_id_for_team_audit_log
        else:
            player_id_for_calc_remaining_tokens = player_id
        tokens_left_string = calc_audit_log_remaining_tokens(player_id_for_calc_remaining_tokens,team_id)
        audit_log.remaining_tokens = tokens_left_string        
        db.session.add(audit_log)
        db.session.commit()
        tokens.append(to_dict(new_token))
    return tokens

@admin_manage_blueprint.route('/token/teams/<player_id>',methods=['GET'])
def get_team_tokens_for_player(player_id):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    teams = fetch_entity(tables.Player,player_id)         

    token_dict = {'teams':{}}    
    team = Team.query.filter(Team.players.any(Player.player_id.__eq__(player.player_id))).first()    
    if team is None:
        return jsonify(token_dict)    
    tokens = Token.query.filter_by(team_id=team.team_id,paid_for=True).all()
    
    #FIXME : need only active divisions
    divisions = Division.query.all()
    for division in divisions:
        token_dict['teams'][division.division_id]=0
    for token in tokens:        
        if token.team_id != None:
            token_dict['teams'][token.division_id]=token_dict['teams'][token.division_id] + 1      
    return jsonify(token_dict)

@admin_manage_blueprint.route('/token/player_id/<player_id>',methods=['GET'])
def get_tokens_for_player(player_id):
    #FIXME : needs more protection?
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    player = fetch_entity(tables.Player,player_id)
    team_ids = tables.Team.query.filter(tables.Team.players.any(player_id=player.player_id)).all()
    tokens = tables.Token.query.filter_by(player_id=player.player_id, paid_for=True).all()
    token_dict = {'divisions':{},'metadivisions':{},'teams':{}}
    remaining_tokens_dict={'divisions':{},'metadivisions':{},'teams':{}}
    #FIXME : need only active divisions
    divisions = tables.Division.query.all()    
    metadivisions = tables.MetaDivision.query.all()
    max_tickets_allowed = int(current_app.td_config['MAX_TICKETS_ALLOWED_PER_DIVISION'])
    for division in divisions:
        if division.team_tournament is False and division.meta_division_id is None:
            if division.tournament.single_division or division.tournament.single_division is False and division.division_id == player.linked_division_id:
                div_count = get_existing_token_count(player_id=player_id, div_id=division.division_id)                
                token_dict['divisions'][division.division_id]=div_count
                remaining_tokens_dict['divisions'][division.division_id] = max_tickets_allowed - div_count
        if division.meta_division_id is not None:
            metadiv_count = get_existing_token_count(player_id=player_id,metadiv_id=division.meta_division_id)
            token_dict['metadivisions'][division.meta_division_id]= metadiv_count
            remaining_tokens_dict['metadivisions'][division.meta_division_id] = max_tickets_allowed - metadiv_count
        if division.team_tournament is True:
            for team in team_ids:
                team_count = get_existing_token_count(team_id=team.team_id,div_id=division.division_id)
                token_dict['teams'][division.division_id]= team_count
                remaining_tokens_dict['teams'][division.division_id] = max_tickets_allowed - team_count
            
    return jsonify({'data':{'tokens':token_dict,'available_tokens':remaining_tokens_dict,'player':player.to_dict_simple()}})

@admin_manage_blueprint.route('/token/confirm_paid_for', methods=['PUT'])
@login_required
def confirm_tokens():
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    tokens_data = json.loads(request.data)['total_tokens']
    for token in tokens_data:
        token = fetch_entity(tables.Token,token['token_id'])
        if token:
            token.paid_for=True
            tables.db_handle.session.commit()
        #DB.session.add(new_audit_log_entry)
        #tables.db_handle.session.commit()        
            
    return jsonify({'data':token.to_dict_simple()})

@admin_manage_blueprint.route('/token/paid_for/<int:paid_for>', methods=['POST'])
@login_required
@Token_permission.require(403)
def add_token(paid_for):
    if current_user.is_player and paid_for != 0:
        raise Forbidden('Stop being a dick, you assface')        
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)    
    total_tokens=[]
    tokens_data = json.loads(request.data)
    check_add_token_request_is_valid(tokens_data, tables)    
    player_id = tokens_data['player_id']
    if 'comped' in tokens_data:
        comped = tokens_data['comped']
    else:
        comped = False
    player = fetch_entity(tables.Player,tokens_data['player_id'])
    if tokens_data.has_key('team_id'):
        team_id = tokens_data['team_id']
        team = fetch_entity(tables.Player,team_id)
    # FIXME : we rely on team_id being passed in - should check for it here
    for div_id in tokens_data['divisions']:
        num_tokens = tokens_data['divisions'][div_id]
        if num_tokens > 0:
            tokens = create_division_tokens(num_tokens,div_id=div_id,player_id=player_id, paid_for=paid_for,comped=comped)
            total_tokens = total_tokens + tokens
    for metadiv_id in tokens_data['metadivisions']:
        num_tokens = tokens_data['metadivisions'][metadiv_id]
        if num_tokens > 0:
            tokens = create_division_tokens(num_tokens,metadiv_id=metadiv_id,player_id=player_id, paid_for=paid_for,comped=comped)
            total_tokens = total_tokens + tokens
    for div_id in tokens_data['teams']:
        num_tokens = tokens_data['teams'][div_id]
        if int(num_tokens) > 0:
            check_add_token_for_max_tokens(num_tokens,div_id=div_id,team_id=team_id)
            tokens = create_division_tokens(num_tokens,div_id=div_id,team_id=team_id,paid_for=paid_for,comped=comped,player_id_for_team_audit_log=player_id)
            total_tokens = total_tokens + tokens
            
    db.session.commit()
    total_divisions_tokens_summary = {}
    total_metadivisions_tokens_summary = {}
    for div_id in tokens_data['divisions']:
        total_divisions_tokens_summary[div_id] = len([token for token in total_tokens if str(token['division_id'])==str(div_id)])
    for div_id in tokens_data['teams']:
        total_divisions_tokens_summary[div_id] = len([token for token in total_tokens if str(token['division_id'])==str(div_id)])
    for metadiv_id in tokens_data['metadivisions']:
        total_metadivisions_tokens_summary[metadiv_id] = len([token for token in total_tokens if str(token['metadivision_id'])==str(metadiv_id)])
         
    return jsonify({'data':{'divisions':total_divisions_tokens_summary,
                            'metadivisions':total_metadivisions_tokens_summary,                            
                            'tokens':total_tokens}})


