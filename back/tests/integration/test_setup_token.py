import unittest
import os
from mock import MagicMock
import td_integration_test_base
import json
from routes import orm_creation
from util import db_util
import random

class SetupTokenTD(td_integration_test_base.TdIntegrationSetupTestBase):
    def setUp(self):
        super(SetupTokenTD,self).setUp()
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
            'Classics 3':'sku_9juhywxXYAFfW7'
        }
        orm_creation.init_papa_tournaments_divisions(self.flask_app,True,stripe_skus)
        orm_creation.init_papa_tournaments_division_machines(self.flask_app)        
        self.player = orm_creation.create_player(self.flask_app,{'first_name':'test','last_name':'player','ifpa_ranking':'123','linked_division_id':'1'})
        self.player_pin = self.player.pin
        for player_num in range(150):
            orm_creation.create_player(self.flask_app,{'first_name':'test_%s'%player_num,'last_name':'player_%s'%player_num,'ifpa_ranking':random.randrange(999),'linked_division_id':'1'})        
        #self.player_three = orm_creation.create_player(self.flask_app,{'first_name':'test_three','last_name':'player','ifpa_ranking':'223','linked_division_id':'1'})        
        #self.player_four = orm_creation.create_player(self.flask_app,{'first_name':'test_four','last_name':'player','ifpa_ranking':'421','linked_division_id':'1'})
        for team_num in range(1,150,2):
            orm_creation.create_team(self.flask_app,{'team_name':'test_team_%s'%team_num,'players':[team_num,team_num+1]})

    def test_setup_before_token(self):        
        num_entries = 0
        # 8 divisions
        # 150 players
        # 30000 herb entries
        # 3750 entries per division
        # 12 machines per division -> 312 entries per machine
        # 2 per player per machine
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_admin','password':'test_admin'}))                       
            for player_num in range(1,100):
                num_entries=1
                rv = c.post('/token/paid_for/1',
                            data=json.dumps({"player_id":player_num,                                        
                                             "divisions":{1:10},
                                             "teams":{5:3},
                                             "metadivisions":{1:10}}))
                print "getting tickets for player %s"%player_num
                print rv.status
                
                while num_entries < 2:
                    print "num_entries is %s"% num_entries                                                    
                    division_machines = self.flask_app.tables.DivisionMachine.query.filter_by(division_id=1).all()
                    for division_machine_idx in range(10):
                        division_machine_id = division_machines[division_machine_idx].division_machine_id
                        rv = c.put('/division/1/division_machine/%s/player/%s'%(division_machine_id,player_num))                                        
                        rv = c.post('/entry/division_machine/%s/score/%s'% (division_machine_id,random.randrange(999999)))
                    division_machines = self.flask_app.tables.DivisionMachine.query.filter_by(division_id=6).all()
                    for division_machine_idx in range(10):
                        division_machine_id = division_machines[division_machine_idx].division_machine_id
                        rv = c.put('/division/6/division_machine/%s/player/%s'%(division_machine_id,player_num))                                        
                        rv = c.post('/entry/division_machine/%s/score/%s'% (division_machine_id,random.randrange(999999)))
                    team_id = self.flask_app.tables.Player.query.filter_by(player_id=player_num).first().teams[0].team_id
                    division_machines = self.flask_app.tables.DivisionMachine.query.filter_by(division_id=5).all()
                    for division_machine_idx in range(10):
                        division_machine_id = division_machines[division_machine_idx].division_machine_id
                        rv = c.put('/division/5/division_machine/%s/team/%s'%(division_machine_id,team_id))
                        rv = c.post('/entry/division_machine/%s/score/%s'% (division_machine_id,random.randrange(999999)))
                    
                    num_entries = num_entries + 1
            
