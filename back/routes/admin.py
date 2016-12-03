from blueprints import admin_login_blueprint,admin_manage_blueprint
from flask import jsonify,current_app,request
import json
from werkzeug.exceptions import BadRequest,Conflict
from util import db_util
from util.permissions import Admin_permission,Scorekeeper_permission
from flask_login import login_required,current_user
from routes.utils import fetch_entity,check_player_team_can_start_game,set_token_start_time
from orm_creation import create_entry
import datetime

@admin_manage_blueprint.route('/admin/score_id/<score_id>/score/<int:score>',methods=['PUT'])
@login_required
@Admin_permission.require(403)
def route_change_score(score_id,score):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)                
    score_obj = fetch_entity(tables.Score,score_id)
    score_obj.score=score
    db.session.commit()
    return jsonify({'data':None})

@admin_manage_blueprint.route('/admin/entry_id/<entry_id>/void/<void>',methods=['DELETE'])
@login_required
@Admin_permission.require(403)
def route_admin_void_score(entry_id,void):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)                
    entry = fetch_entity(tables.Entry,entry_id)
    if void=="1":
        entry.voided=True
    else:
        entry.voided=False
    db.session.commit()
    return jsonify({'data':None})

@admin_manage_blueprint.route('/admin/division_machine_id/<division_machine_id>/score/<int:score>/player_id/<player_id>',methods=['POST'])
@login_required
@Admin_permission.require(403)
def route_admin_add_score(division_machine_id,score,player_id):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    division_id=fetch_entity(tables.DivisionMachine,division_machine_id).division_id
    entry = create_entry(current_app,player_id,division_machine_id,division_id,score)
    db.session.commit()
    return jsonify({'data':entry.entry_id})
