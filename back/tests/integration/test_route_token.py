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
        orm_creation.create_roles(self.flask_app)
        orm_creation.create_user(self.flask_app,'test_admin','test_admin',['1','2','3','4','6'])
        orm_creation.create_user(self.flask_app,'test_desk','test_desk',['6'])
        orm_creation.create_user(self.flask_app,'test_score','test_score',['3','4'])
        db_util.load_machines_from_json(self.flask_app,True)
        db_util.init_papa_tournaments_divisions(self.flask_app.tables)
        self.player = orm_creation.create_player(self.flask_app,{'first_name':'test','last_name':'player','ifpa_ranking':'123','linked_division_id':'1'})
        self.player_two = orm_creation.create_player(self.flask_app,{'first_name':'test_two','last_name':'player_two','ifpa_ranking':'321','linked_division_id':'1'})        
        orm_creation.create_team(self.flask_app,{'team_name':'test_team','players':['1','2']})

    # use cases :                
    # check that team tickets bought by other team member is respected for limits
    
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
            self.assertEquals(len(tokens),3)
            normal_division_token = [token for token in tokens if token['division_id'] == 1]
            team_division_token = [token for token in tokens if token['division_id'] == 5]
            meta_division_token = [token for token in tokens if token['metadivision_id'] == 1]
            self.assertEquals(len(normal_division_token),1)
            self.assertEquals(len(team_division_token),1)
            self.assertEquals(len(meta_division_token),1)
            for div in [normal_division_token,team_division_token,meta_division_token]:
                self.assertEquals(div[0]['used'],False)
                self.assertEquals(div[0]['comped'],False)
                self.assertEquals(div[0]['used_date'],None)
                self.assertEquals(div[0]['scorekeeper_id'],None)
                self.assertEquals(div[0]['game_started_date'],None)            
                self.assertIsNotNone(div[0]['purchase_date'])
                self.assertEquals(div[0]['paid_for'],True)
                self.assertEquals(div[0]['deskworker_id'],2)                
                
            self.assertEquals(normal_division_token[0]['player_id'],1)
            self.assertEquals(normal_division_token[0]['metadivision_id'],None)
            self.assertEquals(normal_division_token[0]['team_id'],None)            

            self.assertEquals(meta_division_token[0]['player_id'],1)
            self.assertEquals(meta_division_token[0]['metadivision_id'],1)
            self.assertEquals(meta_division_token[0]['team_id'],None)
            
            self.assertEquals(team_division_token[0]['team_id'],1)
            self.assertEquals(normal_division_token[0]['metadivision_id'],None)
            new_tokens = self.flask_app.tables.Token.query.all()
            self.assertEquals(len(new_tokens),3)

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
            self.assertEquals(len(tokens),1)
            normal_division_token = [token for token in tokens if token['division_id'] == 1]
            team_division_token = [token for token in tokens if token['division_id'] == 5]
            meta_division_token = [token for token in tokens if token['metadivision_id'] == 1]
            self.assertEquals(len(normal_division_token),1)
            self.assertEquals(len(team_division_token),0)
            self.assertEquals(len(meta_division_token),0)

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
            self.assertEquals(len(tokens),2)
            rv = c.post('/token/paid_for/1',
                       data=json.dumps({"player_id":1,                                        
                                        "divisions":{1:4},
                                        "teams":{},
                                        "metadivisions":{}}))
            self.assertEquals(rv.status_code,
                              409,
                              'Was expecting status code 409, but it was %s : %s' % (rv.status_code,rv.data))
            new_tokens = self.flask_app.tables.Token.query.all()
            self.assertEquals(len(new_tokens),2)

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
            self.assertEquals(len(tokens),2)
            rv = c.post('/token/paid_for/1',
                       data=json.dumps({"player_id":1,
                                        "team_id":"1",
                                        "divisions":{},
                                        "teams":{'5':'4'},
                                        "metadivisions":{}}))
            self.assertEquals(rv.status_code,
                              409,
                              'Was expecting status code 409, but it was %s : %s' % (rv.status_code,rv.data))
            new_tokens = self.flask_app.tables.Token.query.all()
            self.assertEquals(len(new_tokens),2)

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
            self.assertEquals(len(tokens),2)
            rv = c.post('/token/paid_for/1',
                       data=json.dumps({"player_id":1,                                        
                                        "divisions":{},
                                        "teams":{},
                                        "metadivisions":{"1":"4"}}))
            self.assertEquals(rv.status_code,
                              409,
                              'Was expecting status code 409, but it was %s : %s' % (rv.status_code,rv.data))
            new_tokens = self.flask_app.tables.Token.query.all()
            self.assertEquals(len(new_tokens),2)
            
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
            self.assertEquals(len(tokens),1)
            normal_division_token = [token for token in tokens if token['division_id'] == 1]
            team_division_token = [token for token in tokens if token['division_id'] == 5]
            meta_division_token = [token for token in tokens if token['metadivision_id'] == 1]
            self.assertEquals(len(normal_division_token),0)
            self.assertEquals(len(team_division_token),1)
            self.assertEquals(len(meta_division_token),0)

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
            self.assertEquals(len(tokens),1)
            normal_division_token = [token for token in tokens if token['division_id'] == 1]
            team_division_token = [token for token in tokens if token['division_id'] == 5]
            meta_division_token = [token for token in tokens if token['metadivision_id'] == 1]
            self.assertEquals(len(normal_division_token),0)
            self.assertEquals(len(team_division_token),0)
            self.assertEquals(len(meta_division_token),1)

    def test_add_division_token_no_auth(self):        
        with self.flask_app.test_client() as c:                    
            rv = c.post('/token/paid_for/1',
                       data=json.dumps({"player_id":1,                                        
                                        "divisions":{},
                                        "teams":{},
                                        "metadivisions":{'1':'1'}}))
            self.assertEquals(rv.status_code,
                              401,
                              'Was expecting status code 401, but it was %s : %s' % (rv.status_code,rv.data))
            

    def test_add_division_token_wront_auth(self):        
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_score','password':'test_score'}))
            rv = c.post('/token/paid_for/1',
                       data=json.dumps({"player_id":1,                                        
                                        "divisions":{},
                                        "teams":{},
                                        "metadivisions":{'1':'1'}}))
            self.assertEquals(rv.status_code,
                              403,
                              'Was expecting status code 403, but it was %s : %s' % (rv.status_code,rv.data))
            

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
            self.assertEquals(len(tokens),0)
            

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
            self.assertEquals(len(tokens),4)
            rv = c.post('/token/paid_for/1',
                       data=json.dumps({"player_id":1,
                                        "team_id":1,
                                        "divisions":{},
                                        "teams":{'5':'1'},
                                        "metadivisions":{}}))            
            self.assertEquals(rv.status_code,
                              409,
                              'Was expecting status code 409, but it was %s : %s' % (rv.status_code,rv.data))
            
