import random
import os 
from pss_models_v2.PssUsers import generate_pss_users_class
from pss_models_v2.Players import generate_players_class
from pss_models_v2.Events import generate_events_class
from pss_models_v2.EventRoles import generate_event_roles_class
from pss_models_v2.EventRoleMappings import generate_event_role_mappings_class
from pss_models_v2.EventPlayersRoleMappings import generate_event_player_role_mappings_class

from pss_models_v2.Tournaments import generate_tournaments_class
from pss_models_v2.Machines import generate_machines_class
from pss_models_v2.TournamentMachines import generate_tournament_machines_class
from pss_models_v2.MultiDivisionTournaments import generate_multi_division_tournaments_class
from lib_v2 import roles_constants
from lib_v2.serializers import deserializer
#from pss_models_v2.TestMapping import generate_test_class



class TableProxy():
    def initialize_tables(self,db_handle):
        self.db_handle=db_handle                
        self.PssUsers = generate_pss_users_class(self.db_handle)
        self.Players = generate_players_class(self.db_handle)
        self.Events = generate_events_class(self.db_handle)
        self.EventRoles = generate_event_roles_class(self.db_handle)                
        self.EventRoleMappings = generate_event_role_mappings_class(self.db_handle)
        self.EventPlayerRoleMappings = generate_event_player_role_mappings_class(self.db_handle)
        self.Tournaments = generate_tournaments_class(self.db_handle)
        self.MultiDivisionTournaments = generate_multi_division_tournaments_class(db_handle)        
        self.Machines = generate_machines_class(db_handle)        
        self.TournamentMachines = generate_tournament_machines_class(db_handle)        

        self.Tournaments.multi_division_tournament = self.db_handle.relationship(
            'MultiDivisionTournaments', uselist=False, cascade='all'
        )

        self.Players.event_roles = self.db_handle.relationship(
            'EventPlayerRoleMappings', cascade='all'
        )
        
        self.PssUsers.event_roles = self.db_handle.relationship(
            'EventRoleMappings', cascade='all'
        )
        
        self.PssUsers.events_created = self.db_handle.relationship(
            'Events', cascade='all'            
        )
    def commit_changes(self):
        self.db_handle.session.commit()
        
    def get_user_by_username(self,username):
        #return self.PssUsers.query.options(joinedload("admin_roles"),joinedload("event_roles"),joinedload("events"),joinedload("event_user")).filter_by(username=input_data['username']).first()
        return self.PssUsers.query.filter_by(username=username).first()

    def get_user_by_id(self,id):
        #return self.PssUsers.query.options(joinedload("admin_roles"),joinedload("event_roles"),joinedload("events"),joinedload("event_user")).filter_by(username=input_data['username']).first()
        return self.PssUsers.query.filter_by(pss_user_id=id).first()
    
    def get_event_by_eventname(self,eventname):
        return self.Events.query.filter_by(name=eventname).first()            

    def get_event_by_event_id(self,event_id):
        return self.Events.query.filter_by(event_id=event_id).first()            
    
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
        event_player_role_mapping = self.EventPlayerRoleMappings()
        event_player_role_mapping.event_id=event_id
        event_player_role_mapping.player_id=player.player_id        
        if ifpa_ranking:
            event_player_role_mapping.ifpa_ranking=ifpa_ranking
        if selected_division_in_multi_division_tournament:
            event_player_role_mapping.selected_division_in_multi_division_tournament=selected_division_in_multi_division_tournament
        existing_player_ids_for_event = sorted([player_event_info.player_id_for_event for player_event_info in self.EventPlayerRoleMappings.query.filter_by(event_id=event_id).all()],reverse=True)
        if len(existing_player_ids_for_event)==0:
            event_player_role_mapping.player_id_for_event=100
        else:
            event_player_role_mapping.player_id_for_event=existing_player_ids_for_event[0]+1                
        player.event_roles.append(event_player_role_mapping)        
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

    def get_player_by_id(self,player_id):
        return self.Players.query.filter_by(player_id=player_id).first()            

    def get_player_by_player_id_for_event(self,player_id_for_event,event_id):
        return self.Players.query.join(self.EventPlayerRoleMappings).filter_by(event_id=event_id,player_id_for_event=player_id_for_event).first()
        
    def get_players_by_name(self,first_name,last_name,extra_title=None):
        query = self.Players.query.filter_by(first_name=first_name,last_name=last_name)
        if extra_title:
            query = query.filter_by(extra_title=extra_title)
        return query.all()

    #def get_players_for_event(self,event_id):
    #    return self.EventPlayerRoleMappings.query.filter_by(event_id=event_id).all()        
    
    def get_tournament_by_tournament_id(self,tournament_id):
        return self.Tournaments.query.filter_by(tournament_id=tournament_id).first()            

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
        if event is None:
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
        new_tournament_machine.tournament_id=tournament.tournament_id
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
    
