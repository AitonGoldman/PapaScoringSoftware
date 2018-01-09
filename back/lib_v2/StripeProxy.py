import stripe

class StripeProxy():
    def __init__(self,table_proxy):
        self.table_proxy=table_proxy
        
    def get_sku_price(self, sku, api_key):        
        if api_key is None:        
            raise Exception('Stripe API key is not set')
        stripe.api_key = api_key
        product_list = stripe.Product.list(limit=50)    
        items = product_list['data']
        dict_sku_prices = {}
        for item in items:
            for sku_dict in item['skus']['data']:            
                dict_sku_prices[sku_dict['id']]=sku_dict['price']/100                
        if sku in dict_sku_prices:
            return dict_sku_prices[sku]
        else:        
            raise Exception('invalid sku specified')    

    def set_tournament_stripe_prices(self, tournament, api_key, sku=None,discount_sku=None, commit=False):
        tournament.manually_set_price=None
        tournament.discount_price=None        
        if sku:
            tournament.stripe_sku=sku
            tournament.stripe_price=self.get_sku_price(sku,api_key)
        if discount_sku:
            tournament.discount_stripe_sku=discount_sku
            tournament.discount_stripe_price=self.get_sku_price(discount_sku,api_key)
        if commit:
            self.table_proxy.db_handle.session.commit()

    def purchase_tickets(self,stripe_items, api_key, stripe_token, email, token_purchase):
        try:
            stripe.api_key = api_key
            order = stripe.Order.create(
                currency="usd",
                email=email,
                items=stripe_items
            )

            #FIXME : this is for testing only
            # stripe_token = stripe.Token.create(
            #     card={
            #         "number": '4242424242424242',
            #         "exp_month": 12,
            #         "exp_year": 2018,
            #         "cvc": '123'
            #     },
            # ).id

            #input_data['stripe_token']=stripe_token
            
            order_response=order.pay(
                source=stripe_token
            )
            order_id_string =  "order_id %s " % order_response.id
            for token in token_purchase.tokens:
                token.paid_for=True
            token_purchase.completed_purchase=True
            return {'order_id_string':order_id_string}        
        except stripe.error.RateLimitError as e:
            return {'error_text':'The credit card processing service is busy.  Please try again in a few minutes','exception':e}
        except stripe.error.CardError as e:
            return {'error_text':'The credit card processing service has rejected your card.  Please see the front desk for more details','exception':e}
        except Exception as e:
            print e
            return {'error_text':'I have no fucking idea what the fuck just happened','exception':e}
            
