import stripe
from werkzeug.exceptions import BadRequest,Unauthorized,Conflict

def get_sku_price(sku,STRIPE_API_KEY):
    if 'STRIPE_API_KEY' is None:
        raise BadRequest('Stripe API key is not set')
    stripe.api_key = STRIPE_API_KEY    
    product_list = stripe.Product.list(limit=50)    
    items = product_list['data']
    dict_sku_prices = {}
    for item in items:
        for sku_dict in item['skus']['data']:            
            dict_sku_prices[sku_dict['id']]=sku_dict['price']/100                
    if sku in dict_sku_prices:
        return dict_sku_prices[sku]
    else:        
        return None
