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
import stripe
import datetime

# 1) total number (non-comped) single and discount tickets sold per division
# 2) total number comped single and discount tickets sold per division
# 3) total number (non-comped) single and discount tickets sold per division through stripe
# 4) total number (non-comped) single and discount tickets sold per division NOT through stripe

@admin_manage_blueprint.route('/reports/all_division_ticket_summary',methods=['GET'])
def route_get_ticket_summary_for_all_divisions():
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    divisions = [division for division in tables.Division.query.all() if division.meta_division_id is None]    
    meta_divisions = [meta_division for meta_division in tables.MetaDivision.query.all()]
    division_ticket_counts = {}
    meta_division_ticket_counts = {}
    for division in divisions:
        if division.meta_division_id is None:
            division_ticket_counts[division.division_id]=get_ticket_purchases_for_division(division)            
    for meta_division in meta_divisions:
        meta_division_ticket_counts[meta_division.meta_division_id]=get_ticket_purchases_for_division(meta_division)        
    #get_purchase_summary()
    return jsonify({'data':{'divisions':division_ticket_counts,'meta_divisions':meta_division_ticket_counts}})

def get_purchase_summary():
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)    
    stripe.api_key = current_app.td_config['STRIPE_API_KEY']
    purchase_summarys = tables.PurchaseSummary.query.all()
    for purchase_summary in purchase_summarys:                
        if purchase_summary.stripe_charge_id:                                    
            charge_id = purchase_summary.stripe_charge_id
            charge=stripe.Charge.retrieve(charge_id)
            balance_transaction = stripe.BalanceTransaction.retrieve(charge.balance_transaction)            
            print balance_transaction.net
            print balance_transaction.id
 
def get_ticket_purchases_for_division(division,count_stripe=False):    
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)    
    division_ticket_counts={"normal":0,"discount":0,"stripe_normal":0,"stripe_discount":0}    
    if division.discount_ticket_count:
        discount_ticket_count = division.discount_ticket_count
    else:
        discount_ticket_count = 0
    if division.meta_division_id:
        division_ticket_purchases = tables.TicketPurchase.query.filter_by(meta_division_id=division.meta_division_id).all()
        
    else:
        division_ticket_purchases = tables.TicketPurchase.query.filter_by(division_id=division.division_id).all()
        
        
    for division_ticket_purchase in division_ticket_purchases:
        if division_ticket_purchase.description == "1":            
            division_ticket_counts["normal"]=division_ticket_counts["normal"]+division_ticket_purchase.amount
            if division_ticket_purchase.purchase_summary.stripe_charge_id:
                division_ticket_counts["stripe_normal"]=division_ticket_counts["stripe_normal"]+division_ticket_purchase.amount                
        else:
            division_ticket_counts["discount"]=division_ticket_counts["discount"]+division_ticket_purchase.amount
            if division_ticket_purchase.purchase_summary.stripe_charge_id:
                division_ticket_counts["stripe_discount"]=division_ticket_counts["stripe_discount"]+division_ticket_purchase.amount
    return division_ticket_counts
