from werkzeug.exceptions import BadRequest
from util import db_util
import datetime

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
        if division_machine.division.meta_division_id:
            tokens = tables.Token.query.filter_by(player_id=player.player_id,
                                                  metadivision_id=division_machine.division.meta_division_id,
                                                  used=False).all()
        else:
            tokens = tables.Token.query.filter_by(player_id=player.player_id,
                                                  division_id=division_machine.division.division_id,
                                                  used=False).all()
        if tables.DivisionMachine.query.filter_by(player_id=player.player_id).first():
            return False
    if team:
        if division_machine.division.meta_division_id:
            tokens = tables.Token.query.filter_by(team_id=team.team_id,
                                                  metadivision_id=division_machine.division.meta_division_id,
                                                  used=False).all()
        else:
            tokens = tables.Token.query.filter_by(team_id=team.team_id,
                                                  division_id=division_machine.division.division_id,
                                                  used=False).all()
        if tables.DivisionMachine.query.filter_by(team_id=team.team_id).first():
            return False
    
    if len(tokens) == 0:
        return False
    
    # check that player is not on a queue for a different machine (note : this is a special case - we just yank them off the queue)
    return True
    

def set_token_start_time(app,player,division_machine):
    db = db_util.app_db_handle(app)
    tables = db_util.app_db_tables(app)        
    if division_machine.division.meta_division_id is None:
        token_to_set = tables.Token.query.filter_by(player_id=player.player_id,
                                                    division_id=division_machine.division.division_id,
                                                    used=False).first()
    else:
        token_to_set = tables.Token.query.filter_by(player_id=player.player_id,
                                                    metadivision_id=division_machine.division.meta_division_id,
                                                    used=False).first()
    token_to_set.game_started_date=datetime.datetime.now()
    token_to_set.division_machine_id = division_machine.division_machine_id
    db.session.commit()
    pass

def remove_player_from_queue(app,player=None,division_machine=None):
    db = db_util.app_db_handle(app)
    tables = db_util.app_db_tables(app)
    if player:
        queue = tables.Queue.query.filter_by(player_id=player.player_id).first()
    if division_machine:
        queue = division_machine.queue
    if queue is None:
        return False
    division_machine = queue.division_machine
    
    if len(queue.queue_child) > 0:        
        if queue.parent_id is None:            
            division_machine.queue_id=queue.queue_child[0].queue_id
            db.session.commit()                            
        else:            
            queue.queue_child[0].parent_id=queue.parent_id
            db.session.commit()                
    else:
        if queue.parent_id is None:
            division_machine.queue_id=None
            db.session.commit()                            
    db.session.delete(queue)    
    db.session.commit()    
    return queue
    
def get_queue_from_division_machine(division_machine,json_output=False):
    if division_machine.queue is None:
        return []
    queue_list = []
    queue = division_machine.queue    
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
