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
    token = tables.Token.query.filter_by(division_machine_id=division_machine_id,used=False,player_id=division_machine.player_id).first()
    entry = create_entry(current_app,division_machine.player_id,
                         division_machine.division_machine_id,
                         division_machine.division_id,
                         score=score)
    division_machine.player_id=None
    token.used=True
    token.used_date = datetime.datetime.now()
    db.session.commit()
    
        
    audit_log = tables.AuditLog()
    audit_log.player_id = token.player_id
    audit_log.token_id=token.token_id
    audit_log.scorekeeper_id=current_user.user_id
    audit_log.used_date=datetime.datetime.now()
    audit_log.used=True
    tokens_left_string = calc_audit_log_remaining_tokens(token.player_id)        
    audit_log.remaining_tokens = tokens_left_string
    audit_log.division_machine_id=division_machine.division_machine_id
    db.session.add(audit_log)    
    db.session.commit()
    return jsonify({'data':entry.to_dict_simple()})

@admin_manage_blueprint.route('/entry/division_machine/<division_machine_id>/void',methods=['PUT'])
@login_required
@Scorekeeper_permission.require(403)
def route_void_score(division_machine_id):        
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)                
    division_machine = fetch_entity(tables.DivisionMachine,division_machine_id)
    token = tables.Token.query.filter_by(division_machine_id=division_machine_id,used=False,player_id=division_machine.player_id).first()    
    division_machine.player_id=None
    token.used=True
    token.used_date = datetime.datetime.now()
    token.voided=True
    db.session.commit()

    audit_log = tables.AuditLog()
    audit_log.player_id = token.player_id
    audit_log.token_id=token.token_id
    audit_log.scorekeeper_id=current_user.user_id
    audit_log.voided_date=datetime.datetime.now()
    audit_log.voided=True
    audit_log.division_machine_id=division_machine.division_machine_id    
    tokens_left_string = calc_audit_log_remaining_tokens(token.player_id)        
    audit_log.remaining_tokens = tokens_left_string
    db.session.add(audit_log)    
    db.session.commit()
    
    return jsonify({'data':None})


@admin_manage_blueprint.route('/entry/player/<player_id>',methods=['GET'])
@login_required
@Admin_permission.require(403)
def route_get_player_entries(player_id):        
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)                    
    player_entries = tables.Entry.query.filter_by(player_id=player_id).all()    
    return jsonify({'data':{player_entry.entry_id:player_entry.to_dict_simple() for player_entry in player_entries}})

