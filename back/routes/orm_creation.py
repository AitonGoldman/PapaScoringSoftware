from util import db_util
from routes.utils import check_roles_exist,fetch_entity,get_valid_sku
from enum import Enum
import stripe
import os
import random
import datetime
from werkzeug.exceptions import BadRequest,Conflict

class RolesEnum(Enum):
    admin = 1
    desk = 2
    scorekeeper = 3
    void = 4
    player = 5
    token = 6
    queue = 7
    test = 8
    
def set_stripe_api_key(stripe_api_key):
    stripe.api_key=stripe_api_key

def fetch_stripe_price(app,division):
    db = db_util.app_db_handle(app)
    product_list = stripe.Product.list(limit=25)
    items = product_list['data']            
    dict_sku_prices = {}
    for item in items:        
        for sku_dict in item['skus']['data']:
            dict_sku_prices[sku_dict['id']]=sku_dict['price']/100    
    division.local_price = dict_sku_prices[division.stripe_sku]
    if division.discount_stripe_sku:
        division.discount_ticket_price = dict_sku_prices[division.discount_stripe_sku]    
    db.session.commit()        

def create_stanard_roles_and_users(app):
    create_roles(app)
    test_admin = create_user(app,'test_admin', 'test_admin',
                             [str(RolesEnum.admin.value),str(RolesEnum.desk.value),
                              str(RolesEnum.scorekeeper.value),str(RolesEnum.void.value),
                              str(RolesEnum.token.value), str(RolesEnum.queue.value)])
    test_scorekeeper = create_user(app,'test_scorekeeper', 'test_scorekeeper',
                                   [str(RolesEnum.scorekeeper.value),str(RolesEnum.void.value),
                                   str(RolesEnum.queue.value)])            
    
    test_desk = create_user(app,'test_desk', 'test_desk',
                            [str(RolesEnum.desk.value),str(RolesEnum.void.value),str(RolesEnum.token.value),
                            str(RolesEnum.queue.value)])            
    return test_admin,test_scorekeeper,test_desk

def init_papa_players(app):
    from data_files import first_names,last_names    
    for player_num in range(100):
        name_index = random.randrange(0,len(first_names.first_names)-1)        
        create_player(app,{'first_name':'%s'%first_names.first_names[name_index],'last_name':'%s'%last_names.last_names[name_index],'ifpa_ranking':random.randrange(999),'linked_division_id':'1'})
    for player_num in range(100,200):
        create_player(app,{'first_name':'%s'%first_names.first_names[name_index],'last_name':'%s'%last_names.last_names[name_index],'ifpa_ranking':random.randrange(999),'linked_division_id':'2'})
    for player_num in range(200,300):
        create_player(app,{'first_name':'%s'%first_names.first_names[name_index],'last_name':'%s'%last_names.last_names[name_index],'ifpa_ranking':random.randrange(999),'linked_division_id':'3'})
    for player_num in range(300,400):
        create_player(app,{'first_name':'%s'%first_names.first_names[name_index],'last_name':'%s'%last_names.last_names[name_index],'ifpa_ranking':random.randrange(999),'linked_division_id':'4'})                                           
    for team_num in range(1,100,2):
        create_team(app,{'team_name':'test_team_%s'%team_num,'players':[team_num,team_num+1]})

    
def init_papa_tournaments_division_machines(app):
    db = app.tables.db_handle
    tables = app.tables
    machine_counter = 1
    for division_id in [1,2,3,4]:        
        division = tables.Division.query.filter_by(division_id=division_id).first()
        for machine_id in range(12):
            machine_id_to_lookup = machine_id+machine_counter            
            machine = tables.Machine.query.filter_by(machine_id=machine_id_to_lookup).first()
            create_division_machine(app,machine,division)
        machine_counter=machine_counter+12
        
    division = tables.Division.query.filter_by(division_id=5).first()
    for machine_id in range(12):
        machine_id_to_lookup = machine_id+machine_counter            
        machine = tables.Machine.query.filter_by(machine_id=machine_id_to_lookup).first()
        create_division_machine(app,machine,division)
    machine_counter=machine_counter+12
    for division_id in [6,7,8]:        
        division = tables.Division.query.filter_by(division_id=division_id).first()
        for machine_id in range(12):
            machine_id_to_lookup = machine_id+machine_counter            
            machine = tables.Machine.query.filter_by(machine_id=machine_id_to_lookup).first()
            create_division_machine(app,machine,division)
        machine_counter=machine_counter+12
        
        
