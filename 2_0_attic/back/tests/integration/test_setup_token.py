import unittest
import os
from mock import MagicMock
import td_integration_test_base
import json
from routes import orm_creation
from util import db_util
import random
import time


class SetupTokenTD(td_integration_test_base.TdIntegrationSetupTestBase):
    def check_request_success(self,action,rv):
        if rv.status != "200 OK":
            print rv.status
            print "could not %s\n %s"%(action,rv.data)
        
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
        #self.player = orm_creation.create_player(self.flask_app,{'first_name':'test','last_name':'player','ifpa_ranking':'123','linked_division_id':'1'})
        #self.player_pin = self.player.pin
        orm_creation.init_papa_players(self.flask_app)        
        orm_creation.create_team(self.flask_app,{'team_name':'test_team_1','players':[1,2]})
        orm_creation.create_team(self.flask_app,{'team_name':'test_team_2','players':[3,4]})
        orm_creation.create_team(self.flask_app,{'team_name':'test_team_3','players':[5,6]})
        
    def test_setup_before_token(self):        
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_admin','password':'test_admin'}))
            division_machines = {}
            division_machines[1] = self.flask_app.tables.DivisionMachine.query.filter_by(division_id=1).order_by(self.flask_app.tables.DivisionMachine.division_id.desc()).all()                
            division_machines[2] = self.flask_app.tables.DivisionMachine.query.filter_by(division_id=2).order_by(self.flask_app.tables.DivisionMachine.division_id.desc()).all()                
            division_machines[3] = self.flask_app.tables.DivisionMachine.query.filter_by(division_id=3).order_by(self.flask_app.tables.DivisionMachine.division_id.desc()).all()                
            division_machines[4] = self.flask_app.tables.DivisionMachine.query.filter_by(division_id=4).order_by(self.flask_app.tables.DivisionMachine.division_id.desc()).all()                
            division_machines[5] = self.flask_app.tables.DivisionMachine.query.filter_by(division_id=5).order_by(self.flask_app.tables.DivisionMachine.division_id.desc()).all()                
            division_machines[6] = self.flask_app.tables.DivisionMachine.query.filter_by(division_id=6).order_by(self.flask_app.tables.DivisionMachine.division_id.desc()).all()                
            division_machines[7] = self.flask_app.tables.DivisionMachine.query.filter_by(division_id=7).order_by(self.flask_app.tables.DivisionMachine.division_id.desc()).all()                
            division_machines[8] = self.flask_app.tables.DivisionMachine.query.filter_by(division_id=8).order_by(self.flask_app.tables.DivisionMachine.division_id.desc()).all()                
            
            for player_num in range(1,100):
                print "Starting on player %s"% player_num
                num_entries=1
                tokens = {"player_id":player_num,                                        
                          "divisions":{1:[15,1],
                                       2:[0,1],
                                       3:[0,1],
                                       4:[0,1]},                          
                          "metadivisions":{1:[5,1]}}
                if player_num in[1,3,5]:
                    tokens["teams"]={5:[5,1]}
                else:
                    tokens["teams"]={5:[0,0]}
                rv = c.post('/token/paid_for/1',
                            data=json.dumps(tokens))
                self.check_request_success("buy tickets",rv)
                while num_entries < 2:                    
                    if player_num<100:
                        for division_machine in division_machines[1][0:]:                        
                            division_machine_id = division_machine.division_machine_id
                            rv = c.put('/division/1/division_machine/%s/player/%s'%(division_machine_id,player_num))
                            self.check_request_success("add player to machine",rv)
                            rv = c.post('/entry/division_machine/%s/score/%s'% (division_machine_id,random.randrange(999999)))
                            self.check_request_success("record score",rv)
                             
                    # if player_num>=100 and player_num < 200:
                    #     for division_machine in division_machines[2]:                        
                    #         division_machine_id = division_machine.division_machine_id
                    #         rv = c.put('/division/2/division_machine/%s/player/%s'%(division_machine_id,player_num))
                    #         self.check_request_success("add player to machine",rv)

                    #         rv = c.post('/entry/division_machine/%s/score/%s'% (division_machine_id,random.randrange(999999)))
                    #         self.check_request_success("record score",rv)

                    # if player_num>=200 and player_num < 300:
                    #     for division_machine in division_machines[3]:                        
                    #         division_machine_id = division_machine.division_machine_id
                    #         rv = c.put('/division/3/division_machine/%s/player/%s'%(division_machine_id,player_num))
                    #         self.check_request_success("add player to machine",rv)

                    #         rv = c.post('/entry/division_machine/%s/score/%s'% (division_machine_id,random.randrange(999999)))
                    #         self.check_request_success("record score",rv)


                    # if player_num>=300 and player_num < 400:
                    #     for division_machine in division_machines[4]:                        
                    #         division_machine_id = division_machine.division_machine_id
                    #         rv = c.put('/division/4/division_machine/%s/player/%s'%(division_machine_id,player_num))
                    #         self.check_request_success("add player to machine",rv)

                    #         rv = c.post('/entry/division_machine/%s/score/%s'% (division_machine_id,random.randrange(999999)))
                    #         self.check_request_success("record score",rv)

                        
                    # if player_num < 100:
                    #     for division_machine in division_machines[6]:
                    #         division_machine_id = division_machine.division_machine_id
                    #         rv = c.put('/division/6/division_machine/%s/player/%s'%(division_machine_id,player_num))
                    #         self.check_request_success("add player to machine",rv)

                    #         rv = c.post('/entry/division_machine/%s/score/%s'% (division_machine_id,random.randrange(3456789123456)))
                    #     for division_machine in division_machines[7]:
                    #         division_machine_id = division_machine.division_machine_id
                    #         rv = c.put('/division/7/division_machine/%s/player/%s'%(division_machine_id,player_num))
                    #         self.check_request_success("add player to machine",rv)

                    #         rv = c.post('/entry/division_machine/%s/score/%s'% (division_machine_id,random.randrange(999999)))
                    #         self.check_request_success("record score",rv)

                    #     for division_machine in division_machines[8]:
                    #         division_machine_id = division_machine.division_machine_id
                    #         rv = c.put('/division/8/division_machine/%s/player/%s'%(division_machine_id,player_num))
                    #         self.check_request_success("add player to machine",rv)

                    #         rv = c.post('/entry/division_machine/%s/score/%s'% (division_machine_id,random.randrange(999999)))
                        
                    # if player_num < 100:
                    #     team_id = self.flask_app.tables.Player.query.filter_by(player_id=player_num).first().teams[0].team_id
                    #     for division_machine in division_machines[5]:                        
                    #         division_machine_id = division_machine.division_machine_id
                    #         rv = c.put('/division/5/division_machine/%s/team/%s'%(division_machine_id,
                    #                                                                 team_id))                            
                    #         self.check_request_success("add team to machine",rv)

                    #         rv = c.post('/entry/division_machine/%s/score/%s'% (division_machine_id,
                    #                                                             random.randrange(999999)))
                    #         self.check_request_success("record score for team",rv)

                    
                    num_entries = num_entries + 1
            
