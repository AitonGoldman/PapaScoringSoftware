from util import db_util
from routes.utils import check_roles_exist,fetch_entity
from enum import Enum
import stripe

class RolesEnum(Enum):
    admin = 1
    desk = 2
    scorekeeper = 3
    void = 4
    player = 5
    token = 6

def set_stripe_api_key(stripe_api_key):
    stripe.api_key=stripe_api_key

def fetch_stripe_price(app,division):
    db = db_util.app_db_handle(app)
    product_list = stripe.Product.list()
    items = product_list['data']            
    dict_sku_prices = {}
    for item in items:        
        dict_sku_prices[item['skus']['data'][0]['id']]=item['skus']['data'][0]['price']/100    
    division.local_price = dict_sku_prices[division.stripe_sku]
    db.session.commit()        

def create_stanard_roles_and_users(app):
    create_roles(app)
    test_admin = create_user(app,'test_admin', 'test_admin',
                             [str(RolesEnum.admin.value),str(RolesEnum.desk.value),
                              str(RolesEnum.scorekeeper.value),str(RolesEnum.void.value),
                              str(RolesEnum.token.value)])
    test_scorekeeper = create_user(app,'test_scorekeeper', 'test_scorekeeper',
                                   [str(RolesEnum.scorekeeper.value),str(RolesEnum.void.value)])            
    
    test_desk = create_user(app,'test_desk', 'test_desk',
                            [str(RolesEnum.desk.value),str(RolesEnum.void.value),str(RolesEnum.token.value)])            
    return test_admin,test_scorekeeper,test_desk


def init_papa_tournaments_divisions(app,use_stripe=False,stripe_sku=None):
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
        new_tournament_data['stripe_sku']=stripe_sku
    else:
        new_tournament_data['use_stripe']=False
        new_tournament_data['local_price']=5
    for division_name in ['A','B','C','D']:
        new_tournament_data['division_name']=division_name
        new_division = create_division(app,new_tournament_data)            
        db.session.commit()
        new_tournament.divisions.append(new_division)
        db.session.commit()
    new_metadivision = create_meta_division(app,{
        'meta_division_name':'Classics'
    })
    new_team_tournament_data={'tournament_name':'Split Flipper',
                                                         'single_division':True,
                                                         'active':True,
                                                         'team_tournament':True,
                                                         'scoring_type':'HERB',
                                                         'number_of_scores_per_entry':'1',
                                                         'finals_num_qualifiers':'24'}
    if use_stripe:
        new_team_tournament_data['use_stripe']=True
        new_team_tournament_data['stripe_sku']=stripe_sku
    else:
        new_team_tournament_data['use_stripe']=False
        new_team_tournament_data['local_price']=5
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
        new_classics_tournament_data['stripe_sku']=stripe_sku
    else:
        new_classics_tournament_data['use_stripe']=False        
        new_classics_tournament_data['local_price']=5
    for tournament_name in ['Classics 1','Classics 2','Classics 3']:
        new_classics_tournament_data['tournament_name']=tournament_name
        new_tournament = create_tournament(app,new_classics_tournament_data)
        new_metadivision.divisions.append(new_division)
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

    new_player = tables.Player(
        first_name=player_data['first_name'],
        last_name=player_data['last_name'],
        asshole_count=0,
        active=True        
    )
    db.session.add(new_player)
    db.session.commit()                        
    new_player.roles.append(player_role)
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
    tables.db_handle.session.add(new_meta_division)
    tables.db_handle.session.commit()
    return new_meta_division

def create_division(app,division_data):
    db = db_util.app_db_handle(app)
    tables = db_util.app_db_tables(app)

    new_division = tables.Division(            
        division_name = division_data["division_name"],
        finals_num_qualifiers = division_data['finals_num_qualifiers'],
        tournament_id=division_data["tournament_id"]
    )        
    if division_data['scoring_type'] == "HERB":
        new_division.number_of_scores_per_entry=1
    if 'use_stripe' in division_data and division_data['use_stripe']:
        new_division.use_stripe = True
        new_division.stripe_sku=division_data['stripe_sku']
    else:
        new_division.use_stripe = False
    if 'local_price' in division_data and division_data['use_stripe'] == False: 
        new_division.local_price=division_data['local_price']
    if 'team_tournament' in division_data and division_data['team_tournament']:    
        new_division.team_tournament = True
    else:
        new_division.team_tournament = False    
    new_division.scoring_type=division_data['scoring_type']            
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
    
def create_roles(app,custom_roles=[]):
    roles = []
    for role_enum in list(RolesEnum):
        roles.append(role_enum.name)
    db_handle = app.tables.db_handle
    if len(custom_roles)>0:
        roles = custom_roles
    for role in roles:
        db_handle.session.add(app.tables.Role(name=role))
        db_handle.session.commit()

def create_user(app,username,password,roles=[]):
    db = db_util.app_db_handle(app)
    tables = db_util.app_db_tables(app)
    new_user = tables.User(
        username=username
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
    
        
