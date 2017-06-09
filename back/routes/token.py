from blueprints import admin_login_blueprint,admin_manage_blueprint
from flask import jsonify,current_app,request
import json
from werkzeug.exceptions import BadRequest,Conflict,Forbidden
from util import db_util
from util.permissions import Admin_permission, Desk_permission, Token_permission
from flask_login import login_required,current_user
from routes.utils import fetch_entity,calc_audit_log_remaining_tokens,get_discount_normal_ticket_counts
import os
from flask_restless.helpers import to_dict
import datetime
from routes.audit_log_utils import create_audit_log
from orm_creation import create_ticket_purchase,create_purchase_summary

# gets_all_available tokens for a given division or metadiv for a given player or team
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

# retrieving player
# retrieve each division for teams, metadivisions, and divisions
# call check_add_token_for_max_tokens for all teams, metadivisions, and divisions
def check_add_token_request_is_valid(tokens_data, tables):
    if tokens_data.has_key('player_id') is False:
        raise BadRequest('No player_id specified')
    if tokens_data.has_key('divisions') is False and tokens_data.has_key('meta_divisions') is False and tokens_data.has_key('teams') is False:
        raise BadRequest('No divisions specified for tokens')
    player_id = tokens_data['player_id']
    player = fetch_entity(tables.Player,tokens_data['player_id'])
    if tokens_data.has_key('team_id'):
        team_id = tokens_data['team_id']
        team = fetch_entity(tables.Team,team_id)
    elif len(player.teams) > 0:
        team_id=player.teams[0].team_id
    else:
        team_id=None
            
    for div_id in tokens_data['divisions']:
        division=fetch_entity(tables.Division,div_id)
        if division.team_tournament is True:
            raise BadRequest('Tried to add a token for a single player in a team tournament')
        if division.meta_division_id is not None:
            raise BadRequest('Tried to add a division token to a metadivision')                    
        if div_id in tokens_data['divisions'] and len(tokens_data['divisions'][div_id]) > 0:
            num_tokens = tokens_data['divisions'][div_id][0]
        else:
            num_tokens = 0            
        if int(num_tokens) > 0: 
            check_add_token_for_max_tokens(num_tokens,div_id=div_id,player_id=player_id)        
    for div_id in tokens_data['teams']:
        division=fetch_entity(tables.Division,div_id)
        if division.team_tournament is False:
            raise BadRequest('Tried to add a token for a team in a non-team tournament')
        if div_id in tokens_data['teams'] and len(tokens_data['teams'][div_id]) > 0:
            num_tokens = tokens_data['teams'][div_id][0]
        else:
            num_tokens = 0
        if int(num_tokens) > 0:
            check_add_token_for_max_tokens(num_tokens,div_id=div_id,team_id=team_id)        
    for metadiv_id in tokens_data['metadivisions']:
        meta_division=fetch_entity(tables.MetaDivision,metadiv_id)
        if metadiv_id in tokens_data['metadivisions'] and len(tokens_data['metadivisions'][metadiv_id]) > 0:
            num_tokens = tokens_data['metadivisions'][metadiv_id][0]
        else:
            num_tokens = 0
        if int(num_tokens) > 0:
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
        ##db.session.commit()
        ##tokens.append(to_dict(new_token))
        tokens.append(new_token)        
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

    
def get_available_ticket_list(max_count,division,increment=None):        
    if increment is None:
        increment = 1
    available_ticket_list = [[0,0]]
    
    #normal_cost = 5
    if division.local_price:
        normal_cost = division.local_price 
    else:
        normal_cost = 0        
    if division.discount_ticket_count:
        #discount_count = 3
        discount_count = division.discount_ticket_count
        #discount_cost = 12
        discount_cost = division.discount_ticket_price
    else:
        discount_count = 1
        discount_cost = 0
    return get_discount_normal_ticket_counts(max_count,discount_count,discount_cost,increment,normal_cost)
    # 0,0
    # 3:10
    # 6:20
    # 7:20
    # 9:30
    # 10:30
    # 11:X
    # 12:40
    # 13:40
    # 14:40
    # 15:50
    # 16:50
    # 17:50
    # 18:60
    # 19:60
    # 20:60
    # 21:60
    # 22:70
    # 23:70
    # 24:70
    # 25:80        

