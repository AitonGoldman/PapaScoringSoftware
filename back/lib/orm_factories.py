from lib.PssConfig import PssConfig
from werkzeug.exceptions import BadRequest,Unauthorized,Conflict
from base64 import b64encode
import os
from lib import roles_constants
from lib import token_helpers
import random
from lib.serializer import deserialize
import datetime

ACTIONS_TO_ADD_TICKET_SUMMARY_TO = ["Score Recorded","Ticket Purchase","Player Ticket Purchase Complete"]

def create_event(user_creating_event, tables, input_data, new_event_tables,event_owner_pss_user_id):
    secret_key=b64encode(os.urandom(24)).decode('utf-8')        
    new_event = tables.Events(name=input_data['name'],flask_secret_key=secret_key)    
    new_event.event_creator_pss_user_id=event_owner_pss_user_id
    tables.db_handle.session.add(new_event)
    new_event_user = new_event_tables.EventUsers(pss_user_id=user_creating_event.pss_user_id,
                                                 password_crypt=user_creating_event.event_user.password_crypt)
    td_role = new_event_tables.EventRoles.query.filter_by(name=roles_constants.TOURNAMENT_DIRECTOR).first()
    
    existing_user_in_new_event = new_event_tables.PssUsers.query.filter_by(pss_user_id=user_creating_event.pss_user_id).first()
    existing_user_in_new_event.event_roles.append(td_role)
    new_event_tables.db_handle.session.add(new_event_user)
    user_creating_event.events.append(new_event)
    new_event_tables.db_handle.session.commit()
    tables.db_handle.session.commit()        
    return new_event

def create_event_tables(pss_config,new_event_app):
    new_event_tables = pss_config.get_db_info().getImportedTables(new_event_app,"pss_admin")    
    existing_event = new_event_tables.Events.query.filter_by(name=new_event_app.name).first()
    if existing_event is not None:
        raise Conflict('Event already exists')             
    metadata = new_event_tables.db_handle.metadata
    metadata.create_all(new_event_tables.db_handle.session.bind)
    return new_event_tables

def populate_event_user(flask_app,password,
                        pss_user,event_roles,
                        commit=False):
    event_user = flask_app.tables.EventUsers()
    event_user.crypt_password(password)
    pss_user.event_user = event_user
    event = flask_app.tables.Events.query.filter_by(name=flask_app.name).first()
    pss_user.events.append(event)
    for role in event_roles:
        pss_user.event_roles.append(role)                
    if commit:
        flask_app.tables.db_handle.session.commit()        
    return event_user

def modify_event_user(flask_app,
                      pss_user,event_role,
                      password=None,commit=False):        
    if password:        
        pss_user.event_user.crypt_password(password)
    if event_role:        
        pss_user.event_roles=[]        
        pss_user.event_roles.append(event_role)                
    if commit:
        flask_app.tables.db_handle.session.commit()        
    return pss_user


def create_user(flask_app,username,
                first_name,last_name,
                password,admin_roles=[],
                event_roles=[], extra_title=None,
                commit=False):
    tables=flask_app.tables
    user = tables.PssUsers(username=username,
                           first_name=first_name,
                           last_name=last_name)
    if extra_title:
        user.extra_title=extra_title
    populate_event_user(flask_app,password,user,event_roles)
    tables.db_handle.session.add(user)
    for role in admin_roles:
        user.admin_roles.append(role)
    if commit:
        tables.db_handle.session.commit()

    return user


def populate_player(flask_app,new_player,
                    ifpa_ranking,
                    commit=False):
    event_player = flask_app.tables.EventPlayers(ifpa_ranking=ifpa_ranking)    
    event_player.event_player_pin=random.randrange(1000,9999)    

    new_player.event_player = event_player
    
    event = flask_app.tables.Events.query.filter_by(name=flask_app.name).first()
    new_player.events.append(event)
    player_role = flask_app.tables.PlayerRoles.query.filter_by(name=roles_constants.PSS_PLAYER).first()
    new_player.player_roles.append(player_role)
    if commit:
        flask_app.tables.db_handle.session.commit()        
    return event_player

def create_player(flask_app,
                  first_name,last_name,
                  ifpa_ranking,extra_title=None,
                  commit=False):
    tables=flask_app.tables
    new_player = tables.Players(first_name=first_name,
                          last_name=last_name)
    if extra_title:
        new_player.extra_title=extra_title
    populate_player(flask_app,new_player,ifpa_ranking)
    tables.db_handle.session.add(new_player)
    if commit:
        tables.db_handle.session.commit()

    return new_player

