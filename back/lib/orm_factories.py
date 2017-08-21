from lib.PssConfig import PssConfig
from werkzeug.exceptions import BadRequest,Unauthorized,Conflict
from base64 import b64encode
import os
from lib import roles_constants
import random

#FIXME : move this back to route
def create_event(user_creating_event, tables, input_data, new_event_tables):
    secret_key=b64encode(os.urandom(24)).decode('utf-8')        
    new_event = tables.Events(name=input_data['name'],flask_secret_key=secret_key)    
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
