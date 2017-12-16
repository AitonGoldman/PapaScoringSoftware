import os 
from pss_models_v2.PssUsers import generate_pss_users_class
from pss_models_v2.Events import generate_events_class
from pss_models_v2.EventRoles import generate_event_roles_class
from pss_models_v2.EventRoleMappings import generate_event_role_mappings_class
from pss_models_v2.Tournaments import generate_tournaments_class
from pss_models_v2.MultiDivisionTournaments import generate_multi_division_tournaments_class
from lib_v2 import roles_constants
from lib_v2.serializers import deserializer
#from pss_models_v2.TestMapping import generate_test_class



class TableProxy():
    def initialize_tables(self,db_handle):
        self.db_handle=db_handle                
        self.PssUsers = generate_pss_users_class(self.db_handle)
        self.Events = generate_events_class(self.db_handle)
        self.EventRoles = generate_event_roles_class(self.db_handle)                
        self.EventRoleMappings = generate_event_role_mappings_class(self.db_handle)
        self.Tournaments = generate_tournaments_class(self.db_handle)
        self.MultiDivisionTournaments = generate_multi_division_tournaments_class(db_handle)        

        self.Tournaments.multi_division_tournament = self.db_handle.relationship(
            'MultiDivisionTournaments', uselist=False, cascade='all'
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
    
    def edit_event_user(self,pss_user_id,
                        event_id,input_data):
        pass
    
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
    
    def clear_stripe_prices_from_tournament(self,tournament,commit=False):
        tournament.stripe_price = None
        tournament.stripe_sku = None
        tournament.discount_stripe_price = None
        tournament.discount_stripe_sku = None
        if commit:
            self.db_handle.session.commit()
