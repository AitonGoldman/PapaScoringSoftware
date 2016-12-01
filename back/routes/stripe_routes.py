from blueprints import admin_login_blueprint,admin_manage_blueprint
from flask import jsonify,current_app,request
import json
from werkzeug.exceptions import BadRequest,Conflict
from util import db_util
from util.permissions import Admin_permission,Scorekeeper_permission
from flask_login import login_required,current_user
from routes.utils import fetch_entity
import stripe


@admin_manage_blueprint.route('/stripe/sku',methods=['GET'])
def get_sku_prices():
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    dict_sku_prices={}
    dict_div_to_sku={}
    stripe.api_key = current_app.td_config['STRIPE_API_KEY']
    divisions = tables.Division.query.all()
    use_stripe = False
    for division in divisions:
        if division.use_stripe is False:
            use_stripe = True
            dict_div_to_sku[division.division_id]=division.local_price
    if use_stripe is False:
        return jsonify({'data':dict_div_to_sku})    
    
    product_list = stripe.Product.list()
    items = product_list['data']        
    
    for item in items:        
        dict_sku_prices[item['skus']['data'][0]['id']]=item['skus']['data'][0]['price']/100    
    for division in divisions:
        if division.use_stripe:
            dict_div_to_sku[division.division_id]=dict_sku_prices[division.stripe_sku]        
    return jsonify({'data':dict_div_to_sku})