def init_papa_tournaments_divisions(app,use_stripe=False,stripe_skus=None,discount_stripe_skus=None,discount_ticket_counts=None):
    db = app.tables.db_handle
    tables = app.tables
    new_tournament = create_tournament(app,{'tournament_name':'Main','single_division':False})
    new_tournament_data = {
        #'division_name':division_name,
        'finals_num_qualifiers':'24',
        'tournament_id':str(new_tournament.tournament_id),
        'team_tournament':False,
        'scoring_type':'HERB',
        'active':True
    }    
    if use_stripe:
        new_tournament_data['use_stripe']=True        
    else:
        new_tournament_data['use_stripe']=False
        new_tournament_data['local_price']=5
    for division_name in ['A','B','C','D']:        
        if use_stripe:
            new_tournament_data['stripe_sku']=stripe_skus[division_name]
        elif 'stripe_sku' in new_tournament_data:
            new_tournament_data.pop('stripe_sku')            
        if discount_stripe_skus and division_name in discount_stripe_skus:
            new_tournament_data['discount_stripe_sku']=discount_stripe_skus[division_name]
            new_tournament_data['discount_ticket_count']=discount_ticket_counts[division_name]
        elif 'discount_stripe_sku' in new_tournament_data:
            new_tournament_data.pop('discount_stripe_sku')
        new_tournament_data['division_name']=division_name        
        new_division = create_division(app,new_tournament_data)        
        db.session.commit()
        new_tournament.divisions.append(new_division)
        db.session.commit()        
    metadivision_data = {
        'meta_division_name':'Classics',
        'use_stripe':use_stripe        
    }
    if use_stripe:
        metadivision_data['stripe_sku'] = stripe_skus['Classics Meta']        
    if discount_stripe_skus and "Classics Meta" in discount_stripe_skus:
        metadivision_data['discount_stripe_sku'] = discount_stripe_skus['Classics Meta']
        metadivision_data['discount_ticket_count'] = discount_ticket_counts['Classics Meta']
    
    new_metadivision = create_meta_division(app,metadivision_data)
    new_team_tournament_data={'tournament_name':'Split Flipper',
                                                         'single_division':True,
                                                         'active':True,
                                                         'team_tournament':True,
                                                         'scoring_type':'HERB',
                                                         'number_of_scores_per_entry':'1',
                                                         'finals_num_qualifiers':'24'}
    if use_stripe:
        new_team_tournament_data['use_stripe']=True
        new_team_tournament_data['stripe_sku']=stripe_skus['Split Flipper']
    else:
        new_team_tournament_data['use_stripe']=False
        new_team_tournament_data['local_price']=5
    if discount_stripe_skus and "Split Flipper" in discount_stripe_skus:
        new_team_tournament_data['discount_stripe_sku']=discount_stripe_skus["Split Flipper"]
        new_team_tournament_data['discount_ticket_count']=discount_ticket_counts["Split Flipper"]
        
    new_tournament = create_tournament(app,new_team_tournament_data)    
    new_classics_tournament_data = {'single_division':True,
                                    'active':True,
                                    'team_tournament':False,
                                    'scoring_type':'HERB',
                                    'number_of_scores_per_entry':'1',
                                    'finals_num_qualifiers':'24'
    }
    if use_stripe:
        new_classics_tournament_data['use_stripe']=True        
    else:
        new_classics_tournament_data['use_stripe']=False        
        new_classics_tournament_data['local_price']=5
    
    for tournament_name in ['Classics 1','Classics 2','Classics 3']:        
        if use_stripe:
            new_classics_tournament_data['stripe_sku']=stripe_skus[tournament_name]
        new_classics_tournament_data['tournament_name']=tournament_name
        
        new_tournament = create_tournament(app,new_classics_tournament_data)
        new_metadivision.divisions.append(new_tournament.divisions[0])
        db.session.commit()        

def create_team(app,team_data):
    db = db_util.app_db_handle(app)
    tables = db_util.app_db_tables(app)
    team = app.tables.Team(
        team_name=team_data['team_name']
    )    
    db.session.add(team)
    db.session.commit()
    for player_id in team_data['players']:
        team.players.append(fetch_entity(tables.Player,player_id))            
    db.session.commit()
    return team

