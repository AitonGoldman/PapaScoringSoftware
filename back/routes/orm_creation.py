from util import db_util
from routes.utils import check_roles_exist

def create_tournament(app,tournament_data):
    db = db_util.app_db_handle(app)
    tables = db_util.app_db_tables(app)

    new_tournament = tables.Tournament(
        tournament_name=tournament_data['tournament_name']                        
    )    
    if 'single_division' in tournament_data and tournament_data['single_division']:        
        if 'finals_num_qualifiers' not in tournament_data or tournament_data['finals_num_qualifiers'] == "":            
            raise BadRequest('finals_num_qualifiers not found in post data')            
        new_tournament.single_division=True
        new_division = tables.Division(            
            division_name = new_tournament.tournament_name+"_single",
            finals_num_qualifiers = tournament_data['finals_num_qualifiers']
        )
        
        if tournament_data['scoring_type'] == "HERB":
            new_division.number_of_scores_per_entry=1
        if 'use_stripe' in tournament_data and tournament_data['use_stripe']:
            new_division.use_stripe = True
            new_division.stripe_sku=tournament_data['stripe_sku']
        if 'local_price' in tournament_data and tournament_data['use_stripe'] == False: 
            new_division.local_price=tournament_data['local_price']
        if 'team_tournament' in tournament_data and tournament_data['team_tournament']:    
            new_division.team_tournament = True
        else:
            new_division.team_tournament = False    
        new_division.scoring_type=tournament_data['scoring_type']
            
        db.session.add(new_division)
        new_tournament.divisions.append(new_division)        
    else:
        new_tournament.single_division=False    
    db.session.add(new_tournament)
    db.session.commit()
    return new_tournament
    
def create_roles(app,custom_roles=[]):
    roles = ['admin','desk','scorekeeper','void','player']                    
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
    
        
