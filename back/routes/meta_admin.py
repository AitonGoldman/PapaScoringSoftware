from flask import jsonify,current_app,request, Flask
from blueprints import meta_admin_blueprint
from util import db_util, td_config
from util.db_info import DbInfo
from util.permissions import Admin_permission
from time import sleep
import orm_creation
import json
from orm_creation import RolesEnum
import orm_creation
from orm_creation import create_stanard_roles_and_users,create_queue
import os
import random


@meta_admin_blueprint.route('/meta_admin/list_of_events',methods=['GET'])
def route_get_list_of_events():        
    event_file = open(current_app.td_config['EVENT_FILE_PATH']) 
    event_file_contents = event_file.read()
    event_file.close()
    
    input_data = json.loads(event_file_contents)
    #print input_data
    return jsonify({'data':input_data})    
    #return jsonify({})

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

@meta_admin_blueprint.route('/meta_admin/test_scores',methods=['POST'])
def route_meta_admin_create_test_scores():    
    dummy_app = Flask('dummy_app')
    td_config.assign_loaded_configs_to_app(dummy_app)
    dummy_app.td_config['TEST_STRIPE_SKU']=os.getenv('TEST_STRIPE_SKU',None)
    db_config = td_config.get_db_config()    
    db_info = DbInfo(db_config)    
    db_util.create_db_and_tables(dummy_app, 'test', db_info , drop_tables=True)    
    db_handle = dummy_app.tables.db_handle        
    orm_creation.init_papa_tournaments_divisions(dummy_app)
    create_stanard_roles_and_users(dummy_app)
    db_handle.session.commit()        
    db_util.load_machines_from_json(dummy_app,True)
    machines = dummy_app.tables.Machine.query.all()[0:50]
    division_machine_count = 1
    for division in dummy_app.tables.Division.query.all():        
        for x in range(division_machine_count,division_machine_count+7):
            orm_creation.create_division_machine(dummy_app,machines[x],division)
        division_machine_count=division_machine_count+1
    for x in range(150):
        orm_creation.create_player(dummy_app,{'first_name':'aiton','last_name':'goldman%s'% x,'ifpa_ranking':'123','linked_division_id':'1'})

    for division in dummy_app.tables.Division.query.all():                
        for division_machine in dummy_app.tables.DivisionMachine.query.filter_by(division_id=division.division_id).all():
            for player_id in range(1,150):
                for ticket_num in range(5):
                    orm_creation.create_entry(dummy_app,
                                              division_machine.division_machine_id,
                                              division.division_id,
                                              random.randrange(1,9999),
                                              player_id
                    )
        
    db_handle.engine.dispose()
    del dummy_app
    return jsonify({'data':'test'})    


@meta_admin_blueprint.route('/meta_admin/test_queued_up',methods=['POST'])
def route_meta_admin_create_test_queued_up():    
    dummy_app = Flask('dummy_app')
    td_config.assign_loaded_configs_to_app(dummy_app)
    dummy_app.td_config['TEST_STRIPE_SKU']=os.getenv('TEST_STRIPE_SKU',None)
    db_config = td_config.get_db_config()    
    db_info = DbInfo(db_config)    
    db_util.create_db_and_tables(dummy_app, 'test', db_info , drop_tables=True)    
    db_handle = dummy_app.tables.db_handle        
    orm_creation.init_papa_tournaments_divisions(dummy_app)
    create_stanard_roles_and_users(dummy_app)
    db_handle.session.commit()        
    db_util.load_machines_from_json(dummy_app,True)
    machines = dummy_app.tables.Machine.query.all()[0:50]
    division_machine_count = 1
    for division in dummy_app.tables.Division.query.all():        
        for x in range(division_machine_count,division_machine_count+12):
            orm_creation.create_division_machine(dummy_app,machines[x],division)
        division_machine_count=division_machine_count+1
    for x in range(15):
        orm_creation.create_player(dummy_app,{'first_name':'aiton','last_name':'goldman%s'% x,'ifpa_ranking':'123','linked_division_id':'1'})
    for division in dummy_app.tables.Division.query.all():                
        for division_machine in dummy_app.tables.DivisionMachine.query.filter_by(division_id=division.division_id).all():
            new_queue = create_queue(dummy_app,division_machine.division_machine_id,1)
            new_queue = create_queue(dummy_app,division_machine.division_machine_id,2)
            new_queue = create_queue(dummy_app,division_machine.division_machine_id,3)
            new_queue = create_queue(dummy_app,division_machine.division_machine_id,4)
            new_queue = create_queue(dummy_app,division_machine.division_machine_id,5)
            new_queue = create_queue(dummy_app,division_machine.division_machine_id,6)                                            
    db_handle.engine.dispose()
    del dummy_app
    return jsonify({'data':'test'})    



