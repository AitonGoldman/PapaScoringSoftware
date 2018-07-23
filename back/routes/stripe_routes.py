from flask_restless.helpers import to_dict
from lib.flask_lib import blueprints
from flask import jsonify,current_app,request
from werkzeug.exceptions import BadRequest,Unauthorized,Conflict
from flask_login import login_user, logout_user, current_user
import json
from lib import orm_factories,token_helpers
from lib.serializer.generic import generate_generic_serializer
from lib import serializer
from lib.route_decorators.db_decorators import load_tables
from sqlalchemy.orm import joinedload
from lib.flask_lib.permissions import player_buy_tickets_permissions
import stripe
from lib.route_decorators.auth_decorators import check_current_user_is_active

@blueprints.event_blueprint.route('/stripe/token_purchase/<token_purchase_id>',methods=['POST'])
@player_buy_tickets_permissions.require(403)
@check_current_user_is_active
@load_tables
def player_purchase_tokens_with_stripe(tables,token_purchase_id):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('No info in request')        
    token_purchase = current_app.tables.TokenPurchases.query.filter_by(token_purchase_id=token_purchase_id).first()
    if token_purchase.completed_purchase:
        raise BadRequest('You are trying to pay for something that is already paid for')                
    tournaments_dict = {tournament.tournament_id:tournament for tournament in current_app.tables.Tournaments.query.all()}
    meta_tournaments_dict = {meta_tournament.meta_tournament_id:meta_tournament for meta_tournament in current_app.tables.MetaTournaments.query.all()}
    stripe_items=[]
    for token_purchase_summary in token_purchase.token_purchase_summaries:
        token_count=token_purchase_summary.token_count
        if token_purchase_summary.tournament_id:
            tournament=tournaments_dict[token_purchase_summary.tournament_id]
        else:
            tournament=meta_tournaments_dict[token_purchase_summary.meta_tournament_id]
        normal_and_discount_amounts = token_helpers.get_normal_and_discount_amounts(tournament,token_count)
        discount_sku = tournament.discount_stripe_sku
        normal_sku = tournament.stripe_sku
        discount_count = normal_and_discount_amounts[1]
        normal_count = normal_and_discount_amounts[0]                
        if discount_count > 0:
            stripe_items.append({"quantity":discount_count,"type":"sku","parent":discount_sku})
        if normal_count > 0:
            stripe_items.append({"quantity":normal_count,"type":"sku","parent":normal_sku})           
    try:
        stripe.api_key = current_app.event_config['stripe_api_key']    
        order = stripe.Order.create(
            currency="usd",
            email=input_data['email'],
            items=stripe_items
        )

        #FIXME : this is for testing only
        stripe_token = stripe.Token.create(
            card={
                "number": '4242424242424242',
                "exp_month": 12,
                "exp_year": 2018,
                "cvc": '123'
            },
        ).id

        input_data['stripe_token']=stripe_token
        
        order_response=order.pay(
           source=input_data['stripe_token']
        )
        order_id_string =  "order_id %s, " % order_response.id
        for token in token_purchase.tokens:
            token.paid_for=True
        token_purchase.completed_purchase=True
        current_app.tables.db_handle.session.commit()
        return jsonify({'order_id_string':order_id_string})        
    except stripe.error.RateLimitError as e:
        return jsonify({'error':'one'})
        pass
    except stripe.error.CardError as e:
        return jsonify({'error':'two'})
        pass
    except Exception as e:        
        print e
        return jsonify({'error':'three'})
        pass
    pass