def get_total_tokens_for_player(app, tokens, divisions, team_tokens=[]):
    #tokens = app.tables.Token.query.filter_by(player_id=player_id, paid_for=True).all()
    #team = app.tables.Team.query.filter(app.tables.Team.players.any(player_id=player_id)).first()
    #divisions = app.tables.Division.query.all()
    total_tokens = {'divisions':{},'metadivisions':{}}
    for division in divisions:
        if division.meta_division_id:
            total_tokens['metadivisions'][division.meta_division_id]=0
        else:            
            total_tokens['divisions'][division.division_id]=0            
    for token in tokens:        
        if token.division_id:            
            total_tokens['divisions'][token.division_id]=total_tokens['divisions'][token.division_id]+1
        if token.metadivision_id:            
            total_tokens['metadivisions'][token.metadivision_id]=total_tokens['metadivisions'][token.metadivision_id]+1
    for token in team_tokens:        
        total_tokens['divisions'][token.division_id]=total_tokens['divisions'][token.division_id]+1

    return total_tokens
    

@admin_manage_blueprint.route('/token/player_id/<player_id>/total',methods=['GET'])
@login_required
@Desk_permission.require(403)
def route_get_total_tokens_for_player(player_id):
    tokens = current_app.tables.Token.query.filter_by(player_id=player_id, paid_for=True).all()
    team = current_app.tables.Team.query.filter(current_app.tables.Team.players.any(player_id=player_id)).first()
    divisions = current_app.tables.Division.query.all()
    if team:
        team_tokens =  current_app.tables.Token.query.filter_by(team_id=team.team_id, paid_for=True).all()
    else:
        team_tokens=[]
    #get_total_tokens_for_player(app, player_id, tokens, divisions, team_tokens=[]):
    total_tokens = get_total_tokens_for_player(current_app,tokens,divisions,team_tokens)
    return jsonify({'data':total_tokens})
 
@admin_manage_blueprint.route('/token/player_id/<player_id>',methods=['GET'])
def get_tokens_for_player(player_id):
    #FIXME : needs more protection?
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    divisions = tables.Division.query.all()    
    player = fetch_entity(tables.Player,player_id)
    team_ids = tables.Team.query.filter(tables.Team.players.any(player_id=player.player_id)).all()
    if team_ids:
        team_id=tables.Team.query.filter(tables.Team.players.any(player_id=player.player_id)).first().team_id
    else:
        team_id=None
    if team_id:
        team_tokens=current_app.tables.Token.query.filter_by(team_id=team_id, paid_for=True).all()
    else:
        team_tokens=[]            
    tokens = tables.Token.query.filter_by(player_id=player.player_id, paid_for=True).all()
    if current_user.is_player:
        total_tokens={}
    else:
        total_tokens = get_total_tokens_for_player(current_app,tokens,divisions,team_tokens)
    token_dict = {'divisions':{},'metadivisions':{},'teams':{}}
    remaining_tokens_dict={'divisions':{},'metadivisions':{},'teams':{},
                           'divisions_remaining_token_list':{},
                           'teams_remaining_token_list':{},
                           'metadivisions_remaining_token_list':{}}
    #FIXME : need only active divisions
    metadivisions = tables.MetaDivision.query.all()
    max_tickets_allowed = int(current_app.td_config['MAX_TICKETS_ALLOWED_PER_DIVISION'])
    for division in divisions:
        if division.team_tournament is False and division.meta_division_id is None:
            if division.tournament.single_division or division.tournament.single_division is False and division.division_id == player.linked_division_id:
                div_count = get_existing_token_count(player_id=player_id, div_id=division.division_id)                
                token_dict['divisions'][division.division_id]=div_count
                remaining_tokens = max_tickets_allowed - div_count
                remaining_tokens_dict['divisions'][division.division_id] = remaining_tokens                
                remaining_tokens_dict['divisions_remaining_token_list'][division.division_id]=get_available_ticket_list(remaining_tokens,division,division.min_num_tickets_to_purchase)[0]
        if division.meta_division_id is not None:
            metadivision = tables.MetaDivision.query.filter_by(meta_division_id=division.meta_division_id).first()
            metadiv_count = get_existing_token_count(player_id=player_id,metadiv_id=division.meta_division_id)
            token_dict['metadivisions'][division.meta_division_id]= metadiv_count
            remaining_tokens = max_tickets_allowed - metadiv_count             
            remaining_tokens_dict['metadivisions'][division.meta_division_id] = remaining_tokens
            remaining_tokens_dict['metadivisions_remaining_token_list'][division.meta_division_id]=get_available_ticket_list(remaining_tokens,metadivision,division.min_num_tickets_to_purchase)[0]            
        if division.team_tournament is True:
            for team in team_ids:
                team_count = get_existing_token_count(team_id=team.team_id,div_id=division.division_id)
                remaining_tokens = max_tickets_allowed - team_count
                token_dict['teams'][division.division_id]= team_count
                remaining_tokens_dict['teams'][division.division_id] = remaining_tokens
                remaining_tokens_dict['teams_remaining_token_list'][division.division_id]=get_available_ticket_list(remaining_tokens,division,division.min_num_tickets_to_purchase)[0]
                
    return jsonify({'data':{'total_tokens':total_tokens,'tokens':token_dict,'available_tokens':remaining_tokens_dict,'player':player.to_dict_simple()}})

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

