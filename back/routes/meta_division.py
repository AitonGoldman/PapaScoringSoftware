from blueprints import admin_login_blueprint,admin_manage_blueprint
from flask import jsonify,current_app,request
import json
from werkzeug.exceptions import BadRequest,Conflict
from util import db_util
from util.permissions import Admin_permission
from flask_login import login_required,current_user
from routes.utils import fetch_entity
from orm_creation import create_meta_division

@admin_manage_blueprint.route('/meta_division/<meta_division_id>',methods=['GET'])
def route_get_meta_division(meta_division_id):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    meta_division = fetch_entity(tables.MetaDivision,meta_division_id)            
    return jsonify({'data': meta_division.to_dict_simple()})

@admin_manage_blueprint.route('/meta_division',methods=['GET'])
def route_get_meta_divisions():
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    meta_divisions = tables.MetaDivision.query.all()
    return jsonify({'data': {meta_division.meta_division_id:meta_division.to_dict_simple() for meta_division in meta_divisions}})


@admin_manage_blueprint.route('/meta_division',methods=['POST'])
@login_required
@Admin_permission.require(403)
def route_add_meta_division():        
    meta_division_data = json.loads(request.data)
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)                    
    # FIXME : need to load machines as part of init
    # new_meta_division = tables.MetaDivision(
    # )
    # if 'meta_division_name' in meta_division_data:
    #     new_meta_division.meta_division_name=meta_division_data['meta_division_name']
    # if 'divisions' in meta_division_data:
    #     for division in meta_division_data['divisions']:
    #         division_table = fetch_entity(tables.Division,int(division))
    #         new_meta_division.divisions.append(division_table)        
    # tables.db_handle.session.add(new_meta_division)
    # tables.db_handle.session.commit()
    new_meta_division = create_meta_division(current_app,meta_division_data)
    return jsonify({'data':new_meta_division.to_dict_simple()})

@admin_manage_blueprint.route('/meta_division/<meta_division_id>',methods=['PUT'])
@login_required
@Admin_permission.require(403)
def route_edit_meta_division(meta_division_id):        
    meta_division_data = json.loads(request.data)
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)                    
    # FIXME : need to load machines as part of init    
    meta_division = fetch_entity(tables.MetaDivision,int(meta_division_id))
    if 'divisions' in meta_division_data:
        for division in meta_division_data['divisions']:
            division_table = fetch_entity(tables.Division,int(division))
            meta_division.divisions.append(division_table)
        for division in meta_division.divisions:
            if str(division.division_id) not in meta_division_data['divisions']:
                meta_division.divisions.remove(division)
    if 'meta_division_name' in meta_division_data:
        meta_division.meta_division_name=meta_division_data['meta_division_name']
    if 'discount_ticket_count' in meta_division_data:
        meta_division.discount_ticket_count=meta_division_data['discount_ticket_count']
    if 'discount_ticket_price' in meta_division_data:
        meta_division.discount_ticket_price=meta_division_data['discount_ticket_price']
    if 'discount_stripe_sku' in meta_division_data and meta_division_data['discount_stripe_sku']:
        meta_division.discount_stripe_sku=meta_division_data['discount_stripe_sku']
    tables.db_handle.session.commit()
    return jsonify({'data':meta_division.to_dict_simple()})

