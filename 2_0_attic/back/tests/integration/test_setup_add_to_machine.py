import unittest
import os
from mock import MagicMock
import td_integration_test_base
import json
from routes import orm_creation
from util import db_util
import random

class SetupAddToMachineTD(td_integration_test_base.TdIntegrationSetupTestBase):
    def setUp(self):
        super(SetupAddToMachineTD,self).setUp()
        response,results = self.dispatch_request('/%s/util/healthcheck' % self.poop_db_name)                
        self.flask_app = self.app.instances[self.poop_db_name]
        self.admin_user, self.scorekeeper_user,self.desk_user = orm_creation.create_stanard_roles_and_users(self.flask_app)        
        db_util.load_machines_from_json(self.flask_app,False)
        stripe_skus = {
            'A':'main_a_1',
            'B':'main_b_1',
            'C':'main_c_1',
            'D':'main_d_1',
            'Split Flipper':'split_1',
            'Classics 1':'classics_1',
            'Classics 2':'classics_1',
            'Classics 3':'classics_1',
            'Classics Meta':'classics_1'
        }
        discount_stripe_skus = {
            'A':'main_a_3',
            'B':'main_b_3',
            'C':'main_c_3',            
            'Split Flipper':'split_3',
            'Classics Meta':'classics_3'            
        }
        discount_ticket_counts = {
            'A':3,
            'B':3,
            'C':3,            
            'Split Flipper':3,
            'Classics Meta':3            
        }                
        orm_creation.init_papa_tournaments_divisions(self.flask_app,True,stripe_skus=stripe_skus,discount_stripe_skus=discount_stripe_skus,discount_ticket_counts=discount_ticket_counts)
        orm_creation.init_papa_tournaments_division_machines(self.flask_app)        
        orm_creation.init_papa_players(self.flask_app)
        orm_creation.create_player(self.flask_app,{'first_name':'Doug','last_name':'Polka','ifpa_ranking':'321','linked_division_id':'1'})
        orm_creation.create_player(self.flask_app,{'first_name':'Al','last_name':'Thomka','ifpa_ranking':'321','linked_division_id':'1'})
        orm_creation.create_player(self.flask_app,{'first_name':'Elizabeth','last_name':'Cromwell','ifpa_ranking':'321','linked_division_id':'1'})                                
        orm_creation.create_player(self.flask_app,{'first_name':'Greg','last_name':'Galanter','ifpa_ranking':'321','linked_division_id':'1'})                        
        orm_creation.create_player(self.flask_app,{'first_name':'Josh','last_name':'Sharpe','ifpa_ranking':'321','linked_division_id':'1'})                        
        orm_creation.create_player(self.flask_app,{'first_name':'Mark','last_name':'Steinman','ifpa_ranking':'321','linked_division_id':'1'})
        orm_creation.create_player(self.flask_app,{'first_name':'Amy','last_name':'Covell','ifpa_ranking':'321','linked_division_id':'1'})
        orm_creation.create_player(self.flask_app,{'first_name':'AJ','last_name':'Repolgle','ifpa_ranking':'321','linked_division_id':'1'})                                
        orm_creation.create_player(self.flask_app,{'first_name':'Fred','last_name':'Cochran','ifpa_ranking':'321','linked_division_id':'1'})
        orm_creation.create_player(self.flask_app,{'first_name':'Aiton','last_name':'Goldman','ifpa_ranking':'321','linked_division_id':'1'})                                
        orm_creation.create_player(self.flask_app,{'first_name':'Cassie','last_name':'Stahl','ifpa_ranking':'321','linked_division_id':'1'})                                
        orm_creation.create_player(self.flask_app,{'first_name':'Jon','last_name':'Replgle','ifpa_ranking':'321','linked_division_id':'1'})                                
        
        
    def test_setup_before_token(self):        
        pass
