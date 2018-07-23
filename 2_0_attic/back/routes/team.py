from blueprints import admin_login_blueprint,admin_manage_blueprint
from flask import jsonify,current_app,request
import json
from werkzeug.exceptions import BadRequest,Conflict
from util import db_util
from util.permissions import Admin_permission, Desk_permission
from flask_login import login_required,current_user
from routes.utils import fetch_entity
import os
from orm_creation import create_player,create_user,RolesEnum,create_team
import random

@admin_manage_blueprint.route('/team',methods=['POST'])
@login_required
@Desk_permission.require(403)
def route_add_team():
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    input_data = json.loads(request.data)
    for key in ['player_one_id','player_two_id']:
        if key not in input_data:
            raise BadRequest("You did not specify needed information")        
    player_one = tables.Player.query.filter_by(player_id=input_data['player_one_id']).first()
    player_two = tables.Player.query.filter_by(player_id=input_data['player_two_id']).first()
    if len(player_one.teams) > 0 or len(player_two.teams) > 0:
        raise BadRequest("One of the players is already on a team")                
    new_team = create_team(current_app,{'team_name':player_one.last_name+" / "+player_two.last_name,
                                          'players':[player_one.player_id,player_two.player_id]})
    db.session.commit()
    return jsonify({'data':new_team.to_dict_simple()})

@admin_manage_blueprint.route('/team',methods=['GET'])
def route_get_teams():
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    teams = {team.team_id:team.to_dict_simple() for team in tables.Team.query.all()}
    return jsonify({'data':teams})