def create_player(app,player_data):
    db = db_util.app_db_handle(app)
    tables = db_util.app_db_tables(app)

    player_role = tables.Role.query.filter_by(name='player').first()
    queue_role = tables.Role.query.filter_by(name='queue').first()    
    token_role = tables.Role.query.filter_by(name='token').first()    

    new_player = tables.Player(
        first_name=player_data['first_name'],
        last_name=player_data['last_name'],
        asshole_count=0        
    )
    if 'active' in player_data and player_data['active'] is False:
        new_player.active=False
    else:
        new_player.active=True
    pin_range = set(range(1523, 9999))
    existing_player_pins = set([player.pin for player in tables.Player.query.all()])
    allowed_values = pin_range - existing_player_pins        
    random_value = random.choice(list(allowed_values))  
    new_player.pin = random_value
    if app.td_config['DB_TYPE']=='sqlite':        
        new_player.pin= random.randrange(1234,9999999)
        db.session.commit()        
    
    db.session.add(new_player)
    db.session.commit()
    new_user = tables.User(
        username="player%s" % (new_player.pin),
        pin=new_player.pin,
        is_player=True,
        roles=[player_role,queue_role,token_role]
    )
    db.session.add(new_user)
    db.session.commit()
    new_player.user_id=new_user.user_id    
    db.session.commit()    
    if 'ifpa_ranking' in player_data and player_data['ifpa_ranking'] != 0:
        new_player.ifpa_ranking = player_data['ifpa_ranking']
    if 'email_address' in player_data:
        new_player.email_address = player_data['email_address']
    if 'linked_division_id' in player_data and tables.Division.query.filter_by(division_id=player_data['linked_division_id']).first():
        new_player.linked_division_id = player_data['linked_division_id']
    if 'pic_file' in player_data:        
        os.system('mv %s/%s /var/www/html/pics/player_%s.jpg' % (app.config['UPLOAD_FOLDER'],player_data['pic_file'],new_player.player_id))        
    db.session.commit()
    
    return new_player

def create_meta_division(app,meta_division_data):
    db = db_util.app_db_handle(app)
    tables = db_util.app_db_tables(app)
    new_meta_division = tables.MetaDivision(
    )
    if 'meta_division_name' in meta_division_data:
        new_meta_division.meta_division_name=meta_division_data['meta_division_name']
    if 'divisions' in meta_division_data:
        for division in meta_division_data['divisions']:
            division_table = fetch_entity(tables.Division,int(division))
            new_meta_division.divisions.append(division_table)
    if 'use_stripe' in meta_division_data and meta_division_data['use_stripe']:
        new_meta_division.use_stripe = True
        if get_valid_sku(meta_division_data['stripe_sku'],app.td_config['STRIPE_API_KEY'])['sku'] is None:
            raise BadRequest('invalid SKU specified')
        new_meta_division.stripe_sku=meta_division_data['stripe_sku']
        if 'discount_stripe_sku' in meta_division_data and meta_division_data['discount_stripe_sku']:
            if get_valid_sku(meta_division_data['discount_stripe_sku'],app.td_config['STRIPE_API_KEY'])['sku'] is None:                
                raise BadRequest('invalid SKU specified')        
            new_meta_division.discount_stripe_sku=meta_division_data['discount_stripe_sku']
            new_meta_division.discount_ticket_count=meta_division_data['discount_ticket_count']
        
    else:
        new_meta_division.use_stripe = False
    if 'local_price' in meta_division_data and meta_division_data['use_stripe'] == False: 
        new_meta_division.local_price=meta_division_data['local_price']
            
    tables.db_handle.session.add(new_meta_division)
    tables.db_handle.session.commit()
    if new_meta_division.use_stripe:
        set_stripe_api_key(app.td_config['STRIPE_API_KEY'])
        fetch_stripe_price(app,new_meta_division)
    
    return new_meta_division

