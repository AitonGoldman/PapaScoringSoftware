from util import db_util
from routes.utils import check_roles_exist,fetch_entity

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
    if 'local_price' in division_data and division_data['use_stripe'] == False: 
        new_division.local_price=division_data['local_price']
    if 'team_tournament' in division_data and division_data['team_tournament']:    
        new_division.team_tournament = True
    else:
        new_division.team_tournament = False    
    new_division.scoring_type=division_data['scoring_type']            
    db.session.add(new_division)
    db.session.commit()
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
    return new_tournament
    
def create_roles(app,custom_roles=[]):
    roles = ['admin','desk','scorekeeper','void','player','token']                    
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
    
        
