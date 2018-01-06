import datetime
import random
import os 
from pss_models_v2.PssUsers import generate_pss_users_class
from pss_models_v2.Players import generate_players_class
from pss_models_v2.Events import generate_events_class
from pss_models_v2.EventRoles import generate_event_roles_class
from pss_models_v2.EventRoleMappings import generate_event_role_mappings_class
from pss_models_v2.EventPlayersInfo import generate_event_players_info_class
from pss_models_v2.Queues import generate_queues_class
from pss_models_v2.Tournaments import generate_tournaments_class
from pss_models_v2.MetaTournaments import generate_meta_tournaments_class
from pss_models_v2.Machines import generate_machines_class
from pss_models_v2.TournamentMachines import generate_tournament_machines_class
from pss_models_v2.MultiDivisionTournaments import generate_multi_division_tournaments_class
from pss_models_v2.TokenPurchaseSummaries import generate_token_purchase_summaries_class
from pss_models_v2.TokenPurchases import generate_token_purchases_class
from pss_models_v2.Tokens import generate_tokens_class
from pss_models_v2.Teams import generate_teams_class
from pss_models_v2.AuditLogs import generate_audit_logs_class
from pss_models_v2.Entries import generate_entries_class
from pss_models_v2.Scores  import generate_scores_class

from lib_v2 import roles_constants
from lib_v2.serializers import deserializer
from sqlalchemy.orm import foreign, remote
import warnings
from sqlalchemy import exc as sa_exc,func
from flask import Flask
from lib.PssConfig import PssConfig

#from pss_models_v2.TestMapping import generate_test_class

ACTIONS_TO_ADD_TICKET_SUMMARY_TO = ["Score Recorded","Ticket Purchase","Player Ticket Purchase Complete"]

