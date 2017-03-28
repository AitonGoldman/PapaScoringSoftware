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
from sqlalchemy import desc,asc

@admin_manage_blueprint.route('/jagoff',methods=['GET'])
@login_required
@Admin_permission.require(403)
def route_get_jagoffs():        
    #machine_data = json.loads(request.data)
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    jagoffs = [player.to_dict_simple() for player in tables.Player.query.order_by(desc(tables.Player.asshole_count)).all() if player.asshole_count > 0]
    return jsonify({'data':jagoffs})
