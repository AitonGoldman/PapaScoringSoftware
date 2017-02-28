from blueprints import admin_login_blueprint,admin_manage_blueprint
from flask import jsonify,current_app,request
import json
from werkzeug.exceptions import BadRequest,Conflict
from util import db_util
from util.permissions import Admin_permission,Scorekeeper_permission,Token_permission
from flask_login import login_required,current_user
from routes.utils import fetch_entity,calc_audit_log_remaining_tokens
import stripe
import datetime
from routes.audit_log_utils import create_audit_log
from orm_creation import create_ticket_purchase, create_purchase_summary
import os
import sendgrid
from sendgrid.helpers.mail import *
import time

@admin_manage_blueprint.route('/stripe/public_key', methods=['GET'])
def get_public_key():
    return jsonify({'data':current_app.td_config['STRIPE_PUBLIC_KEY']})

@admin_manage_blueprint.route('/stripe/sku/<sku>', methods=['GET'])
def get_valid_sku(sku):
    if 'STRIPE_API_KEY' not in current_app.td_config or current_app.td_config['STRIPE_API_KEY'] is None:
        raise BadRequest('Stripe API key is not set')
    stripe.api_key = current_app.td_config['STRIPE_API_KEY']
    product_list = stripe.Product.list()
    items = product_list['data']
    dict_sku_prices = {}
    for item in items:        
        dict_sku_prices[item['skus']['data'][0]['id']]=item['skus']['data'][0]['price']/100    
    if sku in dict_sku_prices:
        return jsonify({'sku':to_dict(item['skus']['data'][0])})
    else:
        return jsonify({'sku':None})

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

def confirm_tokens(tokens):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    #tokens_data = json.loads(request.data)['total_tokens']
    #for token in tokens_data:
    for token in tokens:
        token = fetch_entity(tables.Token,token['token_id'])
        if token:
            token.paid_for=True
            tables.db_handle.session.commit()
            audit_log = tables.AuditLog()
            audit_log.purchase_date = datetime.datetime.now()            
            if token.player_id:
                audit_log.player_id = token.player_id
            if token.team_id:
                audit_log.team_id = token.team_id
            
            audit_log.token_id=new_token.token_id
            audit_log.deskworker_id=current_user.user_id
        
            tokens_left_string = calc_audit_log_remaining_tokens(player_id,team_id)
            audit_log.remaining_tokens = tokens_left_string        
            db.session.add(audit_log)            
            tables.db_handle.session.commit()
        #DB.session.add(new_audit_log_entry)
        #tables.db_handle.session.commit()        
        db.session.commit()
    
    return jsonify({'data':token.to_dict_simple()})

def build_stripe_purchases(ticket_count,stripe_items,division_skus,discount_division_skus,division_id=None,metadivision_id=None):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)

    if division_id:
        division = tables.Division.query.filter_by(division_id=division_id).first()
        sku_division_id=division.division_id
    if metadivision_id:
        division = tables.MetaDivision.query.filter_by(meta_division_id=metadivision_id).first()
        sku_division_id=division.meta_division_id
        
    discount_for = division.discount_ticket_count
    discount_price = division.discount_ticket_price    
    if discount_for is None or discount_price is None:
        if division_id:
            stripe_items.append({"quantity":ticket_count,"type":"sku","parent":division_skus[sku_division_id]})            
        return            
    if  discount_for and ticket_count >= discount_for:
        discount_count = ticket_count/discount_for
        normal_count = ticket_count%discount_for
    else:
        discount_count = 0
        normal_count = ticket_count
    if discount_count > 0:
        stripe_items.append({"quantity":discount_count,"type":"sku","parent":discount_division_skus[sku_division_id]})
    if normal_count > 0:
        stripe_items.append({"quantity":normal_count,"type":"sku","parent":division_skus[sku_division_id]})



