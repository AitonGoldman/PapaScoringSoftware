import unittest
import os
from mock import MagicMock
import td_integration_test_base
import json
from routes import orm_creation
from util import db_util

class RouteTokenTD(td_integration_test_base.TdIntegrationDispatchTestBase):
    def setUp(self):
        super(RouteTokenTD,self).setUp()
        response,results = self.dispatch_request('/%s/util/healthcheck' % self.poop_db_name)                
        self.flask_app = self.app.instances[self.poop_db_name]
        self.admin_user, self.scorekeeper_user,self.desk_user = orm_creation.create_stanard_roles_and_users(self.flask_app)

        db_util.load_machines_from_json(self.flask_app,True)
        orm_creation.init_papa_tournaments_divisions(self.flask_app)
        self.player = orm_creation.create_player(self.flask_app,{'first_name':'test','last_name':'player','ifpa_ranking':'123','linked_division_id':'1'})
        self.player_pin = self.player.pin
        self.player_two = orm_creation.create_player(self.flask_app,{'first_name':'test_two','last_name':'player_two','ifpa_ranking':'321','linked_division_id':'1'})        
        orm_creation.create_team(self.flask_app,{'team_name':'test_team','players':['1','2']})

    def test_add_token(self):        
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_desk','password':'test_desk'}))
            rv = c.post('/token/paid_for/1',
                       data=json.dumps({"player_id":1,
                                        "team_id":1,
                                        "divisions":{1:1},
                                        "teams":{5:1},
                                        "metadivisions":{1:1}}))
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            tokens = json.loads(rv.data)['data']                        
            #for type_of_token in ["divisions","metadivisions","teams"]
            self.assertEquals(tokens['divisions']['1'],1)
            self.assertEquals(tokens['metadivisions']['1'],1)
            self.assertEquals(tokens['divisions']['5'],1)
            new_division_tokens_count = len(self.flask_app.tables.Token.query.filter_by(division_id=1).all())
            new_teams_tokens_count = len(self.flask_app.tables.Token.query.filter_by(division_id=5).all())            
            new_metadivision_tokens_count = len(self.flask_app.tables.Token.query.filter_by(metadivision_id=1).all())
            self.assertEquals(new_division_tokens_count,1)
            self.assertEquals(new_teams_tokens_count,1)
            self.assertEquals(new_metadivision_tokens_count,1)
            
    def test_add_normal_division_token(self):        
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_desk','password':'test_desk'}))
            rv = c.post('/token/paid_for/1',
                       data=json.dumps({"player_id":1,                                        
                                        "divisions":{1:1},
                                        "teams":{},
                                        "metadivisions":{}}))
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            tokens = json.loads(rv.data)['data']                                    
            self.assertEquals(tokens['divisions']['1'],1)
            new_division_tokens_count = len(self.flask_app.tables.Token.query.filter_by(division_id=1).all())
            new_teams_tokens_count = len(self.flask_app.tables.Token.query.filter_by(division_id=5).all())            
            new_metadivision_tokens_count = len(self.flask_app.tables.Token.query.filter_by(metadivision_id=1).all())
            self.assertEquals(new_division_tokens_count,1)
            self.assertEquals(new_teams_tokens_count,0)
            self.assertEquals(new_metadivision_tokens_count,0)

    def test_add_normal_division_token_past_limit(self):        
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_desk','password':'test_desk'}))
            rv = c.post('/token/paid_for/1',
                       data=json.dumps({"player_id":1,                                        
                                        "divisions":{1:2},
                                        "teams":{},
                                        "metadivisions":{}}))
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            tokens = json.loads(rv.data)['data']                                    
            self.assertEquals(tokens['divisions']['1'],2)
            #self.assertEquals(len(tokens),2)
            rv = c.post('/token/paid_for/1',
                       data=json.dumps({"player_id":1,                                        
                                        "divisions":{1:4},
                                        "teams":{},
                                        "metadivisions":{}}))
            self.assertEquals(rv.status_code,
                              409,
                              'Was expecting status code 409, but it was %s : %s' % (rv.status_code,rv.data))
            new_division_tokens_count = len(self.flask_app.tables.Token.query.filter_by(division_id=1).all())
            self.assertEquals(new_division_tokens_count,2)


            
    def test_add_team_division_token_past_limit(self):        
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_desk','password':'test_desk'}))
            rv = c.post('/token/paid_for/1',
                       data=json.dumps({"player_id":1,
                                        "team_id":"1",
                                        "divisions":{},
                                        "teams":{'5':'2'},
                                        "metadivisions":{}}))
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            tokens = json.loads(rv.data)['data']                                    
            #self.assertEquals(len(tokens),2)
            self.assertEquals(tokens['divisions']['5'],2)            
            rv = c.post('/token/paid_for/1',
                       data=json.dumps({"player_id":1,
                                        "team_id":"1",
                                        "divisions":{},
                                        "teams":{'5':'4'},
                                        "metadivisions":{}}))
            self.assertEquals(rv.status_code,
                              409,
                              'Was expecting status code 409, but it was %s : %s' % (rv.status_code,rv.data))
            new_teams_tokens_count = len(self.flask_app.tables.Token.query.filter_by(division_id=5).all())            
            self.assertEquals(new_teams_tokens_count,2)


    def test_add_meta_division_token_past_limit(self):        
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_desk','password':'test_desk'}))
            rv = c.post('/token/paid_for/1',
                       data=json.dumps({"player_id":1,                                        
                                        "divisions":{},
                                        "teams":{},
                                        "metadivisions":{"1":"2"}}))
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            tokens = json.loads(rv.data)['data']                                    
            #self.assertEquals(len(tokens),2)
            self.assertEquals(tokens['metadivisions']['1'],2)
            rv = c.post('/token/paid_for/1',
                       data=json.dumps({"player_id":1,                                        
                                        "divisions":{},
                                        "teams":{},
                                        "metadivisions":{"1":"4"}}))
            self.assertEquals(rv.status_code,
                              409,
                              'Was expecting status code 409, but it was %s : %s' % (rv.status_code,rv.data))
            new_metadivisions_tokens_count = len(self.flask_app.tables.Token.query.filter_by(metadivision_id=1).all())            
            self.assertEquals(new_metadivisions_tokens_count,2)
            
    def test_add_team_division_token(self):        
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_desk','password':'test_desk'}))
            rv = c.post('/token/paid_for/1',
                       data=json.dumps({"player_id":1,
                                        "team_id":1,
                                        "divisions":{},
                                        "teams":{'5':'1'},
                                        "metadivisions":{}}))
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            tokens = json.loads(rv.data)['data']                                    
            self.assertEquals(tokens['divisions']['5'],1)
            new_division_tokens_count = len(self.flask_app.tables.Token.query.filter_by(division_id=1).all())
            new_teams_tokens_count = len(self.flask_app.tables.Token.query.filter_by(division_id=5).all())            
            new_metadivision_tokens_count = len(self.flask_app.tables.Token.query.filter_by(metadivision_id=1).all())
            self.assertEquals(new_division_tokens_count,0)
            self.assertEquals(new_teams_tokens_count,1)
            self.assertEquals(new_metadivision_tokens_count,0)

    def test_add_meta_division_token(self):        
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_desk','password':'test_desk'}))
            rv = c.post('/token/paid_for/1',
                       data=json.dumps({"player_id":1,                                        
                                        "divisions":{},
                                        "teams":{},
                                        "metadivisions":{'1':'1'}}))
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            tokens = json.loads(rv.data)['data']                                    
            self.assertEquals(tokens['metadivisions']['1'],1)
            new_division_tokens_count = len(self.flask_app.tables.Token.query.filter_by(division_id=1).all())
            new_teams_tokens_count = len(self.flask_app.tables.Token.query.filter_by(division_id=5).all())            
            new_metadivision_tokens_count = len(self.flask_app.tables.Token.query.filter_by(metadivision_id=1).all())
            self.assertEquals(new_division_tokens_count,0)
            self.assertEquals(new_teams_tokens_count,0)
            self.assertEquals(new_metadivision_tokens_count,1)

    def test_player_add_score_badauth(self):
        with self.flask_app.test_client() as c:
            self.checkWrongPermissions(c,'post','/token/paid_for/1')            
        with self.flask_app.test_client() as c:
            self.checkWrongPermissions(c,'post','/token/paid_for/1','test_scorekeeper')            
        with self.flask_app.test_client() as c:
            self.checkWrongPermissions(c,'post','/token/paid_for/1',pin=self.player_pin)                                    

    def test_add_zero_division_token(self):        
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_desk','password':'test_desk'}))
            rv = c.post('/token/paid_for/1',
                       data=json.dumps({"player_id":'1',
                                        "team_id":'1',
                                        "divisions":{'1':'0'},
                                        "teams":{'5':'0'},
                                        "metadivisions":{'1':'0'}}))
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            tokens = json.loads(rv.data)['data']                                    
            self.assertEquals(tokens['divisions']['1'],0)
            self.assertEquals(tokens['divisions']['5'],0)
            self.assertEquals(tokens['metadivisions']['1'],0)            
            new_division_tokens_count = len(self.flask_app.tables.Token.query.filter_by(division_id=1).all())
            new_teams_tokens_count = len(self.flask_app.tables.Token.query.filter_by(division_id=5).all())            
            new_metadivision_tokens_count = len(self.flask_app.tables.Token.query.filter_by(metadivision_id=1).all())
            self.assertEquals(new_division_tokens_count,0)
            self.assertEquals(new_teams_tokens_count,0)
            self.assertEquals(new_metadivision_tokens_count,0)
            

    def test_add_both_team_members_division_token(self):        
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_desk','password':'test_desk'}))
            rv = c.post('/token/paid_for/1',
                       data=json.dumps({"player_id":1,
                                        "team_id":1,
                                        "divisions":{},
                                        "teams":{'5':'1'},
                                        "metadivisions":{}}))
            rv = c.post('/token/paid_for/1',
                       data=json.dumps({"player_id":2,
                                        "team_id":1,
                                        "divisions":{},
                                        "teams":{'5':'5'},
                                        "metadivisions":{}}))            
            self.assertEquals(rv.status_code,
                              409,
                              'Was expecting status code 409, but it was %s : %s' % (rv.status_code,rv.data))
            new_tokens = self.flask_app.tables.Token.query.filter_by(team_id=1).all()
            self.assertEquals(len(new_tokens),1)
            rv = c.post('/token/paid_for/1',
                       data=json.dumps({"player_id":2,
                                        "team_id":1,
                                        "divisions":{},
                                        "teams":{'5':'4'},
                                        "metadivisions":{}}))            
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            tokens = json.loads(rv.data)['data']                                                
            self.assertEquals(tokens['divisions']['5'],4)
            new_tokens = self.flask_app.tables.Token.query.filter_by(team_id=1).all()
            self.assertEquals(len(new_tokens),5)

            rv = c.post('/token/paid_for/1',
                       data=json.dumps({"player_id":1,
                                        "team_id":1,
                                        "divisions":{},
                                        "teams":{'5':'1'},
                                        "metadivisions":{}}))            
            self.assertEquals(rv.status_code,
                              409,
                              'Was expecting status code 409, but it was %s : %s' % (rv.status_code,rv.data))
            
    def test_get_tokens_for_player(self):        
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_desk','password':'test_desk'}))
            rv = c.get('/token/player_id/1')            
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            tokens = json.loads(rv.data)['data']                        
            self.assertEquals(tokens['tokens']['divisions']['1'],0)
            self.assertEquals(tokens['tokens']['metadivisions']['1'],0)
            self.assertEquals(tokens['tokens']['teams']['5'],0)
            self.assertEquals(tokens['available_tokens']['divisions']['1'],5)
            self.assertEquals(tokens['available_tokens']['metadivisions']['1'],5)
            self.assertEquals(tokens['available_tokens']['teams']['5'],5)
            
            rv = c.post('/token/paid_for/1',
                       data=json.dumps({"player_id":1,
                                        "team_id":1,
                                        "divisions":{1:1},
                                        "teams":{5:1},
                                        "metadivisions":{1:1}}))
            rv = c.get('/token/player_id/1')            
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            tokens = json.loads(rv.data)['data']                        
            self.assertEquals(tokens['tokens']['divisions']['1'],1)
            self.assertEquals(tokens['tokens']['metadivisions']['1'],1)
            self.assertEquals(tokens['tokens']['teams']['5'],1)
            self.assertEquals(tokens['available_tokens']['divisions']['1'],4)
            self.assertEquals(tokens['available_tokens']['metadivisions']['1'],4)
            self.assertEquals(tokens['available_tokens']['teams']['5'],4)
