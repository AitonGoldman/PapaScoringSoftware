import unittest
import os
from mock import MagicMock
import td_integration_test_base
import json
from routes import orm_creation
from util import db_util

class RouteEntryTD(td_integration_test_base.TdIntegrationDispatchTestBase):
    def setUp(self):
        super(RouteEntryTD,self).setUp()
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
        self.team_division_machine = orm_creation.create_division_machine(self.flask_app,self.machine,self.team_division)
        
        self.new_team = orm_creation.create_team(self.flask_app,{
            'team_name':'test_team',
            'players':['1','2']
        })

        # add score (player)
        # add score (team)
        
    def test_add_score(self):
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
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            entry_returned = json.loads(rv.data)['data']
            self.assertEquals(entry_returned['score']['score'],1234)

    def test_void_score(self):
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
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            entry_returned = json.loads(rv.data)['data']
            self.assertTrue(entry_returned['voided'])
            token = self.flask_app.tables.Token.query.filter_by(token_id=entry_returned['token_id']).first()
            self.assertTrue(token.voided)
            
    def test_add_bigint_score(self):
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
            rv = c.post('/entry/division_machine/1/score/1123123123123')
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            entry_returned = json.loads(rv.data)['data']
            self.assertEquals(entry_returned['score']['score'],1123123123123)


    def test_add_team_score(self):
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_desk','password':'test_desk'}))
            rv = c.post('/token/paid_for/1',
                        data=json.dumps({"player_id":1,
                                         "team_id":1,
                                         "divisions":{},
                                         "teams":{5:1},
                                         "metadivisions":{}}))                        
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_scorekeeper','password':'test_scorekeeper'}))                    
            rv = c.put('/division/5/division_machine/2/team/1')            
            rv = c.post('/entry/division_machine/2/score/1234')
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            entry_returned = json.loads(rv.data)['data']
            self.assertEquals(entry_returned['score']['score'],1234)

    def test_void_team_token(self):
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_desk','password':'test_desk'}))
            rv = c.post('/token/paid_for/1',
                        data=json.dumps({"player_id":1,
                                         "team_id":1,
                                         "divisions":{},
                                         "teams":{5:1},
                                         "metadivisions":{}}))                        
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_scorekeeper','password':'test_scorekeeper'}))                    
            rv = c.put('/division/5/division_machine/2/team/1')            
            #rv = c.post('/entry/division_machine/2/score/1234')
            rv = c.put('/entry/division_machine/2/void')

            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            entry_returned = json.loads(rv.data)['data']
            self.assertTrue(entry_returned['voided'])
            token = self.flask_app.tables.Token.query.filter_by(token_id=entry_returned['token_id']).first()
            self.assertTrue(token.voided)
            
            
    def test_player_add_score_badauth(self):
        with self.flask_app.test_client() as c:
            self.checkWrongPermissions(c,'post','/entry/division_machine/1/score/1234')            
        with self.flask_app.test_client() as c:
            self.checkWrongPermissions(c,'post','/entry/division_machine/1/score/1234','test_desk')            
        with self.flask_app.test_client() as c:
            self.checkWrongPermissions(c,'post','/entry/division_machine/1/score/1234',pin=self.player_pin)            
        