@meta_admin_blueprint.route('/meta_admin/test_db_with_tournaments_and_player_and_team/<use_stripe>',methods=['POST'])
def route_meta_admin_create_db_and_tournaments_and_player_and_team(use_stripe):    
    dummy_app = Flask('dummy_app')
    td_config.assign_loaded_configs_to_app(dummy_app)
    dummy_app.td_config['TEST_STRIPE_SKU']=os.getenv('TEST_STRIPE_SKU',None)
    db_config = td_config.get_db_config()    
    db_info = DbInfo(db_config)    
    db_util.create_db_and_tables(dummy_app, 'test', db_info , drop_tables=True)    
    db_handle = dummy_app.tables.db_handle    
    if use_stripe == 'stripe':
        test_stripe_sku = os.getenv('TEST_STRIPE_SKU',None)
        orm_creation.init_papa_tournaments_divisions(dummy_app,use_stripe=True,stripe_sku=test_stripe_sku)
    else:
        orm_creation.init_papa_tournaments_divisions(dummy_app)
    create_stanard_roles_and_users(dummy_app)
    test_player = orm_creation.create_player(dummy_app,{'first_name':'aiton','last_name':'goldman','ifpa_ranking':'123','linked_division_id':'1'})
    test_player_two = orm_creation.create_player(dummy_app,{'first_name':'aiton','last_name':'goldman2','ifpa_ranking':'123','linked_division_id':'1'})
    test_player_three = orm_creation.create_player(dummy_app,{'first_name':'aiton','last_name':'goldman3','ifpa_ranking':'123','linked_division_id':'1'})
    test_player_four = orm_creation.create_player(dummy_app,{'first_name':'aiton','last_name':'goldman4','ifpa_ranking':'123','linked_division_id':'1'})

    db_handle.session.commit()    
    orm_creation.create_team(dummy_app,{'team_name':'test_team','players':[str(test_player.player_id)]})
    db_util.load_machines_from_json(dummy_app,True)
    db_handle.engine.dispose()
    del dummy_app
    return jsonify({'data':'test'})    

@meta_admin_blueprint.route('/meta_admin/test_db_with_tournaments',methods=['POST'])
def route_meta_admin_create_db_and_tournaments():    
    dummy_app = Flask('dummy_app')    
    db_info = DbInfo({'DB_TYPE':'sqlite'})
    db_util.create_db_and_tables(dummy_app, 'test', db_info , drop_tables=True)    
    db_handle = dummy_app.tables.db_handle
    create_stanard_roles_and_users(dummy_app)
    db_util.load_machines_from_json(dummy_app,True)
    orm_creation.init_papa_tournaments_divisions(dummy_app)
    db_handle.engine.dispose()
    del dummy_app
    return jsonify({'data':'test'})    

@meta_admin_blueprint.route('/meta_admin/test_db_with_machines',methods=['POST'])
def route_meta_admin_create_db_and_load_machines():    
    dummy_app = Flask('dummy_app')    
    db_config = td_config.get_db_config()    
    db_info = DbInfo(db_config)    
    db_util.create_db_and_tables(dummy_app, 'test', db_info , drop_tables=True)    
    db_handle = dummy_app.tables.db_handle
    create_stanard_roles_and_users(dummy_app)
    db_util.load_machines_from_json(dummy_app,True)
    db_handle.engine.dispose()
    del dummy_app
    return jsonify({'data':'test'})    

@meta_admin_blueprint.route('/meta_admin/test_db',methods=['POST'])
def route_meta_admin_wipe_test_db():    
    dummy_app = Flask('dummy_app')    
    db_info = DbInfo({'DB_TYPE':'sqlite'})
    db_util.create_db_and_tables(dummy_app, 'test', db_info , drop_tables=True)    
    db_handle = dummy_app.tables.db_handle
    create_stanard_roles_and_users(dummy_app)
    db_util.load_machines_from_json(dummy_app,True)
    db_handle.engine.dispose()
    del dummy_app
    return jsonify({'data':'test'})    

@meta_admin_blueprint.route('/meta_admin/healthcheck',methods=['GET'])
def route_meta_admin_health_check():    
    return jsonify({'data':'METAADMIN_HEALTHY'})    