@admin_manage_blueprint.route('/stripe_registration', methods=['POST'])
def start_pre_reg_sale():
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    stripe_token = json.loads(request.data)['stripe_token']
    player_id = json.loads(request.data)['player_id']
    email = json.loads(request.data)['player_email']
    cc_email = json.loads(request.data)['player_cc_email']    
    stripe.api_key = current_app.td_config['STRIPE_API_KEY']
    registration_sku = os.getenv('REGISTRATION_FEE_SKU',None)
    stripe_items = [{"quantity":1,"type":"sku","parent":registration_sku}]
    player = fetch_entity(tables.Player,player_id)
    try:
        order = stripe.Order.create(
            currency="usd",
            email=cc_email,
            items=stripe_items
        )
        order_response=order.pay(
            source=stripe_token 
        )
        order_id_string =  "order_id %s, " % order_response.id
        
        
        create_audit_log("Player Ticket Registration Completed",datetime.datetime.now(),
                         order_id_string,None,
                         player_id=int(player_id))
        player.pre_reg_paid = True
        db.session.commit()
        player_dict = player.to_dict_simple()
        player_dict['pin']=player.pin        
        sg = sendgrid.SendGridAPIClient(apikey=current_app.td_config['SENDGRID_API_KEY'])
        from_email = Email("prereg@papa.org")
        subject = "You have been pre-registered for PAPA 20!"
        to_email = Email(email)
        content = Content("text/plain",
                          "Your player number is : %s\n\nYour player PIN is : %s\n\n\n\nBelow is information you will need to complete the registration process.\n\n\n\nThe PAPA 20 World Championship starts on April 6th, but the PAPA facility will be open to the public on April 5th during the PAPA Circuit Final.  Starting on April 5th at 1pm you will be able to complete the registration process.  You will need to go to the front desk and fill out your legal waiver and pick up your PAPA 20 t-shirt.\n\n\n\nYou will be unable to play any games until you sign the waiver.\n\n\n\nIf you have any questions, please email sales@papa.org\n\n\n\nWe look forward to seeing you at PAPA 20!" % (player.player_id,player.pin)))
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        return jsonify({'data':player_dict})
        
    except stripe.error.CardError as e:
        # The card has been declined        
        return jsonify({"data":"FAILURE"})            
    