class TableProxy():
    def initialize_tables(self,db_handle):
        self.db_handle=db_handle                
        self.PssUsers = generate_pss_users_class(self.db_handle)
        self.Players = generate_players_class(self.db_handle)
        self.Events = generate_events_class(self.db_handle)
        self.EventRoles = generate_event_roles_class(self.db_handle)                
        self.EventRoleMappings = generate_event_role_mappings_class(self.db_handle)
        self.EventPlayersInfo = generate_event_players_info_class(self.db_handle)
        self.Tournaments = generate_tournaments_class(self.db_handle)
        self.MultiDivisionTournaments = generate_multi_division_tournaments_class(db_handle)        
        self.Machines = generate_machines_class(db_handle)        
        self.TournamentMachines = generate_tournament_machines_class(db_handle)        
        self.MetaTournaments = generate_meta_tournaments_class(db_handle)
        self.Tournaments.multi_division_tournament = self.db_handle.relationship(
            'MultiDivisionTournaments', uselist=False, cascade='all'
        )
        self.Teams = generate_teams_class(db_handle)
        self.TokenPurchaseSummaries = generate_token_purchase_summaries_class(self.db_handle)
        self.TokenPurchases = generate_token_purchases_class(self.db_handle)        
        self.Tokens = generate_tokens_class(self.db_handle)        
        self.Queues = generate_queues_class(self.db_handle)        
        self.AuditLogs = generate_audit_logs_class(self.db_handle)
        self.Entries = generate_entries_class(self.db_handle)
        self.Scores = generate_scores_class(self.db_handle)
        #self.Players.event_roles = self.db_handle.relationship(
        #    'EventPlayerRoleMappings', cascade='all'
        #)

        self.initialize_all_event_relationship()
        #self.Players.event_info = self.db_handle.relationship(
        #    'EventPlayersInfo', cascade='all', uselist=True
        #)
        
        self.Players.events = db_handle.relationship(
            'Events',
            secondary=self.generate_player_event_mapping()
        )
        
        self.PssUsers.event_roles = self.db_handle.relationship(
            'EventRoleMappings', cascade='all'
        )        
        self.PssUsers.events_created = self.db_handle.relationship(
            'Events', cascade='all'            
        )
        self.Tournaments.tournament_machines = self.db_handle.relationship(
            'TournamentMachines', cascade='all'
        )
        self.Events.tournaments = self.db_handle.relationship(
            'Tournaments', cascade='all'
        )                
        self.MetaTournaments.tournaments = self.db_handle.relationship(
            'Tournaments', cascade='all'
        )
        self.TokenPurchases.token_purchase_summaries = self.db_handle.relationship(
            'TokenPurchaseSummaries', cascade='all'
        )
        self.TokenPurchases.tokens = self.db_handle.relationship(
            'Tokens', cascade='all'
        )
        self.Tokens.tournament = self.db_handle.relationship(
            'Tournaments', cascade='all', uselist=False
        )
        self.Tokens.meta_tournament = self.db_handle.relationship(
            'MetaTournaments', cascade='all', uselist=False
        )                
        self.Queues.tournament_machine = db_handle.relationship(
            'TournamentMachines', uselist=False            
        )    
        self.Entries.scores = db_handle.relationship(
            'Scores'
        )    
        
    def generate_player_event_mapping(self):
        Player_Event_mapping = self.db_handle.Table(
            'player_event',
            self.db_handle.Column('player_id', self.db_handle.Integer, self.db_handle.ForeignKey('players.player_id')),
            self.db_handle.Column('event_id', self.db_handle.Integer, self.db_handle.ForeignKey('events.event_id'))
        )
        return Player_Event_mapping
        
    def initialize_event_specific_relationship(self,target_event_id):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=sa_exc.SAWarning)
            self.Players.event_info = self.db_handle.relationship(
                'EventPlayersInfo', cascade='all', uselist=True, 
                primaryjoin="and_(EventPlayersInfo.player_id==Players.player_id,EventPlayersInfo.event_id==%s)"%target_event_id
            )
            
    def initialize_all_event_relationship(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=sa_exc.SAWarning)
            self.Players.event_info = self.db_handle.relationship(
                'EventPlayersInfo', cascade='all', uselist=True
            )                        
            
    def commit_changes(self):
        self.db_handle.session.commit()
        
    def get_user_by_username(self,username):
        #return self.PssUsers.query.options(joinedload("admin_roles"),joinedload("event_roles"),joinedload("events"),joinedload("event_user")).filter_by(username=input_data['username']).first()
        return self.PssUsers.query.filter_by(username=username).first()

    def get_all_users(self):
        return self.PssUsers.query.all()
    
    def get_user_by_id(self,id):
        #return self.PssUsers.query.options(joinedload("admin_roles"),joinedload("event_roles"),joinedload("events"),joinedload("event_user")).filter_by(username=input_data['username']).first()
        return self.PssUsers.query.filter_by(pss_user_id=id).first()
    
    def get_event_by_eventname(self,eventname):
        return self.Events.query.filter_by(name=eventname).first()            

    def get_event_by_event_id(self,event_id):
        return self.Events.query.filter_by(event_id=event_id).first()            

    def get_all_active_events(self,event_id):
        return self.Events.query.filter_by(event_id=event_id).first()            
    
    def get_query_for_available_tokens(self, event_id):
        return self.Tokens.query.filter_by(used=False,voided=False,paid_for=True,deleted=False,event_id=event_id)

    def get_tournament_machine_player_is_playing(self,player,event_id):
        return self.TournamentMachines.query.filter_by(player_id=player.player_id,event_id=event_id).first()

    def get_available_token_count_for_tournament(self,event_id,player,tournament):
        tournament_results,meta_tournament_results = self.get_available_token_count_for_tournaments(event_id,player)
        if tournament.meta_tournament_id:
            return meta_tournament_results[tournament.meta_tournament_id]['count']
        else:
            return tournament_results[tournament.tournament_id]['count']
    def get_all_machines(self):
        return self.Machines.query.all()
    
    def get_all_event_roles(self):
        return self.EventRoles.query.all()
        
    def get_available_token_count_for_tournaments(self,event_id,player):                
        tournament_results={}
        meta_tournament_results={}
        results = self.get_query_for_available_tokens(event_id).all()        
        for result in results:            
            if result.tournament_id:
                if result.tournament_id in tournament_results:
                    count = tournament_results[result.tournament_id]['count']
                    tournament_results[result.tournament_id]={"tournament_name":result.tournament.tournament_name,"count":count+1}                
                else:
                    tournament_results[result.tournament_id]={"tournament_name":result.tournament.tournament_name,"count":1}
                
            if result.meta_tournament_id:
                if result.meta_tournament_id in meta_tournament_results:                    
                    count = meta_tournament_results[result.meta_tournament_id]['count']
                    meta_tournament_results[result.meta_tournament_id]={"meta_tournament_name":result.meta_tournament.meta_tournament_name,"count":count+1}
                else:
                    meta_tournament_results[result.meta_tournament_id]={"meta_tournament_name":result.meta_tournament.meta_tournament_name,"count":1}
        return tournament_results,meta_tournament_results
    
    
    def create_token_purchase(self,player_initiated=False,commit=False):
        new_token_purchase = self.TokenPurchases()
        if player_initiated:
            new_token_purchase.stripe_purchase=True
            new_token_purchase.completed=False
            
        else:
            new_token_purchase.stripe_purchase=False
            new_token_purchase.completed=True
            
        self.db_handle.session.add(new_token_purchase)
        if commit:
            self.db_handle.session.commit()
        return new_token_purchase

    def create_token_purchase_summary(self,token_purchase,commit=False):
        new_token_purchase_summary = self.TokenPurchaseSummaries()
        self.db_handle.session.add(new_token_purchase_summary)
        token_purchase.token_purchase_summaries.append(new_token_purchase_summary)
        if commit:
            self.db_handle.session.commit()
        return new_token_purchase_summary

    def create_token(self, event_id,
                     player_initiated=False,comped=False,
                     player=None,team_id=None,
                     tournament=None,meta_tournament=None,
                     commit=False):
        new_token = self.Tokens()
        new_token.event_id=event_id
        if player_initiated:
            new_token.paid_for=False
        else:
            new_token.paid_for=True
        new_token.comped=comped
        if meta_tournament or (tournament and tournament.team_tournament is False):
            new_token.player_id=player.player_id            
        if tournament and tournament.team_tournament :
            new_token.team_id=player.event_info.team_id
        if tournament:
            new_token.tournament_id=tournament.tournament_id
        else:
            new_token.meta_tournament_id=meta_tournament.meta_tournament_id
        self.db_handle.session.add(new_token)
        if commit:
            self.db_handle.session.commit()
        return new_token
    
    def create_event_tables(self, event_id):
        #new_event_app = Flask('dummy')
        pss_config=PssConfig()
        #new_db_handle = pss_config.get_db_info().create_db_handle(new_event_app)
        token_purchase_summaries_class = generate_token_purchase_summaries_class(self.db_handle,event_id)
        token_purchases_class = generate_token_purchases_class(self.db_handle,event_id)
        tokens = generate_tokens_class(self.db_handle,event_id)        
        #new_event_tables = pss_config.get_db_info().getImportedTables(new_event_app,"pss_admin")    
        #existing_event = new_event_tables.Events.query.filter_by(name=new_event_app.name).first()
        #if existing_event is not None:
        #    raise Conflict('Event already exists')             
        metadata = self.db_handle.metadata
        metadata.create_all(self.db_handle.session.bind)
        #return new_event_tables        
    
    def create_event(self,current_user,                     
                     event_info,
                     commit=False):
        new_event = self.Events()
        new_event.event_creator_pss_user_id=current_user.pss_user_id
        deserializer.deserialize_json(new_event,event_info)
        #event creation logic goes here
        self.db_handle.session.add(new_event)
        if commit:
            self.db_handle.session.commit()
        return new_event

    def edit_event(self, event_info,
                     commit=False):                    
        event = self.Events.query.filter_by(event_id=event_info['event_id']).first()
        if event is None:
            raise Exception('No event with the specified id')
        deserializer.deserialize_json(event,event_info)
        #event edit logic goes here        
        if commit:
            self.db_handle.session.commit()
        return event

    def create_role(self,role_name,commit=False):        
        event_role = self.EventRoles(event_role_name=role_name)
        self.db_handle.session.add(event_role)        
        if commit:
            self.db_handle.session.commit()
        return event_role

    def update_event_user_roles(self, event_role_ids,
                                event_id, pss_user,
                                commit=False):
        if pss_user.pss_user_id:            
            event_role_mappings_for_event = self.EventRoleMappings.query.filter_by(event_id=event_id,pss_user_id=pss_user.pss_user_id).all()                        
            for event_role_mapping in event_role_mappings_for_event:                
                pss_user.event_roles.remove(event_role_mapping)
                self.db_handle.session.delete(event_role_mapping)                
        for event_role_id in event_role_ids:            
            event_role = self.EventRoles.query.filter_by(event_role_id=event_role_id).first()
            
            if event_role is None:
                raise Exception('Naughty Naughty')
            event_role_mapping = self.EventRoleMappings()
            event_role_mapping.event_id=event_id
            event_role_mapping.pss_user_id=pss_user.pss_user_id
            event_role_mapping.event_role_id=event_role.event_role_id
            event_role_mapping.event_role_name=event_role.event_role_name
            pss_user.event_roles.append(event_role_mapping)        
        if commit:
            self.db_handle.session.commit()
        return pss_user

    def update_player_roles(self,
                            event_id, player,
                            ifpa_ranking=None,
                            selected_division_in_multi_division_tournament=None,
                            commit=False):                
        event = self.get_event_by_event_id(event_id)
        event_player_info = self.EventPlayersInfo()
        event_player_info.event_id=event_id
        event_player_info.player_id=player.player_id        
        if ifpa_ranking:
            event_player_info.ifpa_ranking=ifpa_ranking
        if selected_division_in_multi_division_tournament:
            event_player_info.selected_division_in_multi_division_tournament=selected_division_in_multi_division_tournament
        existing_player_ids_for_event = sorted([player_event_info.player_id_for_event for player_event_info in self.EventPlayersInfo.query.filter_by(event_id=event_id).all()],reverse=True)
        if len(existing_player_ids_for_event)==0:
            event_player_info.player_id_for_event=100
        else:
            event_player_info.player_id_for_event=existing_player_ids_for_event[0]+1                
        player.events.append(event)
        self.db_handle.session.add(event_player_info)
        if commit:
            self.db_handle.session.commit()
        return player
    
    def edit_event_user(self,pss_user_id,
                        event_id,input_data):
        pass

    def create_player(self,
                      first_name,last_name,
                      pin=None,
                      extra_title=None,
                      img_url=None,
                      commit=False):        
        player = self.Players()
        player.first_name=first_name
        player.last_name=last_name        
        if extra_title:
            user.extra_title=extra_title
        if pin:
            player.pin=pin
        else:
            player.pin=random.randrange(1234,9999)
        if img_url:
            player.img_url=img_url
        self.db_handle.session.add(player)
        if commit:            
            self.db_handle.session.commit()
        return player
    
    def create_user(self, username,
                    first_name,last_name,
                    password=None, event_creator=False,                    
                    extra_title=None, commit=False,
                    add_user_to_session=True):        
        user = self.PssUsers()
        user.username=username
        user.first_name=first_name
        user.last_name=last_name
        if extra_title:
            user.extra_title=extra_title
        if event_creator:
            user.event_creator=True
        else:
            user.event_creator=False
        if password:
            user.crypt_password(password)        
        if add_user_to_session:
            self.db_handle.session.add(user)
        if commit:            
            self.db_handle.session.commit()
        return user

    def create_meta_tournament(self, tournaments,
                               input_data,
                               event_id,
                               commit=False):        
        new_meta_tournament = self.MetaTournaments()
        deserializer.deserialize_json(new_meta_tournament,input_data)
        new_meta_tournament.event_id=event_id
        self.db_handle.session.add(new_meta_tournament)
        for tournament in tournaments:
            new_meta_tournament.tournaments.append(tournament)
        if commit:            
            self.db_handle.session.commit()
        return new_meta_tournament

    def edit_meta_tournament(self, meta_tournament,
                             input_data,commit=False):                
        #for tournament in meta_tournament.tournaments:
        #    meta_tournament.tournaments.remove(tournament)
        deserializer.deserialize_json(meta_tournament,input_data)
        if commit:            
            self.db_handle.session.commit()
        return meta_tournament
    
    def search_player(self, player_string):
        return self.Players.query.filter((self.Players.first_name+" "+self.Players.last_name).like(player_string+"%")).all()
    
    def get_all_players(self):
        return self.Players.query.all()

    
    def get_player(self,event_id,player_id=None,
                   player_id_for_event=None,
                   first_name=None,last_name=None,
                   extra_title=None,
                   initialize_event_specific_relationship=False):
        if initialize_event_specific_relationship:
            self.initialize_event_specific_relationship(event_id)
        else:
            self.initialize_all_event_relationship()
        if player_id:
            return self.Players.query.filter_by(player_id=player_id).first()
        if player_id_for_event:
            return self.Players.query.join(self.EventPlayersInfo).filter_by(event_id=event_id,player_id_for_event=player_id_for_event).first()
        if first_name:
            query = self.Players.query.filter_by(first_name=first_name,last_name=last_name)
            if extra_title:
                query = query.filter_by(extra_title=extra_title)
            return query.all()
            
    def get_token_purchase_by_id(self,token_purchase_id):
        return self.TokenPurchases.query.filter_by(token_purchase_id=token_purchase_id).first()

    def get_tokens_by_tournament_id(self,player_id,tournament_id=None,meta_tournament_id=None):
        return self.Tokens.query.filter_by(tournament_id=tournament_id,meta_tournament_id=meta_tournament_id).all()
    
    def get_tournament_by_tournament_id(self,tournament_id):
        return self.Tournaments.query.filter_by(tournament_id=tournament_id).first()

    def get_tournaments(self,event_id,exclude_metatournaments=False):
        query = self.Tournaments.query.filter_by(event_id=event_id)
        if exclude_metatournaments is False:
            return query.filter_by(meta_tournament_id=None).all()        
        return query.all()

    def get_meta_tournaments(self,event_id):
        return self.MetaTournaments.query.filter_by(event_id=event_id).all()
        
    
    def create_multi_division_tournament(self, multi_division_tournament_name,                                         
                                         division_count, tournament_info,
                                         event_id, commit=False):
        new_tournaments=[]
        multi_division_names=['A','B','C','D']
        multi_division_names_to_use=multi_division_names[0:division_count]
        multi_div = self.MultiDivisionTournaments()
        multi_div.multi_division_tournament_name=multi_division_tournament_name
        for division_name in multi_division_names_to_use:
            new_tournament=self.create_tournament(tournament_info,event_id)
            new_tournament.tournament_name=division_name
            new_tournament.multi_division_tournament=multi_div
            self.db_handle.session.add(new_tournament)
            new_tournaments.append(new_tournament)
        if commit:
            self.db_handle.session.commit()
        return new_tournaments
    
    def create_tournament(self,tournament_info,
                          event_id,commit=False):        
        event = self.get_event_by_event_id(event_id)
        #FIXME : Guyh - we should NOT allow a non-valid event id, but
        #        for now we do it because wizard create needs it
        if event is None and commit is True:
            raise Exception('Event specified does not exist')
        new_tournament = self.Tournaments()        
        deserializer.deserialize_json(new_tournament,tournament_info)
        new_tournament.event_id=event_id
        #tournament creation logic goes here
        self.db_handle.session.add(new_tournament)
        if commit:
            self.db_handle.session.commit()
        return new_tournament

    def edit_tournament(self, tournament_info,
                        commit=False):                    
        tournament = self.Tournaments.query.filter_by(tournament_id=tournament_info['tournament_id']).first()
        if tournament is None:
            raise Exception('No tournament with the specified id')
        deserializer.deserialize_json(tournament,tournament_info)
        #event edit logic goes here        
        if commit:
            self.db_handle.session.commit()
        return tournament

    #NEEDS UNIT TEST
    def clear_stripe_prices_from_tournament(self,tournament,commit=False):
        tournament.stripe_price = None
        tournament.stripe_sku = None
        tournament.discount_stripe_price = None
        tournament.discount_stripe_sku = None
        if commit:
            self.db_handle.session.commit()

    #NEEDS UNIT TEST    
    def create_machine(self,machine_info,
                       commit=False):                                    
        new_machine = self.Machines()        
        deserializer.deserialize_json(new_machine,machine_info)        
        self.db_handle.session.add(new_machine)
        if commit:
            self.db_handle.session.commit()
        return new_machine

    def get_machine_by_id(self,machine_id):
        return self.Machines.query.filter_by(machine_id=machine_id).first()

    def get_meta_tournament_by_id(self,meta_tournament_id):
        return self.MetaTournaments.query.filter_by(meta_tournament_id=meta_tournament_id).first()
    
    def get_tournament_machines(self,tournament_id):
        return self.TournamentMachines.query.filter_by(tournament_id=tournament_id,removed=False).all()

    def get_tournament_machine_by_id(self,tournament_machine_id):
        return self.TournamentMachines.query.filter_by(tournament_machine_id=tournament_machine_id).first()
    
    def create_tournament_machine(self,
                                  machine,tournament,
                                  commit=False):
        existing_tournament_machine = self.TournamentMachines.query.filter_by(machine_id=machine.machine_id,tournament_id=tournament.tournament_id).first()
        if existing_tournament_machine:
            existing_tournament_machine.removed = False
            existing_tournament_machine.active = True
            if commit:
                self.db_handle.session.commit()
            return existing_tournament_machine
        
        new_tournament_machine = self.TournamentMachines()                
        new_tournament_machine.machine_id=machine.machine_id
        new_tournament_machine.tournament_machine_name=machine.machine_name
        new_tournament_machine.abbreviation=machine.abbreviation
        new_tournament_machine.active=True
        #new_tournament_machine.tournament_id=tournament.tournament_id
        tournament.tournament_machines.append(new_tournament_machine)
        self.db_handle.session.add(new_tournament_machine)
        # CREATE QUEUES HERE
        if commit:
            self.db_handle.session.commit()
        
        return new_tournament_machine

    def edit_tournament_machine(self,tournament_machine_info,
                                commit=False):
        existing_tournament_machine = self.TournamentMachines.query.filter_by(tournament_machine_id=tournament_machine_info['tournament_machine_id']).first()
        deserializer.deserialize_json(existing_tournament_machine,tournament_machine_info)                
        if existing_tournament_machine.removed:         
            existing_tournament_machine.active=False        
        # CREATE QUEUES HERE
        if commit:
            self.db_handle.session.commit()
        
        return existing_tournament_machine
    
    def create_queue_for_tournament_machine(self,tournament_machine,max_queue_length,event_id,commit=False):
        old_queue_slot=None
        for queue_position in range(max_queue_length,0,-1):
            new_queue_slot=self.Queues()
            new_queue_slot.position=queue_position
            if old_queue_slot:            
                new_queue_slot.queue_child=old_queue_slot
            new_queue_slot.tournament_machine = tournament_machine
            new_queue_slot.event_id=event_id
            self.db_handle.session.add(new_queue_slot)
            old_queue_slot=new_queue_slot
    
        if commit:
            self.db_handle.session.commit()

    def get_queue_player_is_already_in(self,player,event_id):
        return self.Queues.query.filter_by(player_id=player.player_id,event_id=event_id).first()
            
    def get_queue_for_tounament_machine(self,tournament_machine):
        return self.Queues.query.filter_by(tournament_machine_id=tournament_machine.tournament_machine_id).order_by(self.Queues.position).all()
    
    def get_position_of_player_in_queue(self, player,tournament_machine):
        current_player_queue = self.Queues.query.filter_by(player_id=player.player_id,tournament_machine_id=tournament_machine.tournament_machine_id).first()
        if current_player_queue:
            return current_player_queue.position
        else:
            return None    

    def get_sorted_queue_for_tournament_machine(self,tournament_machine,queues=None):    
        if queues is None:
            queues=self.Queues.query.filter_by(tournament_machine_id=tournament_machine.tournament_machine_id)
        return sorted(queues, key=lambda queue: queue.position)

    def bump_player_down_queue(self, player,tournament_machine):
        queues_to_lock_for_for_removal = self.Queues.query.with_for_update().filter_by(tournament_machine_id=tournament_machine.tournament_machine_id).all()
        sorted_bump_queue=self.get_sorted_queue_for_tournament_machine(tournament_machine,queues_to_lock_for_for_removal)        
        position_2_bump=sorted_bump_queue[1].bumped
        position_2_player_id=sorted_bump_queue[1].player_id        
        position_1_player_id=sorted_bump_queue[0].player_id
        sorted_bump_queue[1].bumped=True
        sorted_bump_queue[1].player_id=position_1_player_id        
        sorted_bump_queue[0].bumped=position_2_bump
        sorted_bump_queue[0].player_id=position_2_player_id
        return True
        
    def remove_player_from_queue(self, player,tournament_machine,position_in_queue=None):
        queues_to_lock_for_for_removal = self.Queues.query.with_for_update().filter_by(tournament_machine_id=tournament_machine.tournament_machine_id).all()
        if position_in_queue is None:
            position_in_queue=self.get_position_of_player_in_queue(player,tournament_machine)
            if position_in_queue is None:
                return False
        sorted_remove_queue=self.get_sorted_queue_for_tournament_machine(tournament_machine,queues_to_lock_for_for_removal)        
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
    
    def add_player_to_queue(self,player,app,tournament_machine):
        queues_to_lock_for_addition = app.table_proxy.Queues.query.with_for_update().filter_by(tournament_machine_id=tournament_machine.tournament_machine_id).all()
        for index,queue in enumerate(self.get_sorted_queue_for_tournament_machine(tournament_machine,queues_to_lock_for_addition)):            
            if queue.player_id is None:
                break
        if queue.player_id is not None:
            raise BadRequest('no room left in queue')
        if queue.player_id is None:
            queue.player_id=player.player_id
        return queue    

    def create_audit_log(self, audit_log_params, event_id, player=None, commit=False):
        global ACTIONS_TO_ADD_TICKET_SUMMARY_TO        
        audit_log = self.AuditLogs()
        audit_log.action_date=datetime.datetime.now()

        deserializer.deserialize_json(audit_log,audit_log_params,allow_foreign_keys=True)
        self.db_handle.session.add(audit_log)
        if commit is True:
            self.db_handle.session.commit()    
        if audit_log_params['action'] not in ACTIONS_TO_ADD_TICKET_SUMMARY_TO:
            return
        if player is None:
            player = self.get_player(event_id, player_id=audit_log_params['player_id'])        
        tournament_token_count,meta_tournament_token_count = self.get_available_token_count_for_tournaments(event_id,player)
        list_of_token_counts = [token_count['tournament_name']+':'+str(token_count['count']) for tournament_id,token_count in tournament_token_count.iteritems()]+[token_count['meta_tournament_name']+':'+str(token_count['count']) for meta_tournament_id,token_count in meta_tournament_token_count.iteritems()]
        token_count_string = "ticket summary - " + ", ".join(list_of_token_counts)        
        audit_log_ticket_summary = self.AuditLogs()
        audit_log_ticket_summary.player_id=player.player_id
        audit_log_ticket_summary.action_date=datetime.datetime.now()
        audit_log_ticket_summary.description=token_count_string    
        audit_log_ticket_summary.summary=True
        self.db_handle.session.add(audit_log_ticket_summary)
        if commit is True:
            self.db_handle.session.commit()

    def start_player_on_machine(self,event_id,tournament_machine,player,tournament=None,commit=False):
        tournament_token_count,meta_tournament_token_count = self.get_available_token_count_for_tournaments(event_id,player)
        if tournament is None:
            tournament = self.get_tournament_by_tournament_id(tournament_machine.tournament_id)            
        if tournament.meta_tournament_id:
            tokens_available = meta_tournament_token_count.get(meta_tournament_id,None) is not None
        else:
            tokens_available = tournament_token_count.get(tournament.tournament_id,None) is not None
        if tokens_available is False:
            return False
        tournament_machine.player_id=player.player_id
        if commit:
            self.db_handle.session.commit()
        return True

    def record_score(self,event_id,player,tournament_machine,score,commit=False):
        new_entry = self.Entries()
        new_score = self.Scores()
        new_score.score=score
        new_score.player_id=player.player_id
        new_score.event_id=event_id        
        new_score.tournament_machine_id=tournament_machine.tournament_machine_id
        new_entry.scores.append(new_score)
        new_entry.tournament_id=tournament_machine.tournament_id
        new_entry.player_id=tournament_machine.player_id
        new_entry.event_id=event_id
        self.db_handle.session.add(new_entry)
        if commit:
            self.db_handle.session.commit()
        
    
    def remove_player_from_machine(self,tournament_machine):
        tournament_machine.player_id=None

    def mark_token_as_used(self,event_id,player,tournament=None,meta_tournament=None,commit=False):
        tournament_id=None
        meta_tournament_id=None
        if tournament.meta_tournament_id:        
            meta_tournament_id=tournament.tournament_id
        else:
            tournament_id=tournament.tournament_id
        token = self.get_tokens_by_tournament_id(player.player_id,tournament_id=tournament_id,meta_tournament_id=meta_tournament_id)[0]
        token.used=True                
        if commit:
            self.db_handle.session.commit()
        return True
    
        
    def void_ticket(self,event_id,player,tournament_machine=None,tournament=None,commit=False):
        tournament_token_count,meta_tournament_token_count = self.get_available_token_count_for_tournaments(event_id,player)
        tournament_id=None
        meta_tournament_id=None
        if tournament is None:
            tournament = self.get_tournament_by_tournament_id(tournament_machine.tournament_id)            
        if tournament.meta_tournament_id:
            tokens_available = meta_tournament_token_count.get(meta_tournament_id,None) is not None
            meta_tournament_id=tournament.meta_tournament_id
        else:
            tokens_available = tournament_token_count.get(tournament.tournament_id,None) is not None
            tournament_id=tournament.tournament_id
        if tokens_available is False:
            return False
        token = self.get_tokens_by_tournament_id(player.player_id,tournament_id=tournament_id,meta_tournament_id=meta_tournament_id)[0]
        token.voided=True                
        if commit:
            self.db_handle.session.commit()
        return True
    
    