def create_division(app,division_data):
    db = db_util.app_db_handle(app)
    tables = db_util.app_db_tables(app)

    new_division = tables.Division(            
        division_name = division_data["division_name"],
        finals_num_qualifiers = division_data['finals_num_qualifiers'],
        tournament_id=division_data["tournament_id"]
    )
    if 'active' in division_data:
        new_division.active=division_data['active']
    if division_data['scoring_type'] == "HERB":
        new_division.number_of_scores_per_entry=1
    if 'use_stripe' in division_data and division_data['use_stripe']:
        new_division.use_stripe = True
        if get_valid_sku(division_data['stripe_sku'],app.td_config['STRIPE_API_KEY'])['sku'] is None:
            print "trying to get normal %s %s"%(division_data['division_name'], division_data['stripe_sku'])
            raise BadRequest('invalid SKU specified')
        new_division.stripe_sku=division_data['stripe_sku']        
        if 'discount_stripe_sku' in division_data and division_data['discount_stripe_sku']:
            if get_valid_sku(division_data['discount_stripe_sku'],app.td_config['STRIPE_API_KEY'])['sku'] is None:
                print "trying to get %s"%division_data['discount_stripe_sku']
                raise BadRequest('invalid SKU specified')        
            new_division.discount_stripe_sku=division_data['discount_stripe_sku']            
            new_division.discount_ticket_count=division_data['discount_ticket_count']
            
    else:
        new_division.use_stripe = False
    if 'local_price' in division_data and division_data['use_stripe'] == False: 
        new_division.local_price=division_data['local_price']
    if 'team_tournament' in division_data and division_data['team_tournament']:    
        new_division.team_tournament = True
    else:
        new_division.team_tournament = False    
    new_division.scoring_type=division_data['scoring_type']
    new_division.finals_player_selection_type = "papa"
    new_division.number_of_relevant_scores = 6
    db.session.add(new_division)
    db.session.commit()
    if new_division.use_stripe:
        set_stripe_api_key(app.td_config['STRIPE_API_KEY'])
        fetch_stripe_price(app,new_division)
    return new_division

def create_tournament(app,tournament_data):
    db = db_util.app_db_handle(app)
    tables = db_util.app_db_tables(app)

    new_tournament = tables.Tournament(
        tournament_name=tournament_data['tournament_name']                        
    )
    db.session.add(new_tournament)
    db.session.commit()
    if 'single_division' in tournament_data and tournament_data['single_division']:        
        new_tournament.single_division=True
        tournament_data['division_name']= new_tournament.tournament_name+"_single"
        tournament_data['tournament_id']= new_tournament.tournament_id
        create_division(app,tournament_data)    
    else:        
        new_tournament.single_division=False
    db.session.commit()
    return new_tournament

def create_base_ticket_purchase(app,player_id,division_id,metadivision_id,user_id,purchase_summary_id):
    db = db_util.app_db_handle(app)
    tables = db_util.app_db_tables(app)
    ticket_purchase = tables.TicketPurchase()
    ticket_purchase.player_id=player_id
    ticket_purchase.division_id=division_id
    ticket_purchase.meta_division_id=metadivision_id
    ticket_purchase.user_id=user_id
    ticket_purchase.purchase_date=datetime.datetime.now()
    ticket_purchase.purchase_summary_id=purchase_summary_id
    return ticket_purchase

def create_purchase_summary(app,
                            player_id,
                            use_stripe=False,
                            stripe_charge_id=None):
    db = db_util.app_db_handle(app)
    tables = db_util.app_db_tables(app)
    purchase_summary = tables.PurchaseSummary(player_id=player_id,
                                              purchase_date=datetime.datetime.now(),
                                              use_stripe=use_stripe,
                                              stripe_charge_id=stripe_charge_id)
    db.session.add(purchase_summary)
    db.session.commit()
    return purchase_summary

    
def create_ticket_purchase(app,
                           ticket_count,
                           player_id,
                           user_id,
                           purchase_summary_id,
                           division_id=None,
                           metadivision_id=None,
                           commit=True):    
    if ticket_count == 0:
        return
    db = db_util.app_db_handle(app)
    tables = db_util.app_db_tables(app)
    if division_id:
        division = tables.Division.query.filter_by(division_id=division_id).first()
    if metadivision_id:
        division = tables.MetaDivision.query.filter_by(meta_division_id=metadivision_id).first()
        
    discount_for = division.discount_ticket_count
    discount_price = division.discount_ticket_price
    if discount_for is None or discount_price is None:
        ticket_purchase = create_base_ticket_purchase(app,player_id,division_id,metadivision_id,user_id,purchase_summary_id)            
        ticket_purchase.amount=ticket_count
        ticket_purchase.description="1"
        db.session.add(ticket_purchase)
        db.session.commit()
        return
    if ticket_count >= discount_for:
        discount_count = ticket_count/discount_for
        normal_count = ticket_count%discount_for
    else:
        discount_count = 0
        normal_count = ticket_count
    if discount_count > 0:        
        ticket_purchase = create_base_ticket_purchase(app,player_id,division_id,metadivision_id,user_id,purchase_summary_id)    
        ticket_purchase.amount=discount_count
        ticket_purchase.description="%s"%discount_for
        db.session.add(ticket_purchase)        
    if normal_count > 0:        
        ticket_purchase = create_base_ticket_purchase(app,player_id,division_id,metadivision_id,user_id,purchase_summary_id)    
        ticket_purchase.amount=normal_count
        ticket_purchase.description="1"
        db.session.add(ticket_purchase)
    if commit:        
        db.session.commit()
    return {'discount_count':discount_count,'normal_count':normal_count}

