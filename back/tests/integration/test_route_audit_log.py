import unittest
import os
from mock import MagicMock
import td_integration_test_base
import json
from routes import orm_creation
from util import db_util

class RouteAuditLogTD(td_integration_test_base.TdIntegrationDispatchTestBase):
    def setUp(self):
        super(RouteAuditLogTD,self).setUp()
        response,results = self.dispatch_request('/%s/util/healthcheck' % self.poop_db_name)                
        self.flask_app = self.app.instances[self.poop_db_name]
        self.admin_user, self.scorekeeper_user,self.desk_user = orm_creation.create_stanard_roles_and_users(self.flask_app)
        #FIXME : password/username should be passed in to create_roles_and_users()
        self.score_user_name_password='test_scorekeeper'
        self.admin_user_name_password='test_admin'        
        db_util.load_machines_from_json(self.flask_app,True)
        orm_creation.init_papa_tournaments_divisions(self.flask_app)        
        self.player = orm_creation.create_player(self.flask_app,{'first_name':'test','last_name':'player','ifpa_ranking':'123','linked_division_id':'1'})
        self.player_pin = self.player.pin
        self.player_two = orm_creation.create_player(self.flask_app,{'first_name':'test','last_name':'player_2','ifpa_ranking':'123','linked_division_id':'1'})        
        self.machine = self.flask_app.tables.Machine.query.filter_by(machine_id=1).first()
        self.division = self.flask_app.tables.Division.query.filter_by(division_id=1).first()
        self.team_division = self.flask_app.tables.Division.query.filter_by(team_tournament=True).first()        
        self.division_machine = orm_creation.create_division_machine(self.flask_app,self.machine,self.division)
        self.division_machines = []
        for division in self.flask_app.tables.Division.query.all():
            self.division_machines.append(orm_creation.create_division_machine(self.flask_app,self.machine,division))
            
        self.team_division_machine = orm_creation.create_division_machine(self.flask_app,self.machine,self.team_division)
        
        # add score (player)
        # add score (team)
        
    def test_audit_log_add_token_division(self):
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user_name_password,'password':self.admin_user_name_password}))
            rv = c.post('/token/paid_for/1',
                        data=json.dumps({"player_id":1,                                     
                                         "divisions":{1:1},
                                         "teams":{},
                                         "metadivisions":{}}))                        
            rv = c.get('/admin/audit_log/where_all_my_tokens_at/player_id/1')
            audit_log = json.loads(rv.data)['data']
            self.assertRegexpMatches(audit_log[0],"Purchased on \d+-\d+-\d+ \d+\:\d+\:\d+\.\d+ -  for division Main, A - sold by test_admin - number purchased : 1, remaining tokens :  Main, A : 1")

    def test_audit_log_add_token_metadivision(self):
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user_name_password,'password':self.admin_user_name_password}))
            rv = c.post('/token/paid_for/1',
                        data=json.dumps({"player_id":1,                                     
                                         "divisions":{},
                                         "teams":{},
                                         "metadivisions":{1:1}}))                        
            rv = c.get('/admin/audit_log/where_all_my_tokens_at/player_id/1')
            audit_log = json.loads(rv.data)['data']
            self.assertRegexpMatches(audit_log[0],"Purchased on \d+-\d+-\d+ \d+\:\d+\:\d+\.\d+ -  for metadivision Classics - sold by test_admin - number purchased : 1, remaining tokens :  Classics : 1")

    def test_audit_log_add_token_team(self):
        self.new_team = orm_creation.create_team(self.flask_app,{
            'team_name':'test_team',
            'players':['1','2']
        })

        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user_name_password,'password':self.admin_user_name_password}))
            rv = c.post('/token/paid_for/1',
                        data=json.dumps({"player_id":1,
                                         "team_id":1,
                                         "divisions":{},
                                         "teams":{5:1},
                                         "metadivisions":{}}))                        
            rv = c.get('/admin/audit_log/where_all_my_tokens_at/player_id/1')
            audit_log = json.loads(rv.data)['data']
            self.assertRegexpMatches(audit_log[0],"Purchased on \d+-\d+-\d+ \d+\:\d+\:\d+\.\d+ -  for division Split Flipper - sold by test_admin - number purchased : 1, remaining tokens :  Split Flipper : 1")

    def test_audit_log_add_multiple_tokens_division(self):
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user_name_password,'password':self.admin_user_name_password}))
            rv = c.post('/token/paid_for/1',
                        data=json.dumps({"player_id":1,                                     
                                         "divisions":{1:5},
                                         "teams":{},
                                         "metadivisions":{}}))                        
            rv = c.get('/admin/audit_log/where_all_my_tokens_at/player_id/1')
            audit_log = json.loads(rv.data)['data']
            self.assertRegexpMatches(audit_log[0],"Purchased on \d+-\d+-\d+ \d+\:\d+\:\d+\.\d+ -  for division Main, A - sold by test_admin - number purchased : 5, remaining tokens :  Main, A : 5")
            #print audit_log
            
    def test_audit_log_add_multiple_tokens_metadivision(self):
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user_name_password,'password':self.admin_user_name_password}))
            rv = c.post('/token/paid_for/1',
                        data=json.dumps({"player_id":1,                                     
                                         "divisions":{},
                                         "teams":{},
                                         "metadivisions":{1:5}}))                        
            rv = c.get('/admin/audit_log/where_all_my_tokens_at/player_id/1')
            audit_log = json.loads(rv.data)['data']
            self.assertRegexpMatches(audit_log[0],"Purchased on \d+-\d+-\d+ \d+\:\d+\:\d+\.\d+ -  for metadivision Classics - sold by test_admin - number purchased : 5, remaining tokens :  Classics : 5")

    def test_audit_log_add_multiple_tokens_team(self):
        self.new_team = orm_creation.create_team(self.flask_app,{
            'team_name':'test_team',
            'players':['1','2']
        })

        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user_name_password,'password':self.admin_user_name_password}))
            rv = c.post('/token/paid_for/1',
                        data=json.dumps({"player_id":1,
                                         "team_id":1,
                                         "divisions":{},
                                         "teams":{5:5},
                                         "metadivisions":{}}))                        
            rv = c.get('/admin/audit_log/where_all_my_tokens_at/player_id/1')
            audit_log = json.loads(rv.data)['data']
            self.assertRegexpMatches(audit_log[0],"Purchased on \d+-\d+-\d+ \d+\:\d+\:\d+\.\d+ -  for division Split Flipper - sold by test_admin - number purchased : 5, remaining tokens :  Split Flipper : 5")

    def test_audit_log_add_multiple_tokens_all(self):
        self.new_team = orm_creation.create_team(self.flask_app,{
            'team_name':'test_team',
            'players':['1','2']
        })

        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user_name_password,'password':self.admin_user_name_password}))
            rv = c.post('/token/paid_for/1',
                        data=json.dumps({"player_id":1,
                                         "team_id":1,
                                         "divisions":{1:5},
                                         "teams":{5:5},
                                         "metadivisions":{1:5}}))                        
            rv = c.get('/admin/audit_log/where_all_my_tokens_at/player_id/1')
            audit_log = json.loads(rv.data)['data']
            self.assertRegexpMatches(audit_log[0],"Purchased on \d+-\d+-\d+ \d+\:\d+\:\d+\.\d+ -  for division Main, A - sold by test_admin - number purchased : 5, remaining tokens :  Main, A : 5 ")
            self.assertRegexpMatches(audit_log[1],"Purchased on \d+-\d+-\d+ \d+\:\d+\:\d+\.\d+ -  for metadivision Classics - sold by test_admin - number purchased : 5, remaining tokens :  Main, A : 5 .  Classics : 5 .")
            self.assertRegexpMatches(audit_log[2],"Purchased on \d+-\d+-\d+ \d+\:\d+\:\d+\.\d+ -  for division Split Flipper - sold by test_admin - number purchased : 5, remaining tokens :  Main, A : 5 .  Split Flipper : 5 .  Classics : 5 .")
            
            
    def test_audit_log_add_to_machine_division(self):
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user_name_password,'password':self.admin_user_name_password}))
            rv = c.post('/token/paid_for/1',
                        data=json.dumps({"player_id":1,                                     
                                         "divisions":{1:1},
                                         "teams":{},
                                         "metadivisions":{}}))                        
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_scorekeeper','password':'test_scorekeeper'}))                    
            rv = c.put('/division/1/division_machine/1/player/1')        
            rv = c.get('/admin/audit_log/where_all_my_tokens_at/player_id/1')            
            audit_log = json.loads(rv.data)['data']
            self.assertRegexpMatches(audit_log[1], "Game started on \d+-\d+-\d+ \d+\:\d+\:\d+\.\d+ - .+ for division Main, A - by test_scorekeeper - remaining tokens :  Main, A : 1")

    def test_audit_log_add_to_machine_metadivision(self):
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user_name_password,'password':self.admin_user_name_password}))
            rv = c.post('/token/paid_for/1',
                        data=json.dumps({"player_id":1,                                     
                                         "divisions":{},
                                         "teams":{},
                                         "metadivisions":{1:1}}))                        
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_scorekeeper','password':'test_scorekeeper'}))
            division_machine = self.flask_app.tables.DivisionMachine.query.filter_by(division_id=6).first()
            rv = c.put('/division/6/division_machine/%s/player/1'%division_machine.division_machine_id)        
            rv = c.get('/admin/audit_log/where_all_my_tokens_at/player_id/1')            
            audit_log = json.loads(rv.data)['data']
            self.assertRegexpMatches(audit_log[1], "Game started on \d+-\d+-\d+ \d+\:\d+\:\d+\.\d+ - .+ for metadivision Classics - by test_scorekeeper - remaining tokens :  Classics : 1")
            

    def test_audit_log_add_to_machine_team(self):
        self.new_team = orm_creation.create_team(self.flask_app,{
            'team_name':'test_team',
            'players':['1','2']
        })

        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user_name_password,'password':self.admin_user_name_password}))
            rv = c.post('/token/paid_for/1',
                        data=json.dumps({"player_id":1,
                                         "team_id":1,
                                         "divisions":{},
                                         "teams":{5:1},
                                         "metadivisions":{}}))                        
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_scorekeeper','password':'test_scorekeeper'}))                    
            division_machine = self.flask_app.tables.DivisionMachine.query.filter_by(division_id=5).first()
            rv = c.put('/division/1/division_machine/%s/team/1'%division_machine.division_machine_id)        
            rv = c.get('/admin/audit_log/where_all_my_tokens_at/player_id/1')            
            audit_log = json.loads(rv.data)['data']
            self.assertRegexpMatches(audit_log[1], "Game started on \d+-\d+-\d+ \d+\:\d+\:\d+\.\d+ - .+ for division Split Flipper - by test_scorekeeper - remaining tokens :  Split Flipper : 1")
            
            
    def test_audit_log_add_score_division(self):
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user_name_password,'password':self.admin_user_name_password}))
            rv = c.post('/token/paid_for/1',
                        data=json.dumps({"player_id":1,                                     
                                         "divisions":{1:1},
                                         "teams":{},
                                         "metadivisions":{}}))                        
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_scorekeeper','password':'test_scorekeeper'}))                    
            rv = c.put('/division/1/division_machine/1/player/1')
            rv = c.post('/entry/division_machine/1/score/1234')
            
            rv = c.get('/admin/audit_log/where_all_my_tokens_at/player_id/1')            
            audit_log = json.loads(rv.data)['data']

            self.assertRegexpMatches(audit_log[2], "Game score \(.+?\) submitted on \d+-\d+-\d+ \d+\:\d+\:\d+\.\d+ - .+ for division Main, A - by test_scorekeeper - remaining tokens : ")
            

    def test_audit_log_add_score_metadivision(self):
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user_name_password,'password':self.admin_user_name_password}))
            rv = c.post('/token/paid_for/1',
                        data=json.dumps({"player_id":1,                                     
                                         "divisions":{},
                                         "teams":{},
                                         "metadivisions":{1:1}}))                        
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_scorekeeper','password':'test_scorekeeper'}))
            division_machine = self.flask_app.tables.DivisionMachine.query.filter_by(division_id=6).first()
            rv = c.put('/division/6/division_machine/%s/player/1'%division_machine.division_machine_id)        
            rv = c.post('/entry/division_machine/%s/score/1234'%division_machine.division_machine_id)
            rv = c.get('/admin/audit_log/where_all_my_tokens_at/player_id/1')            
            audit_log = json.loads(rv.data)['data']
            self.assertRegexpMatches(audit_log[2], "Game score \(.+?\) submitted on \d+-\d+-\d+ \d+\:\d+\:\d+\.\d+ - .+ for metadivision Classics - by test_scorekeeper - remaining tokens : ")
 
            

    def test_audit_log_add_score_team(self):
        self.new_team = orm_creation.create_team(self.flask_app,{
            'team_name':'test_team',
            'players':['1','2']
        })

        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user_name_password,'password':self.admin_user_name_password}))
            rv = c.post('/token/paid_for/1',
                        data=json.dumps({"player_id":1,
                                         "team_id":1,
                                         "divisions":{},
                                         "teams":{5:1},
                                         "metadivisions":{}}))                        
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_scorekeeper','password':'test_scorekeeper'}))                    
            division_machine = self.flask_app.tables.DivisionMachine.query.filter_by(division_id=5).first()
            rv = c.put('/division/1/division_machine/%s/team/1'%division_machine.division_machine_id)
            rv = c.post('/entry/division_machine/%s/score/1234'%division_machine.division_machine_id)            
            rv = c.get('/admin/audit_log/where_all_my_tokens_at/player_id/1')            
            audit_log = json.loads(rv.data)['data']
            self.assertRegexpMatches(audit_log[2], "Game score \(.+?\) submitted on \d+-\d+-\d+ \d+\:\d+\:\d+\.\d+ - .+ for division Split Flipper - by test_scorekeeper - remaining tokens :")


    def test_audit_log_void_division(self):
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user_name_password,'password':self.admin_user_name_password}))
            rv = c.post('/token/paid_for/1',
                        data=json.dumps({"player_id":1,                                     
                                         "divisions":{1:1},
                                         "teams":{},
                                         "metadivisions":{}}))                        
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_scorekeeper','password':'test_scorekeeper'}))                    
            rv = c.put('/division/1/division_machine/1/player/1')
            rv = c.put('/entry/division_machine/1/void')
            
            rv = c.get('/admin/audit_log/where_all_my_tokens_at/player_id/1')            
            audit_log = json.loads(rv.data)['data']

            self.assertRegexpMatches(audit_log[2], "Game voided on \d+-\d+-\d+ \d+\:\d+\:\d+\.\d+ - .+ for division Main, A - by test_scorekeeper - remaining tokens : ")
            

    def test_audit_log_void_metadivision(self):
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user_name_password,'password':self.admin_user_name_password}))
            rv = c.post('/token/paid_for/1',
                        data=json.dumps({"player_id":1,                                     
                                         "divisions":{},
                                         "teams":{},
                                         "metadivisions":{1:1}}))                        
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_scorekeeper','password':'test_scorekeeper'}))
            division_machine = self.flask_app.tables.DivisionMachine.query.filter_by(division_id=6).first()
            rv = c.put('/division/6/division_machine/%s/player/1'%division_machine.division_machine_id)        
            rv = c.put('/entry/division_machine/%s/void'%division_machine.division_machine_id)
            #rv = c.post('/entry/division_machine/%s/score/1234'%division_machine.division_machine_id)
            rv = c.get('/admin/audit_log/where_all_my_tokens_at/player_id/1')            
            audit_log = json.loads(rv.data)['data']
            self.assertRegexpMatches(audit_log[2], "Game voided on \d+-\d+-\d+ \d+\:\d+\:\d+\.\d+ - .+ for metadivision Classics - by test_scorekeeper - remaining tokens : ")
 
            
    def test_audit_log_void_team(self):
        self.new_team = orm_creation.create_team(self.flask_app,{
            'team_name':'test_team',
            'players':['1','2']
        })

        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user_name_password,'password':self.admin_user_name_password}))
            rv = c.post('/token/paid_for/1',
                        data=json.dumps({"player_id":1,
                                         "team_id":1,
                                         "divisions":{},
                                         "teams":{5:1},
                                         "metadivisions":{}}))                        
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_scorekeeper','password':'test_scorekeeper'}))                    
            division_machine = self.flask_app.tables.DivisionMachine.query.filter_by(division_id=5).first()
            rv = c.put('/division/5/division_machine/%s/team/1'%division_machine.division_machine_id)
            #rv = c.post('/entry/division_machine/%s/score/1234'%division_machine.division_machine_id)            
            rv = c.put('/entry/division_machine/%s/void'%division_machine.division_machine_id)            
            rv = c.get('/admin/audit_log/where_all_my_tokens_at/player_id/1')            
            audit_log = json.loads(rv.data)['data']
            self.assertRegexpMatches(audit_log[2], "Game voided on \d+-\d+-\d+ \d+\:\d+\:\d+\.\d+ - .+ for division Split Flipper - by test_scorekeeper - remaining tokens :")
            
            