# fetch player
# fetch divisions
# create_division_tokens

@admin_manage_blueprint.route('/token/paid_for/<int:paid_for>', methods=['POST'])
@login_required
@Token_permission.require(403)
def add_token(paid_for):
    if current_user.is_player and paid_for != 0:
        raise Forbidden('Stop being a dick, you assface')        
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)    
    total_tokens=[]
    #tokens = []
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
        team = fetch_entity(tables.Team,team_id)
    #else:
    elif len(player.teams) > 0:
        team_id=player.teams[0].team_id
    else:
        team_id=None    

    division_token_summary = {}
    metadivision_token_summary = {}

    for div_id in tokens_data['divisions']:
        #num_tokens = tokens_data['divisions'][div_id]
        if div_id in tokens_data['divisions'] and len(tokens_data['divisions'][div_id]) > 0:
            num_tokens = int(tokens_data['divisions'][div_id][0])
        else:
            num_tokens = 0
        if num_tokens > 0:
            division_token_summary[tables.Division.query.filter_by(division_id=div_id).first().get_self_tournament_name()]=num_tokens
            ## back 
            tokens = create_division_tokens(num_tokens,div_id=div_id,player_id=player_id, paid_for=paid_for,comped=comped)
            total_tokens = total_tokens + tokens
    for metadiv_id in tokens_data['metadivisions']:
        if metadiv_id in tokens_data['metadivisions'] and len(tokens_data['metadivisions'][metadiv_id]) > 0:
            num_tokens = tokens_data['metadivisions'][metadiv_id][0]
        else:
            num_tokens = 0
        if num_tokens > 0:
            metadivision_token_summary[tables.Division.query.filter_by(meta_division_id=metadiv_id).first().get_self_tournament_name()]=num_tokens

            tokens = create_division_tokens(num_tokens,metadiv_id=metadiv_id,player_id=player_id, paid_for=paid_for,comped=comped)
            total_tokens = total_tokens + tokens

    for div_id in tokens_data['teams']:
        if div_id in tokens_data['teams'] and len(tokens_data['teams'][div_id]) > 0:
            num_tokens = tokens_data['teams'][div_id][0]
        else:
            num_tokens = 0
        if int(num_tokens) > 0:
            division_token_summary[tables.Division.query.filter_by(division_id=div_id).first().get_self_tournament_name()]=num_tokens
            check_add_token_for_max_tokens(num_tokens,div_id=div_id,team_id=team_id)
            tokens = create_division_tokens(num_tokens,div_id=div_id,team_id=team_id,paid_for=paid_for,comped=comped,player_id_for_team_audit_log=player_id)            
            total_tokens = total_tokens + tokens        
    db.session.commit()
    division_ticket_summary = ", ".join(["%s : %s"%(div_name,div_count) for div_name,div_count in division_token_summary.iteritems()]+["%s : %s"%(div_name,div_count) for div_name,div_count in metadivision_token_summary.iteritems()])    
    if paid_for == 1:            
        action="Ticket Purchase"
    if paid_for == 0:
        action="Player Ticket Purchase Started"
    if comped:
        division_ticket_summary = division_ticket_summary + " (COMPED)"
    create_audit_log(action,datetime.datetime.now(),
                     division_ticket_summary,user_id=current_user.user_id,
                     player_id=player_id,team_id=team_id,commit=False)    
    
    if paid_for == 1:
        if player_id:
            tokens_left_string = calc_audit_log_remaining_tokens(player_id)
        create_audit_log("Ticket Summary(AP)",datetime.datetime.now(),
                         tokens_left_string,user_id=current_user.user_id,
                         player_id=player_id,team_id=team_id,commit=False)
    total_divisions_tokens_summary = {}
    total_metadivisions_tokens_summary = {}
    # for each div/metadiv
    #   calculate num of single
    #   calculate num of discount 
    #   create audit_logs for both

    if paid_for == 1 and comped is False:
        purchase_summary = create_purchase_summary(current_app,
                                                   player_id)
    divisions_count={}
    teams_count={}
    metadivisions_count={}
    for div_id in tokens_data['divisions']:
        ##total_divisions_tokens_summary[div_id] = len([token for token in total_tokens if str(token['division_id'])==str(div_id)])
        total_divisions_tokens_summary[div_id] = len([token for token in total_tokens if str(token.division_id)==str(div_id)])
        if paid_for == 1 and comped is False:
            divisions_count[div_id]=create_ticket_purchase(current_app,
                                                            total_divisions_tokens_summary[div_id],
                                                            player_id,
                                                            current_user.user_id,
                                                            purchase_summary.purchase_summary_id,
                                                            division_id=div_id,
                                                            commit=False)            
    for div_id in tokens_data['teams']:
        total_divisions_tokens_summary[div_id] = len([token for token in total_tokens if str(token.division_id)==str(div_id)])
        if paid_for == 1 and comped is False:
            divisions_count[div_id] = create_ticket_purchase(current_app,
                                                             total_divisions_tokens_summary[div_id],
                                                             player_id,
                                                             current_user.user_id,
                                                             purchase_summary.purchase_summary_id,
                                                             division_id=div_id,
                                                             commit=False)
    for metadiv_id in tokens_data['metadivisions']:
        total_metadivisions_tokens_summary[metadiv_id] = len([token for token in total_tokens if str(token.metadivision_id)==str(metadiv_id)])
        if paid_for == 1 and comped is False:
            metadivisions_count[metadiv_id] = create_ticket_purchase(current_app,
                                                                     total_metadivisions_tokens_summary[metadiv_id],
                                                                     player_id,
                                                                     current_user.user_id,
                                                                     purchase_summary.purchase_summary_id,                                   
                                                                     metadivision_id=metadiv_id,commit=False)
    db.session.commit()
    ##return jsonify({})
    for idx,tok in enumerate(total_tokens):
        total_tokens[idx] = to_dict(tok)            
    return jsonify({'data':{'divisions':total_divisions_tokens_summary,
                            'metadivisions':total_metadivisions_tokens_summary,                            
                            'tokens':total_tokens,
                            'divisions_count':divisions_count,
                            'teams_count':teams_count,
                            'metadivisions_count':metadivisions_count}})
    