def create_roles(app,custom_roles=[]):
    roles = []
    new_roles = []
    for role_enum in list(RolesEnum):
        roles.append(role_enum.name)
    db_handle = app.tables.db_handle
    if len(custom_roles)>0:
        roles = custom_roles
    for role in roles:
        new_role = app.tables.Role(name=role)
        db_handle.session.add(new_role)
        db_handle.session.commit()
        new_roles.append(new_role)
    return new_roles

def create_division_machine(app,machine,division):
    db = db_util.app_db_handle(app)
    tables = db_util.app_db_tables(app)
    new_division_machine = tables.DivisionMachine(
        machine_id=machine.machine_id,
        division_id=division.division_id,
        removed=False
    )    
    tables.db_handle.session.add(new_division_machine)
    tables.db_handle.session.commit()
    return new_division_machine

def create_user(app,username,password,roles=[]):
    db = db_util.app_db_handle(app)
    tables = db_util.app_db_tables(app)
    new_user = tables.User(
        username=username,
        is_player=False
    )
    
    new_user.crypt_password(password)
    db.session.add(new_user)

    if len(roles)>0:        
        check_roles_exist(app.tables, roles)
        for role_id in roles:
            existing_role = tables.Role.query.filter_by(role_id=role_id).first()            
            new_user.roles.append(existing_role)
    
    db.session.commit()                        
    return new_user
    
        
def create_queue(app,division_machine_id,player_id,bumped=None):
    db = db_util.app_db_handle(app)
    tables = db_util.app_db_tables(app)
    division_machine = tables.DivisionMachine.query.filter_by(division_machine_id=division_machine_id).first()
    #queue_node = division_machine.queue        
    new_queue = tables.Queue(
        division_machine_id=division_machine_id,
        player_id=player_id
    )
    db.session.add(new_queue)
    #db.session.commit()
    bump_num = int(app.td_config['QUEUE_BUMP_AMOUNT'])        
    if bumped and bump_num!=0:
        queue_count = 1
        queue=division_machine.queue
        while(len(queue.queue_child)>0) and queue_count < bump_num:
            queue_count = queue_count + 1            
            queue=queue.queue_child[0]
        new_queue.parent_id=queue.queue_id
        if(len(queue.queue_child)>0):
            queue.queue_child[0].parent_id=new_queue.queue_id        
        new_queue.bumped=True
        #db.session.commit()        
        return new_queue
    if division_machine.queue_id is None:
        division_machine.queue=new_queue
        #db.session.commit()        
        return new_queue
    queue_node = division_machine.queue        
    while queue_node and len(queue_node.queue_child) > 0:        
        queue_node = queue_node.queue_child[0]
    if queue_node:
        queue_node.queue_child.append(new_queue)
    #db.session.commit()    
    return new_queue
        
#def create_entry(app,player_id,division_machine_id,division_id,score):
def create_entry(app,division_machine_id,division_id,score,player_id=None,team_id=None):
    db = db_util.app_db_handle(app)
    tables = db_util.app_db_tables(app)
    entry = tables.Entry(        
        division_id=division_id
    )
    if player_id:
        existing_score = tables.Score.query.filter_by(division_machine_id=division_machine_id,score=score).join(tables.Entry).filter_by(player_id=player_id).first()
        if existing_score:
            return existing_score.entry
        entry.player_id=player_id
    if team_id:
        existing_score = tables.Score.query.filter_by(division_machine_id=division_machine_id,score=score).join(tables.Entry).filter_by(team_id=team_id).first()
        if existing_score:
            return existing_score.entry

        entry.team_id=team_id
    
    db.session.add(entry)
    ##db.session.commit()
    score = tables.Score(
        score=score,
        ##entry_id=entry.entry_id,
        division_machine_id=division_machine_id
    )
    db.session.add(score)
    entry.scores.append(score)
    db.session.commit()    
    return entry
