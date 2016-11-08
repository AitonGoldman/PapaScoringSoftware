from blueprints import admin_login_blueprint,admin_manage_blueprint
from flask import jsonify,current_app,request
import json
from werkzeug.exceptions import BadRequest,Conflict
from util import db_util
from util.permissions import Admin_permission
from flask_login import login_required,current_user
from routes.utils import fetch_entity

@admin_manage_blueprint.route('/division/<division_id>',methods=['GET'])
def route_get_division(division_id):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)            
    return jsonify({'data': tables.Division.query.filter_by(division_id=division_id).first().to_dict_simple()})


@admin_manage_blueprint.route('/division',methods=['POST'])
@login_required
@Admin_permission.require(403)
def route_add_division():
    division_data = json.loads(request.data)
    if 'division_name' not in division_data or division_data['division_name'] is None or division_data['division_name'] == "":        
        raise BadRequest('division_name not found in post data')
    if 'tournament_id' not in division_data:
        raise BadRequest('tournament_id not found in division_data')
    if 'scoring_type' not in division_data:        
        raise BadRequest('did not specify scoring type')            
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)    
    if tables.Division.query.filter_by(division_name=division_data['division_name'],tournament_id=division_data['tournament_id']).first():
        raise Conflict('You are trying to create a duplicate tournament')
    
    new_division = tables.Division(            
        division_name = division_data["division_name"],
        finals_num_qualifiers = division_data['finals_num_qualifiers'],
        tournament_id=division_data["tournament_id"]
    )        
    if division_data['scoring_type'] == "HERB":
        new_division.number_of_scores_per_entry=1
    if 'use_stripe' in division_data and division_data['use_stripe']:
        new_division.use_stripe = True
        new_division.stripe_sku=division_data['stripe_sku']
    if 'local_price' in division_data and division_data['use_stripe'] == False: 
        new_division.local_price=division_data['local_price']
    if 'team_tournament' in division_data and division_data['team_tournament']:    
        new_division.team_tournament = True
    else:
        new_division.team_tournament = False    
    new_division.scoring_type=division_data['scoring_type']            
    db.session.add(new_division)
    db.session.commit()

    return jsonify({'data':new_division.to_dict_simple()})


@admin_manage_blueprint.route('/division/<division_id>',methods=['PUT'])
@login_required
@Admin_permission.require(403)
def route_edit_division(division_id):
    division_data = json.loads(request.data)
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    division = fetch_entity(tables.Division,division_id)
    if 'division_id' not in division_data:
        raise BadRequest('No DivisionId specified')
    # FIXME : need to deal with single division vs multiple division name editing (i.e. tournament_name is calculated)
    #if 'division_name' in division_data and division.division_name != division_data['division_name']:
    #    dup_division = tables.Division.query.filter_by(division_name=division_data['division_name'],tournament_id=division.tournament_id).first()
    #    if dup_division:
    #        raise Conflict('You are trying to create a duplicate division')
    #    division.division_name=division_data['division_name']
    if 'active' in division_data:
        if  division_data['active'] == True:
            division.active = True
        else:
            division.active = False    
    if 'finals_num_qualifiers' in division_data:
        division.finals_num_qualifiers = division_data['finals_num_qualifiers']    
    if 'team_tournament' in division_data:
        division.team_tournament = division_data['team_tournament']
    if 'use_stripe' in division_data and 'stripe_sku' in division_data:        
        division.use_stripe=division_data['use_stripe']
        if division.use_stripe:            
            division.stripe_sku = division_data['stripe_sku']
        elif 'local_price' in division_data:            
            division.local_price = division_data['local_price']    
    db.session.commit()
    return jsonify({'data':division.to_dict_simple()})
            
