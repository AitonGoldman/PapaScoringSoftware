from sqlalchemy.orm import joinedload
import itertools
from werkzeug.exceptions import BadRequest

def get_queue_for_tounament_machine(app,tournament_machine_id):
    return app.tables.Queues.query.options(joinedload("tournament_machine"),joinedload("player")).filter_by(tournament_machine_id=tournament_machine_id).order_by(app.tables.Queues.position).all()

def get_queue_for_tounament(app,tournament_id):
    queues = app.tables.Queues.query.options(joinedload("player")).join(app.tables.TournamentMachines).filter_by(tournament_id=tournament_id).order_by(app.tables.Queues.position).all()
    sorted_input = sorted(queues, key=lambda queue: queue.tournament_machine_id)
    return itertools.groupby(sorted_input, key=lambda queue: queue.tournament_machine_id)
    

    #for queue in queues:
    #    if queue.tournament_machine_id not in tournament_queues_dict:
    #        tournament_queues_dict[queue.tournament_machine_id]=[]
    #    tournament_queues_dict[queue.tournament_machine_id].append(queue)
        
def get_queue_player_is_already_in(player_id,app):
    return app.tables.Queues.query.options(joinedload("tournament_machine"),joinedload("player")).filter_by(player_id=player_id).first()

def get_position_of_player_in_queue(app,player_id):
    current_player_queue = app.tables.Queues.query.options(joinedload("tournament_machine"),joinedload("player")).filter_by(player_id=player_id).first()
    if current_player_queue:
        return current_player_queue.position
    else:
        return None    

def add_player_to_queue(player_id,queues,app,tournament_machine_id):
    queues_to_lock_for_addition = app.tables.Queues.query.with_for_update().filter_by(tournament_machine_id=tournament_machine_id).all()
    for index,queue in enumerate(queues):
        if queue.player_id is None:
            break
    if queue.player_id is not None:
        raise BadRequest('no room left in queue')
    if queue.player_id is None:
        queue.player_id=player_id
    return queue    

def bump_player_down_queue(app,tournament_machine_id,queues):            
    #FIXME : actually use bump_amount to allow for larger bumps than 1
    queues_to_lock_for_for_removal = app.tables.Queues.query.with_for_update().filter_by(tournament_machine_id=tournament_machine_id).all()    
    
    player_id_to_move_up=queues[1].player_id
    queues[1].player_id=queues[0].player_id
    queues[0].bumped = queues[1].bumped
    queues[1].bumped = True     
    queues[0].player_id=player_id_to_move_up
    return queues

def remove_player_from_queue(app,player_id,queues=None,tournament_machine_id=None,position_in_queue=None):
    if tournament_machine_id is None:
        tournament_machine_id=queues[0].tournament_machine_id
    queues_to_lock_for_for_removal = app.tables.Queues.query.with_for_update().filter_by(tournament_machine_id=tournament_machine_id).all()
    if queues is None:        
        queues = get_queue_for_tounament_machine(current_app,tournament_machine_id)

    if position_in_queue is None:
        position_in_queue=get_position_of_player_in_queue(app,player_id)
        if position_in_queue is None:
            return False
    #sorted_remove_queue=get_sorted_queue_for_tournament_machine(queues)
    sorted_remove_queue=queues
    players_to_notify=[]
    for index,queue in enumerate(sorted_remove_queue):
        if index == len(sorted_remove_queue)-1:
            queue.player_id=None
            break
        if index >= position_in_queue-1:
            queue.player_id=sorted_remove_queue[index+1].player_id
            queue.bumped=sorted_remove_queue[index+1].bumped
            sorted_remove_queue[index+1].bumped=False
    return True

def get_sorted_queue_for_tournament_machine(queues):    
    return sorted(queues, key=lambda queue: queue.position)
