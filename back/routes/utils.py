from werkzeug.exceptions import BadRequest,Conflict
from util import db_util
import datetime
from flask import current_app,jsonify
from flask_login import current_user
import stripe
from flask_restless.helpers import to_dict
import requests
import json
from audit_log_utils import create_audit_log

def get_discount_normal_ticket_counts(max_count,discount_count,discount_cost,increment,normal_cost):
    cur_count = 0
    cur_value = 0    
    available_ticket_list = [[0,0]]
    discount_counts = {}
    normal_counts = {}
    if discount_count is None:
        discount_count = 1
    if discount_cost is None:
        discount_cost=0
        
    while(cur_count < max_count):    
        cur_count = cur_count+1        
        is_discount_count = True if cur_count%discount_count == 0 and discount_count != 1 else False
        multiplier = cur_count/discount_count
        if is_discount_count and cur_count != 1:                        
            ticket_cost = multiplier*discount_cost
            available_ticket_list.append([cur_count,ticket_cost])
            discount_counts[cur_count]=multiplier
            normal_counts[cur_count]=0            
            continue
        discounts_contained_in_cur_count = cur_count/discount_count
        keep_looping=True
        if discounts_contained_in_cur_count > 0:
            while keep_looping is True and discounts_contained_in_cur_count > 0:                
                discount_amount_contained_in_cur_count=discounts_contained_in_cur_count*discount_count
                remainder_to_check = cur_count-discount_amount_contained_in_cur_count
                normal_increment_remainder=remainder_to_check%increment
                if normal_increment_remainder==0 and remainder_to_check >= increment:
                    ticket_cost = discounts_contained_in_cur_count*discount_cost                    
                    ticket_cost = ticket_cost + ((remainder_to_check/increment)*normal_cost)
                    
                    available_ticket_list.append([cur_count,ticket_cost])
                    discount_counts[cur_count]=discounts_contained_in_cur_count
                    normal_counts[cur_count]=remainder_to_check/increment                                
                    keep_looping=False
                else:
                    discounts_contained_in_cur_count=discounts_contained_in_cur_count-1
            if discounts_contained_in_cur_count > 0:
                continue
        is_normal_count = True if cur_count%increment == 0 else False
        if is_normal_count:
            normal_amount = cur_count/increment
            available_ticket_list.append([cur_count,normal_amount*normal_cost])
            discount_counts[cur_count]=0
            normal_counts[cur_count]=cur_count/increment                        
            continue
    list_len = len(available_ticket_list)
    filtered_ticket_list = []
    for idx,ticket_info in enumerate(available_ticket_list):
        if idx<list_len-1 and available_ticket_list[idx+1][1] == available_ticket_list[idx][1]:
            continue
        filtered_ticket_list.append(ticket_info)
    return [filtered_ticket_list,normal_counts,discount_counts]
    #return available_ticket_list

def check_player_is_on_device(player_id):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)    
    player = fetch_entity(tables.Player,player_id)
    if player and player.user.ioniccloud_push_token:
        return True
    return False

def check_player_in_queue(player_id,division_machine):
    queue_for_machine = get_queue_from_division_machine(division_machine,True)    
    queue_item_for_player=None
    for thing in queue_for_machine:
        print thing['player_id']
        if int(thing['player_id']) == int(player_id):
            queue_item_for_player = thing
    return queue_item_for_player

