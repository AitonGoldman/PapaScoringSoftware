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
        db_util.load_machines_from_json(self.flask_app,True)
        stripe_skus = {
            'A':'sku_8bY4j0VdBxGmPu',
            'B':'sku_8bU4ZwvW1UMtxy',
            'C':'sku_8beFqmlhh0y6Wa',
            'D':'sku_8beJOPdNmnoQgw',
            'Split Flipper':'sku_8cVf2tetzJ4f8D',
            'Classics 1':'sku_8beHMnaBSdH4NA',
            'Classics 2':'sku_9jugzXV5S8oafx',
            'Classics 3':'sku_9juhywxXYAFfW7',
            'Classics Meta':'sku_9wukf1rcx9hWsb'
        }
        discount_stripe_skus = {
            'A':'sku_9wugGsS0eFracR',
            'B':'sku_9wuhUNp2629DGp',
            'C':'sku_9wuigiEVZ61TBJ',            
            'Split Flipper':'sku_9wvPotSYBuA13h',
            'Classics Meta':'sku_9wtQxO4yXCGV9w'            
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
        self.player = orm_creation.create_player(self.flask_app,{'first_name':'test','last_name':'player','ifpa_ranking':'123','linked_division_id':'1'})
        self.player_pin = self.player.pin
        self.player_two = orm_creation.create_player(self.flask_app,{'first_name':'test_two','last_name':'player_two','ifpa_ranking':'321','linked_division_id':'1'})        
        self.player_three = orm_creation.create_player(self.flask_app,{'first_name':'test_three','last_name':'player','ifpa_ranking':'223','linked_division_id':'1'})        
        self.player_four = orm_creation.create_player(self.flask_app,{'first_name':'test_four','last_name':'player','ifpa_ranking':'421','linked_division_id':'1'})        
        orm_creation.create_team(self.flask_app,{'team_name':'test_team','players':['1','2']})
        
        
    def test_setup_before_token(self):        
        pass
