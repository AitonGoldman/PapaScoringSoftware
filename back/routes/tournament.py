from blueprints import admin_login_blueprint,admin_manage_blueprint
from flask import jsonify,current_app,request
import json
from werkzeug.exceptions import BadRequest,Conflict
from util import db_util
from util.permissions import Admin_permission
from flask_login import login_required,current_user
from routes.utils import fetch_entity
from orm_creation import create_tournament

@admin_manage_blueprint.route('/tournament',methods=['GET'])
def route_get_all_tournaments():
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)            
    tournaments_dict = {tournament.tournament_id: tournament.to_dict_simple() for tournament in tables.Tournament.query.all()}    
    return jsonify({'data': tournaments_dict})

@admin_manage_blueprint.route('/tournament',methods=['POST'])
@login_required
@Admin_permission.require(403)
def route_add_tournament():    
    tournament_data = json.loads(request.data)
    if 'tournament_name' not in tournament_data or tournament_data['tournament_name'] is None or tournament_data['tournament_name'] == "":        
        raise BadRequest('tournament_name not found in post data')
    if 'scoring_type' not in tournament_data:        
        raise BadRequest('did not specify scoring type')            
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)            
    if tables.Tournament.query.filter_by(tournament_name=tournament_data['tournament_name']).first():                
        raise Conflict('You are trying to create a duplicate tournament')
    new_tournament = create_tournament(current_app,tournament_data)
    return jsonify({'data': new_tournament.to_dict_simple()})

@admin_manage_blueprint.route('/tournament/<tournament_id>/division',methods=['GET'])
def route_get_all_tournament_divisions(tournament_id):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    divisions = tables.Division.query.filter_by(tournament_id=tournament_id).all()
    divisions_dict = {division.division_id:division.to_dict_simple() for division in divisions}
    return jsonify({'data':divisions_dict})


@admin_manage_blueprint.route('/tournament/<tournament_id>',methods=['PUT'])
@login_required
@Admin_permission.require(403)
def route_edit_tournament(tournament_id):
    tournament_data = json.loads(request.data)
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    tournament = fetch_entity(tables.Tournament,tournament_id)
    if 'tournament_name' in tournament_data:
        if tables.Tournament.query.filter_by(tournament_name=tournament_data['tournament_name']).first():
            raise Conflict('You are trying to create a duplicate tournament')        
        tournament.tournament_name=tournament_data['tournament_name']
    if 'active' in tournament_data:
        if  tournament_data['active'] == True:
            tournament.active = True
        else:
            tournament.active = False        
    db.session.commit()
    return jsonify({'data': tournament.to_dict_simple()})