def do_stripe_sale(stripe_token):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    #stripe_token = json.loads(request.data)['stripeToken']
    added_token_count = json.loads(request.data)['addedTokens']
    tokens = json.loads(request.data)['tokens']
    email = json.loads(request.data)['email']    
    #stripe.api_key = current_app.td_config['STRIPE_API_KEY']
    division_skus={}
    discount_division_skus={}
    metadivision_skus={}
    discount_metadivision_skus={}
    
    for division in tables.Division.query.all():        
        division_skus[division.division_id]=division.stripe_sku
        discount_division_skus[division.division_id]=division.discount_stripe_sku

    #FIXME : need to associate a cost with metadiv directly
    for metadivision in tables.MetaDivision.query.all():
        metadivision_skus[metadivision.meta_division_id]=metadivision.stripe_sku
        discount_metadivision_skus[metadivision.meta_division_id]=metadivision.discount_stripe_sku
        
    stripe_items=[]
    for division_id,num_tokens in added_token_count['divisions'].iteritems():        
        if int(num_tokens[0]) > 0:
            ticket_count = int(num_tokens[0])
            build_stripe_purchases(ticket_count,stripe_items,division_skus,discount_division_skus,int(division_id))            
                         
    for metadivision_id,num_tokens in added_token_count['metadivisions'].iteritems():        
        if int(num_tokens[0]) > 0:            
            ticket_count = int(num_tokens[0])            
            build_stripe_purchases(ticket_count,stripe_items,metadivision_skus,discount_metadivision_skus,metadivision_id=int(metadivision_id))            
            
    for division_id,num_tokens in added_token_count['teams'].iteritems():        
        if int(num_tokens[0]) > 0:            
            ticket_count = int(num_tokens[0])
            build_stripe_purchases(ticket_count,stripe_items,division_skus,discount_division_skus,int(division_id))            
    try:
        order = stripe.Order.create(
            currency="usd",
            email=email,
            items=stripe_items
        )
        order_response=order.pay(
            source=stripe_token 
        )
        order_id_string =  "order_id %s, " % order_response.id
        stripe_purchase_summary_string = order_id_string
        purchase_summary = create_purchase_summary(current_app,
                                                   current_user.player.player_id,
                                                   use_stripe=True,
                                                   stripe_charge_id=order_response.charge)
        for division_id,num_tokens in added_token_count['divisions'].iteritems():        
            if int(num_tokens[0]) > 0:
                create_ticket_purchase(current_app,
                                       num_tokens[0],
                                       current_user.player.player_id,
                                       current_user.user_id,
                                       purchase_summary.purchase_summary_id,                                       
                                       division_id=division_id)#,
                                       #use_stripe=True,
                                       #stripe_charge_id=order_response.charge)
        for metadivision_id,num_tokens in added_token_count['metadivisions'].iteritems():        
            if int(num_tokens[0]) > 0:            
                create_ticket_purchase(current_app,
                                       num_tokens[0],
                                       current_user.player.player_id,
                                       current_user.user_id,
                                       purchase_summary.purchase_summary_id,                                       
                                       metadivision_id=metadivision_id)#,
                                       #use_stripe=True,
                                       #stripe_charge_id=order_response.charge)
        for division_id,num_tokens in added_token_count['teams'].iteritems():        
            if int(num_tokens[0]) > 0:            
                create_ticket_purchase(current_app,
                                       num_tokens[0],
                                       current_user.player.player_id,
                                       current_user.user_id,
                                       purchase_summary.purchase_summary_id,                                       
                                       division_id=division_id)#,
                                       #use_stripe=True,
                                       #stripe_charge_id=order_response.charge)
        for json_token in tokens:            
            token = tables.Token.query.filter_by(token_id=json_token['token_id']).first()            
            token.paid_for=True
            db.session.commit()

        create_audit_log("Player Ticket Purchase Completed",datetime.datetime.now(),
                         stripe_purchase_summary_string,user_id=current_user.user_id,
                         player_id=current_user.player.player_id)    
        
        if len(current_user.player.teams) > 0:
            team_id = current_user.player.teams[0].team_id
        else:
            team_id = None
        tokens_left_string = calc_audit_log_remaining_tokens(current_user.player.player_id,team_id)        
        create_audit_log("Ticket Summary",datetime.datetime.now(),
                         tokens_left_string,
                         player_id=current_user.player.player_id)       
        return jsonify({"data":"success"})
    except stripe.error.CardError as e:
        # The card has been declined        
        return jsonify({"data":"FAILURE"})        

@admin_manage_blueprint.route('/stripe/test_player_purchase/<output_file_num>', methods=['POST'])
@login_required
@Token_permission.require(403)
def start_test_sale(output_file_num):
    stripe.api_key = current_app.td_config['STRIPE_API_KEY']
    stripe_tokens = []
    for i in range(int(output_file_num)):
        stripe_token = stripe.Token.create(
            card={
                "number": '4242424242424242',
                "exp_month": 12,
                "exp_year": 2018,
                "cvc": '123'
            },
        ).id
        f = open('/tmp/tokens_%s.json' % i,'w')
        f.write(json.dumps({'stripe_token':stripe_token}))
        f.close()
    return jsonify({})
    
