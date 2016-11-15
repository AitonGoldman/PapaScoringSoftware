from blueprints import admin_login_blueprint,admin_manage_blueprint
from flask import jsonify,current_app,request
import json
from werkzeug.exceptions import BadRequest,Conflict
from util import db_util
from util.permissions import Admin_permission
from flask_login import login_required,current_user
from routes.utils import fetch_entity

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
    new_tournament = tables.Tournament(
        tournament_name=tournament_data['tournament_name']                        
    )    
    if 'single_division' in tournament_data and tournament_data['single_division']:        
        if 'finals_num_qualifiers' not in tournament_data or tournament_data['finals_num_qualifiers'] == "":
            print "no qualifiers"
            raise BadRequest('finals_num_qualifiers not found in post data')            
        new_tournament.single_division=True
        new_division = tables.Division(            
            division_name = new_tournament.tournament_name+"_single",
            finals_num_qualifiers = tournament_data['finals_num_qualifiers']
        )
        
        if tournament_data['scoring_type'] == "HERB":
            new_division.number_of_scores_per_entry=1
        if 'use_stripe' in tournament_data and tournament_data['use_stripe']:
            new_division.use_stripe = True
            new_division.stripe_sku=tournament_data['stripe_sku']
        if 'local_price' in tournament_data and tournament_data['use_stripe'] == False: 
            new_division.local_price=tournament_data['local_price']
        if 'team_tournament' in tournament_data and tournament_data['team_tournament']:    
            new_division.team_tournament = True
        else:
            new_division.team_tournament = False    
        new_division.scoring_type=tournament_data['scoring_type']
            
        db.session.add(new_division)
        new_tournament.divisions.append(new_division)
        #db.session.add(new_tournament)
        #db.sesssion.commit()
        # FILL IN DIVISION CREATION CODE HERE
    else:
        new_tournament.single_division=False    
    db.session.add(new_tournament)
    db.session.commit()
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

