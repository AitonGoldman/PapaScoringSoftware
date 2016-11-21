from flask import jsonify,current_app,request, Flask
from blueprints import meta_admin_blueprint
from util import db_util, td_config
from util.db_info import DbInfo
from util.permissions import Admin_permission
from time import sleep
import json

def generate_test_user(username,dummy_app,db_handle,roles=[]):
    
    user = dummy_app.tables.User(
        username=username        
    )
    user.crypt_password(username)
    db_handle.session.add(user)
    db_handle.session.commit()
    user = dummy_app.tables.User.query.filter_by(username=username).first()
    for role in roles:
        role = dummy_app.tables.Role.query.filter_by(name=role).first()        
        user.roles.append(role)
        db_handle.session.commit()

def generate_test_player(first_name,last_name,dummy_app,db_handle):
    
    player = dummy_app.tables.Player(
        first_name=first_name,
        last_name=last_name,
        ifpa_ranking=15        
    )    
    db_handle.session.add(player)
    db_handle.session.commit()
    player = dummy_app.tables.Player.query.filter_by(player_id=player.player_id).first()
    role = dummy_app.tables.Role.query.filter_by(name='player').first()        
    player.roles.append(role)
    db_handle.session.commit()
    return player

def generate_test_team(players,dummy_app,db_handle):
    
    team = dummy_app.tables.Team(
        team_name="test_team"
    )    
    db_handle.session.add(team)
    db_handle.session.commit()
    for player in players:
        team.players.append(player)            
    db_handle.session.commit()
    
#FIXME : needs protection
#FIXME : need to pull db creation out into seperate function
@meta_admin_blueprint.route('/meta_admin/db',methods=['POST'])
def route_meta_admin_create_db():    
    dummy_app = Flask('dummy_app')
    input_data = json.loads(request.data)
    db_config = td_config.get_db_config()    
    db_util.create_db_and_tables(dummy_app, input_data['db_name'], DbInfo(db_config))
    del dummy_app
    return jsonify({'data':input_data['db_name']})    


@meta_admin_blueprint.route('/meta_admin/test_db_with_tournaments_and_player_and_team',methods=['POST'])
def route_meta_admin_create_db_and_tournaments_and_player_and_team():    
    dummy_app = Flask('dummy_app')    
    db_info = DbInfo({'DB_TYPE':'sqlite'})
    db_util.create_db_and_tables(dummy_app, 'test', db_info , drop_tables=True)
    db_url = db_util.generate_db_url('test', db_info)
    db_handle = dummy_app.tables.db_handle
    for role in ['admin','desk','scorekeeper','void','player']:
        db_handle.session.add(dummy_app.tables.Role(name=role))
        db_handle.session.commit()
    
    generate_test_user('test_admin',dummy_app, db_handle,['admin','scorekeeper','desk','void'])            
    generate_test_user('test_scorekeeper',dummy_app, db_handle,['scorekeeper','void'])                
    generate_test_user('test_desk',dummy_app, db_handle,['desk','void'])            
    test_player = generate_test_player('aiton','goldman',dummy_app,db_handle)
    generate_test_team([test_player],dummy_app,db_handle)
    db_util.load_machines_from_json(dummy_app,True)
    db_util.init_papa_tournaments_divisions(dummy_app.tables)
    db_handle.engine.dispose()
    del dummy_app
    return jsonify({'data':'test'})    

@meta_admin_blueprint.route('/meta_admin/test_db_with_tournaments',methods=['POST'])
def route_meta_admin_create_db_and_tournaments():    
    dummy_app = Flask('dummy_app')    
    db_info = DbInfo({'DB_TYPE':'sqlite'})
    db_util.create_db_and_tables(dummy_app, 'test', db_info , drop_tables=True)
    db_url = db_util.generate_db_url('test', db_info)
    db_handle = dummy_app.tables.db_handle
    for role in ['admin','desk','scorekeeper','void','player']:
        db_handle.session.add(dummy_app.tables.Role(name=role))
        db_handle.session.commit()
    
    generate_test_user('test_admin',dummy_app, db_handle,['admin','scorekeeper','desk','void'])            
    generate_test_user('test_scorekeeper',dummy_app, db_handle,['scorekeeper','void'])                
    generate_test_user('test_desk',dummy_app, db_handle,['desk','void'])            
    db_util.load_machines_from_json(dummy_app,True)
    db_util.init_papa_tournaments_divisions(dummy_app.tables)
    db_handle.engine.dispose()
    del dummy_app
    return jsonify({'data':'test'})    


@meta_admin_blueprint.route('/meta_admin/test_db_with_machines',methods=['POST'])
def route_meta_admin_create_db_and_load_machines():    
    dummy_app = Flask('dummy_app')    
    db_info = DbInfo({'DB_TYPE':'sqlite'})
    db_util.create_db_and_tables(dummy_app, 'test', db_info , drop_tables=True)
    db_url = db_util.generate_db_url('test', db_info)
    db_handle = dummy_app.tables.db_handle
    for role in ['admin','desk','scorekeeper','void','player']:
        db_handle.session.add(dummy_app.tables.Role(name=role))
        db_handle.session.commit()
    
    generate_test_user('test_admin',dummy_app, db_handle,['admin','scorekeeper','desk','void'])            
    generate_test_user('test_scorekeeper',dummy_app, db_handle,['scorekeeper','void'])                
    generate_test_user('test_desk',dummy_app, db_handle,['desk','void'])            
    db_util.load_machines_from_json(dummy_app,True)
    db_handle.engine.dispose()
    del dummy_app
    return jsonify({'data':'test'})    

    


@meta_admin_blueprint.route('/meta_admin/test_db',methods=['POST'])
def route_meta_admin_wipe_test_db():    
    dummy_app = Flask('dummy_app')    
    db_info = DbInfo({'DB_TYPE':'sqlite'})
    db_util.create_db_and_tables(dummy_app, 'test', db_info , drop_tables=True)
    db_url = db_util.generate_db_url('test', db_info)
    db_handle = dummy_app.tables.db_handle
    for role in ['admin','desk','scorekeeper','void']:
        db_handle.session.add(dummy_app.tables.Role(name=role))
        db_handle.session.commit()
    
    generate_test_user('test_admin',dummy_app, db_handle,['admin','scorekeeper','desk','void'])            
    generate_test_user('test_scorekeeper',dummy_app, db_handle,['scorekeeper','void'])                
    generate_test_user('test_desk',dummy_app, db_handle,['desk','void'])                
    db_util.load_machines_from_json(dummy_app,True)
    db_handle.engine.dispose()
    del dummy_app
    return jsonify({'data':'test'})    

@meta_admin_blueprint.route('/meta_admin/healthcheck',methods=['GET'])
def route_meta_admin_health_check():    
    return jsonify({'data':'METAADMIN_HEALTHY'})    