@admin_manage_blueprint.route('/stripe', methods=['POST'])
@login_required
@Token_permission.require(403)
def start_sale():
    stripe_token = json.loads(request.data)['stripeToken']    
    stripe.api_key = current_app.td_config['STRIPE_API_KEY']
    return do_stripe_sale(stripe_token)
    
    # db = db_util.app_db_handle(current_app)
    # tables = db_util.app_db_tables(current_app)
    # stripe_token = json.loads(request.data)['stripeToken']
    # added_token_count = json.loads(request.data)['addedTokens']
    # tokens = json.loads(request.data)['tokens']
    # email = json.loads(request.data)['email']    
    # stripe.api_key = current_app.td_config['STRIPE_API_KEY']
    # division_skus={}
    # discount_division_skus={}
    # metadivision_skus={}
    # discount_metadivision_skus={}
    
    # for division in tables.Division.query.all():        
    #     division_skus[division.division_id]=division.stripe_sku
    #     discount_division_skus[division.division_id]=division.discount_stripe_sku

    # #FIXME : need to associate a cost with metadiv directly
    # for metadivision in tables.MetaDivision.query.all():
    #     metadivision_skus[metadivision.meta_division_id]=metadivision.stripe_sku
    #     discount_metadivision_skus[metadivision.meta_division_id]=metadivision.discount_stripe_sku
        
    # stripe_items=[]
    # for division_id,num_tokens in added_token_count['divisions'].iteritems():        
    #     if int(num_tokens[0]) > 0:
    #         ticket_count = int(num_tokens[0])
    #         build_stripe_purchases(ticket_count,stripe_items,division_skus,discount_division_skus,int(division_id))            
                         
    # for metadivision_id,num_tokens in added_token_count['metadivisions'].iteritems():        
    #     if int(num_tokens[0]) > 0:            
    #         ticket_count = int(num_tokens[0])            
    #         build_stripe_purchases(ticket_count,stripe_items,metadivision_skus,discount_metadivision_skus,metadivision_id=int(metadivision_id))            
            
    # for division_id,num_tokens in added_token_count['teams'].iteritems():        
    #     if int(num_tokens[0]) > 0:            
    #         ticket_count = int(num_tokens[0])
    #         build_stripe_purchases(ticket_count,stripe_items,division_skus,discount_division_skus,int(division_id))            
    # try:
    #     order = stripe.Order.create(
    #         currency="usd",
    #         email=email,
    #         items=stripe_items
    #     )
    #     order_response=order.pay(
    #         source=stripe_token 
    #     )
    #     order_id_string =  "order_id %s, " % order_response.id
    #     stripe_purchase_summary_string = order_id_string
    #     purchase_summary = create_purchase_summary(current_app,
    #                                                current_user.player.player_id,
    #                                                use_stripe=True,
    #                                                stripe_charge_id=order_response.charge)
    #     for division_id,num_tokens in added_token_count['divisions'].iteritems():        
    #         if int(num_tokens[0]) > 0:
    #             create_ticket_purchase(current_app,
    #                                    num_tokens[0],
    #                                    current_user.player.player_id,
    #                                    current_user.user_id,
    #                                    purchase_summary.purchase_summary_id,                                       
    #                                    division_id=division_id)#,
    #                                    #use_stripe=True,
    #                                    #stripe_charge_id=order_response.charge)
    #     for metadivision_id,num_tokens in added_token_count['metadivisions'].iteritems():        
    #         if int(num_tokens[0]) > 0:            
    #             create_ticket_purchase(current_app,
    #                                    num_tokens[0],
    #                                    current_user.player.player_id,
    #                                    current_user.user_id,
    #                                    purchase_summary.purchase_summary_id,                                       
    #                                    metadivision_id=metadivision_id)#,
    #                                    #use_stripe=True,
    #                                    #stripe_charge_id=order_response.charge)
    #     for division_id,num_tokens in added_token_count['teams'].iteritems():        
    #         if int(num_tokens[0]) > 0:            
    #             create_ticket_purchase(current_app,
    #                                    num_tokens[0],
    #                                    current_user.player.player_id,
    #                                    current_user.user_id,
    #                                    purchase_summary.purchase_summary_id,                                       
    #                                    division_id=division_id)#,
    #                                    #use_stripe=True,
    #                                    #stripe_charge_id=order_response.charge)
    #     for json_token in tokens:            
    #         token = tables.Token.query.filter_by(token_id=json_token['token_id']).first()            
    #         token.paid_for=True
    #         db.session.commit()

    #     create_audit_log("Player Ticket Purchase Completed",datetime.datetime.now(),
    #                      stripe_purchase_summary_string,user_id=current_user.user_id,
    #                      player_id=current_user.player.player_id)    
        
    #     if len(current_user.player.teams) > 0:
    #         team_id = current_user.player.teams[0].team_id
    #     else:
    #         team_id = None
    #     tokens_left_string = calc_audit_log_remaining_tokens(current_user.player.player_id,team_id)        
    #     create_audit_log("Ticket Summary",datetime.datetime.now(),
    #                      tokens_left_string,
    #                      player_id=current_user.player.player_id)       
    #     return jsonify({"data":"success"})
    # except stripe.error.CardError as e:
    #     # The card has been declined        
    #     return jsonify({"data":"FAILURE"})