def create_tournament(flask_app,tournament_name,
                      multi_division_tournament_name=None,
                      multi_division_tournament_id=None,                      
                      commit=False,
                      finals_style=None):
    new_tournament = flask_app.tables.Tournaments(tournament_name=tournament_name)
    flask_app.tables.db_handle.session.add(new_tournament)
    if multi_division_tournament_name and multi_division_tournament_id is None:
        multi_division_tournament = flask_app.tables.MultiDivisionTournaments(multi_division_tournament_name=multi_division_tournament_name)
        flask_app.tables.db_handle.session.add(multi_division_tournament)
        new_tournament.multi_division_tournament=multi_division_tournament
        new_tournament.multi_division_tournament_name=multi_division_tournament_name
    if multi_division_tournament_id:
        multi_division_tournament = flask_app.tables.MultiDivisionTournaments.query.filter_by(multi_division_tournament_id=multi_division_tournament_id).first()
        if multi_division_tournament is None:
            raise BadRequest('Bad multi division tournament id')                            
        new_tournament.multi_division_tournament=multi_division_tournament
        new_tournament.multi_division_tournament_name=multi_division_tournament.multi_division_tournament_name
    if finals_style:
        new_tournament.finals_style=finals_style
    if commit:
        flask_app.tables.db_handle.session.commit()
    return new_tournament

def create_queue_for_tournament_machine(app,tournament_machine,max_queue_length,commit=False):
    old_queue_slot=None
    for queue_position in range(max_queue_length,0,-1):
        new_queue_slot=app.tables.Queues()
        new_queue_slot.position=queue_position
        if old_queue_slot:            
            new_queue_slot.queue_child=old_queue_slot
        new_queue_slot.tournament_machine = tournament_machine
        app.tables.db_handle.session.add(new_queue_slot)
        old_queue_slot=new_queue_slot
    
    if commit:
        app.tables.db_handle.session.commit()
    
    
def create_audit_log(app, audit_log_params, commit=False):
    # action,user_id, player_id=None,
    #                 division_machine_id=None,team_id=None,generic_json_data=None,
    #                 commit=True,summary=False,description=None
    global ACTIONS_TO_ADD_TICKET_SUMMARY_TO
    tables = app.tables
    audit_log = tables.AuditLogs()
    deserialize.deserialize_json(audit_log,audit_log_params,app,allow_foreign_keys=True)
    #audit_log.action=action
    audit_log.action_date=datetime.datetime.now()    
    #if 'pss_user_id' in audit_log_params and audit_log_params['pss_user_id'] is not None:
    #    audit_log.player_initiated=False
    #if 'player_id' in audit_log_params and audit_log_params['player_id'] is not None and 'pss_user_id' not in audit_log_params:
    #    audit_log.player_initiated=True            
    tables.db_handle.session.add(audit_log)
    if commit is True:
        tables.db_handle.session.commit()    
    if audit_log_params['action'] not in ACTIONS_TO_ADD_TICKET_SUMMARY_TO:
        return
    player = tables.Players.query.filter_by(player_id=audit_log_params['player_id']).first()
    
    tournament_token_count,meta_tournament_token_count = token_helpers.get_number_of_unused_tickets_for_player_in_all_tournaments(player,
                                                                                                                                  app,
                                                                                                                                  remove_empty_tournaments=True)
    token_count_string = "ticket summary - " + ", ".join([token_count['tournament_name']+':'+str(token_count['count']) for token_count in tournament_token_count])
    #print tournament_token_count_string
    if len(meta_tournament_token_count) > 0:
        meta_tournament_token_count_string = ", ".join([token_count['meta_tournament_name']+':'+str(token_count['count']) for token_count in meta_tournament_token_count])
        token_count_string = token_count_string + ", "+meta_tournament_token_count_string
    
    
    audit_log_ticket_summary = tables.AuditLogs()
    audit_log_ticket_summary.action="Ticket Summary"
    audit_log_ticket_summary.action_date=datetime.datetime.now()
    if 'player_id' in audit_log_params and audit_log_params['player_id']:
         audit_log_ticket_summary.player_id=audit_log_params['player_id']
    audit_log_ticket_summary.description=token_count_string    
    audit_log_ticket_summary.summary=True
    tables.db_handle.session.add(audit_log_ticket_summary)
    if commit is True:
        tables.db_handle.session.commit()
    