def get_player_list_to_notify(player_id,division_machine):    
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    queue = tables.Queue.query.filter_by(player_id=player_id).first()
    players_to_alert = []
    while queue:
        if len(queue.queue_child) > 0:
            queue = queue.queue_child[0]
            players_to_alert.append(queue.to_dict_simple())
        else:
            queue = None
    players_to_alert_filtered = [player_to_alert for player_to_alert in players_to_alert if check_player_is_on_device(player_to_alert['player_id'])]            
    #queue_for_machine = get_queue_from_division_machine(division_machine,True)    
    #for thing in queue_for_machine:
    #    pass    
    #queue_item_for_player=None
    #try:
    #queue_item_for_player = next(queue_dict for queue_dict in queue_for_machine if int(queue_dict['player_id']) == int(player_id))
    #for thing in queue_for_machine:
    #    if int(thing['player_id']) == int(player_id):
    #        queue_item_for_player = thing
    #except Exception as e:
    #    print "uh oh------"
    # we are interested in the queue_item_index after the current head of the queue, so
    # we don't change the position we get back into an index (i.e. subtract one)    
    #if queue_item_for_player:
    #    queue_item_index = int(queue_item_for_player['queue_position'])
    #    players_to_alert = queue_for_machine[queue_item_index:]    
    #    players_to_alert_filtered = [player_to_alert for player_to_alert in players_to_alert if check_player_is_on_device(player_to_alert['player_id'])]
    #else:
    #    raise Conflict("The server encountered a problem - try again.")
    #    #print "oh shit..."
    #    #players_to_alert_filtered=[]
    return players_to_alert_filtered

def record_ioniccloud_push_token(token,user_id=None,player_id=None):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)    
    if user_id:
        user = fetch_entity(tables.User,user_id)
    if player_id:
        player = fetch_entity(tables.Player,player_id)
        user=player.user
    user.ioniccloud_push_token=token
    db.session.commit()
    
def send_push_notification(message,user_id=None,player_id=None,postpone=None,players=None,title="YAPSS NOTIFICATION"):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)    

    if user_id:
        user = fetch_entity(tables.User,user_id)
        token = user.ioniccloud_push_token
        token_list = [token]        
    if player_id:
        player = fetch_entity(tables.Player,player_id)
        user=player.user
        token = user.ioniccloud_push_token
        token_list = [token]
    if players:
        token_list = []
        for player_queue_item in players:
            player = fetch_entity(tables.Player,player_queue_item['player_id'])
            user=player.user
            token = user.ioniccloud_push_token
            token_list.append(token)
            
    
    url = "https://api.ionic.io/push/notifications"
    api_key = current_app.td_config['IONICCLOUD_API_KEY']
    
    payload = {
        "tokens":token_list,
        "profile":current_app.td_config['IONICCLOUD_PROFILE_TAG'],
        "notification":{
            "ios":{
                "message":message,
                "sound":"default",
                "priority":10
            },
            "android":{
                "message":message,
                "sound":"default"
            }
            #"message":message
        }
    }
    if postpone:
        now = datetime.datetime.now()
        now_plus = now + datetime.timedelta(seconds = postpone)
        now_plus_adjusted = now_plus + datetime.timedelta(hours = 5)
        #2017-01-07T14:15:00Z
        scheduled_time_string = now_plus_adjusted.strftime("%Y-%m-%dT%H:%M:%SZ")
        payload['scheduled']=scheduled_time_string
    headers = {
        'Authorization': "Bearer %s" % api_key,
        'Content-Type': "application/json"
    }

    response = requests.post(url, data=json.dumps(payload), headers=headers)    

def get_valid_sku(sku,STRIPE_API_KEY):
    if 'STRIPE_API_KEY' is None:
        raise BadRequest('Stripe API key is not set')
    stripe.api_key = STRIPE_API_KEY
    product_list = stripe.Product.list(limit=25)    
    items = product_list['data']
    dict_sku_prices = {}
    for item in items:
        for sku_dict in item['skus']['data']:            
            dict_sku_prices[sku_dict['id']]=sku_dict['price']/100                
    if sku in dict_sku_prices:        
        return {'sku':sku}
    else:        
        return {'sku':None}

def get_valid_skus(STRIPE_API_KEY):
    if 'STRIPE_API_KEY' is None:
        raise BadRequest('Stripe API key is not set')
    stripe.api_key = STRIPE_API_KEY
    product_list = stripe.Product.list(limit=25)    
    items = product_list['data']
    dict_sku_prices = {}
    for item in items:
        print item['skus']['data'][0]['id']
        dict_sku_prices[item['skus']['data'][0]['id']]=item['skus']['data'][0]['price']/100                
    return dict_sku_prices

