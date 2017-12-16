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
            tournament.stripe_price=self.get_sku_price(sku,api_key)
        if discount_sku:
            tournament.discount_stripe_price=self.get_sku_price(discount_sku,api_key)
        if commit:
            self.table_proxy.session.commit()
