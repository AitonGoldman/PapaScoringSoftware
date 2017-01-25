from blueprints import admin_login_blueprint,admin_manage_blueprint
from ranking import Ranking
from sqlalchemy.sql import functions
#from sqlalchemy import within_group
from sqlalchemy.orm import join
from sqlalchemy.sql.expression import desc, asc
from flask import jsonify, request, abort, current_app
from util import db_util
from sqlalchemy import null, func, text, and_
from sqlalchemy.sql import select
from routes.utils import fetch_entity
import json


# 1) total number (non-comped) single and discount tickets sold per division
# 2) total number comped single and discount tickets sold per division
# 3) total number (non-comped) single and discount tickets sold per division through stripe
# 4) total number (non-comped) single and discount tickets sold per division NOT through stripe

@admin_manage_blueprint.route('/reports/money_summary/division_id/<division_id>',methods=['GET'])
def route_get_money_spent_for_division(division_id):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    divisions = tables.Division.query.all()
    for division in divisions:
        division_count[division.division_id]=0
    metadivision_count={}
    metadivisions = tables.MetaDivision.query.all()
    for metadivision in metadivisions:
        metadivision_count[metadivision.meta_division_id]=0
    
    total_non_comp_purchases = tables.TicketPurchase.query.all()
    for non_comp_purchase in total_non_comp_purchases:
        if non_comp_purchase.division_id:            
                        division_count[non_comp_purchase.division_id]=division_count[non_comp_purchase.division_id]+non_comp_purchase.amount
            pass
    return jsonify({})