def fetch_entity(model_class,model_id):
    found_entity = model_class.query.get(model_id)    
    if found_entity is None:        
        error_arg_list = (model_id, model_class.__name__, model_class.__name__, model_id)
        raise BadRequest("Expecting url param %s with valid %s id but could not find valid %s with id %s" % error_arg_list)
    return found_entity

def check_roles_exist(tables, roles):
    for role_id in roles:
        existing_role = tables.Role.query.filter_by(role_id=role_id).first()
        if existing_role is None:            
            raise BadRequest('Role with id %s does not exist' % role_id)

def check_player_team_can_start_game(app,division_machine,player=None,team=None):
    db = db_util.app_db_handle(app)
    tables = db_util.app_db_tables(app)    
    if player:
        if tables.DivisionMachine.query.filter_by(player_id=player.player_id).first():            
            return False        
        if division_machine.division.meta_division_id:
            tokens = tables.Token.query.filter_by(player_id=player.player_id,
                                                  metadivision_id=division_machine.division.meta_division_id,
                                                  used=False,paid_for=True).all()
        else:
            tokens = tables.Token.query.filter_by(player_id=player.player_id,
                                                  division_id=division_machine.division.division_id,
                                                  used=False,paid_for=True).all()
    if team:
        if division_machine.division.meta_division_id:
            tokens = tables.Token.query.filter_by(team_id=team.team_id,
                                                  metadivision_id=division_machine.division.meta_division_id,
                                                  used=False,paid_for=True).all()
        else:
            tokens = tables.Token.query.filter_by(team_id=team.team_id,
                                                  division_id=division_machine.division.division_id,
                                                  used=False,paid_for=True).all()
        if tables.DivisionMachine.query.filter_by(team_id=team.team_id).first():            
            return False
    
    if len(tokens) == 0:        
        return False
    
    # check that player is not on a queue for a different machine (note : this is a special case - we just yank them off the queue)
    return True
    

def set_token_start_time(app,player,division_machine,team_id=None,commit=True):
    db = db_util.app_db_handle(app)
    tables = db_util.app_db_tables(app)        
    if division_machine.division.meta_division_id is None:
        if player:
            token_to_set = tables.Token.query.filter_by(player_id=player.player_id,
                                                        division_id=division_machine.division.division_id,
                                                        paid_for=True,used=False).first()
        if team_id:
            token_to_set = tables.Token.query.filter_by(team_id=team_id,
                                                        division_id=division_machine.division.division_id,
                                                        paid_for=True,used=False).first()
            
            
    else:
        if player:
            token_to_set = tables.Token.query.filter_by(player_id=player.player_id,
                                                        metadivision_id=division_machine.division.meta_division_id,
                                                        paid_for=True,used=False).first()
            
    token_to_set.game_started_date=datetime.datetime.now()
    token_to_set.division_machine_id = division_machine.division_machine_id
    if commit:
        db.session.commit()
    if player:
        player_id=player.player_id
    else:
        player_id=None        
    
    create_audit_log("Game Started",datetime.datetime.now(),
                     "",user_id=current_user.user_id,
                     player_id=player_id,team_id=team_id,
                     division_machine_id=division_machine.division_machine_id,
                     token_id=token_to_set.token_id,
                     commit=commit)        
    #if player:
    #    tokens_left_string = calc_audit_log_remaining_tokens(player.player_id)
    #else:
    #    tokens_left_string = calc_audit_log_remaining_tokens(None,team_id)

    #create_audit_log("Ticket Summary",datetime.datetime.now(),
    #                 tokens_left_string,user_id=current_user.user_id,
    #                 player_id=player_id,team_id=team_id)
        

