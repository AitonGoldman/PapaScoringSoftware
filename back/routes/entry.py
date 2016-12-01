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
    return jsonify({'data':None})