def remove_player_from_queue(app,player=None,division_machine=None,commit=True):
    db = db_util.app_db_handle(app)
    tables = db_util.app_db_tables(app)
    if player:
        queue = tables.Queue.query.filter_by(player_id=player.player_id).first()
        if queue is None:            
            return None
    if division_machine:        
        queue = division_machine.queue
    if queue is None:        
        return False
    division_machine = queue.division_machine
    
    if len(queue.queue_child) > 0:        
        if queue.parent_id is None:            
            division_machine.queue.append(queue.queue_child[0])            
        else:            
            parent_queue = tables.Queue.query.filter_by(queue_id=queue.parent_id).first()
            parent_queue.queue_child.append(queue.queue_child[0])            
            #queue.queue_child[0].parent_id=queue.parent_id            
    else:        
        if queue.parent_id is None:            
            print "removing division machine queue id"
            #division_machine.queue_id=None
            #queue.division_machine = None
            division_machine.queue.remove(queue)
            #tables.DivisionMachine.query.filter_by(division_machine_id=division_machine.division_machine_id).first().queue_id=None
            #tables.DivisionMachine.query.filter_by(division_machine_id=division_machine.division_machine_id).first().queue=None
            
    #db.session.commit()
    db.session.delete(queue)    
    if commit:
        db.session.commit()    
    return queue

def get_queue_from_division_machine(division_machine,json_output=False):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)    
 
    if division_machine.queue is None:
        return []
    queue_list = []
    queue = tables.Queue.query.filter_by(division_machine_id=division_machine.division_machine_id,parent_id=None).first()
    #queue = division_machine.queue[0]    
    while queue is not None:
        if json_output:
            queue_list.append(queue.to_dict_simple())            
        else:                
            queue_list.append(queue)
        if len(queue.queue_child) > 0:
            queue = queue.queue_child[0]
        else:
            queue = None
    return queue_list


def calc_audit_log_remaining_tokens(player_id,team_id=None,return_string=True):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    divisions = {division.division_id:division.to_dict_simple() for division in tables.Division.query.all()}
    metadivisions = {meta_division.meta_division_id:meta_division.to_dict_simple() for meta_division in tables.MetaDivision.query.all()}
    division_tokens_left={}
    metadivision_tokens_left={}
    player_teams = []
    tokens_left = []    
    if player_id:
        tokens_left = tables.Token.query.filter_by(player_id=player_id,used=False,paid_for=True).all()
        player_teams = tables.Player.query.filter_by(player_id=player_id).first().teams
    if len(player_teams) > 0:
        team_id = player_teams[0].team_id
    if team_id:
        tokens_left = tokens_left + tables.Token.query.filter_by(team_id=team_id,used=False,paid_for=True).all()
    
    for token in tokens_left:
        if token.metadivision_id:
            if token.metadivision_id not in metadivision_tokens_left:
                metadivision_tokens_left[token.metadivision_id]=1
            else:
                metadivision_tokens_left[token.metadivision_id]=metadivision_tokens_left[token.metadivision_id]+1
        else:
            if token.division_id not in division_tokens_left:
                division_tokens_left[token.division_id]=1
            else:
                division_tokens_left[token.division_id]=division_tokens_left[token.division_id]+1
    tokens_left_string = ", ".join(["%s : %s" % (divisions[division_id]['tournament_name'],division_token_count) for division_id,division_token_count in division_tokens_left.iteritems()] +     ["%s : %s" % (metadivisions[metadivision_id]['meta_division_name'],metadivision_token_count) for metadivision_id,metadivision_token_count in metadivision_tokens_left.iteritems()])
    if tokens_left_string == "":
        tokens_left_string="No Tickets Left"
    if return_string:
        return tokens_left_string
    else:
        return {
            "tokens_left_string":tokens_left_string,
            "division_tokens_left":division_tokens_left,
            "metadivision_tokens_left":metadivision_tokens_left
        }
