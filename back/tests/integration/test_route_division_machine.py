import unittest
import os
from mock import MagicMock
import td_integration_test_base
import json
from routes import orm_creation

class RouteDivisionMachineTD(td_integration_test_base.TdIntegrationDispatchTestBase):
    def setUp(self):
        super(RouteDivisionMachineTD,self).setUp()
        response,results = self.dispatch_request('/%s/util/healthcheck' % self.poop_db_name)                
        self.flask_app = self.app.instances[self.poop_db_name]
        self.admin_user,self.scorekeeper_user,self.desk_user = orm_creation.create_stanard_roles_and_users(self.flask_app)
        self.admin_user_password='test_admin'
        self.desk_user_password='test_desk'        

        self.machine = self.flask_app.tables.Machine(machine_name='test_machine',abbreviation='AAAA')
        self.flask_app.tables.db_handle.session.add(self.machine)
        self.flask_app.tables.db_handle.session.commit()
        self.new_tournament = orm_creation.create_tournament(self.flask_app,{
            'tournament_name':'test_tournament_1',
            'single_division':True,
            'finals_num_qualifiers':'24',
            'scoring_type':"HERB",
            'team_tournament':False,
            'local_price':'5',
            'use_stripe':False
        })

        self.new_player = orm_creation.create_player(self.flask_app,{
            'first_name':'test',
            'last_name':'player',
            'ifpa_ranking':'123'            
        })
        self.new_player_2 = orm_creation.create_player(self.flask_app,{
            'first_name':'test',
            'last_name':'player_2',
            'ifpa_ranking':'123'            
        })        
        self.new_team = orm_creation.create_team(self.flask_app,{
            'team_name':'test_team',
            'players':['1','2']
        })
        self.new_team_2 = orm_creation.create_team(self.flask_app,{
            'team_name':'test_team',
            'players':['1','2']
        })        
        

    def test_add_division_machine(self): 
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user.username,'password':self.admin_user_password}))
            rv = c.post('/division/1/division_machine',
                        data=json.dumps({'machine_id':1}))        
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s' % (rv.status_code))
            
            returned_division_machine = json.loads(rv.data)['data']
            self.assertTrue(returned_division_machine['division_machine_name'],'test_machine')
            self.assertTrue(returned_division_machine['abbreviation'],'GLAM')
            division_machine = self.flask_app.tables.DivisionMachine.query.filter_by(division_machine_id=returned_division_machine['division_machine_id']).first()            
            self.assertIsNotNone(division_machine)

    def test_delete_division_machine(self): 
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user.username,'password':self.admin_user_password}))
            rv = c.post('/division/1/division_machine',
                        data=json.dumps({'machine_id':1}))        
            rv = c.delete('/division/1/division_machine/1')        
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s' % (rv.status_code))
            
            returned_division_machine = json.loads(rv.data)['data']
            self.assertTrue(returned_division_machine['removed'],True)
            division_machine = self.flask_app.tables.DivisionMachine.query.filter_by(division_machine_id=returned_division_machine['division_machine_id']).first()            
            self.assertTrue(division_machine.removed)
            
    def test_get_division_machines(self): 
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user.username,'password':self.admin_user_password}))
            rv = c.post('/division/1/division_machine',
                        data=json.dumps({'machine_id':1}))        

            rv = c.get('/division/1/division_machine')
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s' % (rv.status_code))
            
            division_machine = json.loads(rv.data)['data']['1']
            self.assertTrue(division_machine['division_machine_name'],'test_machine')
            self.assertTrue(division_machine['abbreviation'],'GLAM')                        

    def test_get_division_machine(self): 
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user.username,'password':self.admin_user_password}))
            rv = c.post('/division/1/division_machine',
                        data=json.dumps({'machine_id':1}))        

            rv = c.get('/division/1/division_machine/1')
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s' % (rv.status_code))
            
            division_machine = json.loads(rv.data)['data']
            self.assertEquals(division_machine['division_machine_name'],'test_machine')
            self.assertEquals(division_machine['abbreviation'],'AAAA')                        
            
    def test_add_division_machine_no_auth(self): 
        with self.flask_app.test_client() as c:
            rv = c.post('/division/1/division_machine',
                        data=json.dumps({'machine_id':1}))        
            self.assertEquals(rv.status_code,
                              401,
                              'Was expecting status code 401, but it was %s' % (rv.status_code))

    def test_delete_division_machine_no_auth(self): 
        with self.flask_app.test_client() as c:
            rv = c.delete('/division/1/division_machine/1')        
            self.assertEquals(rv.status_code,
                              401,
                              'Was expecting status code 401, but it was %s' % (rv.status_code))
            

    def test_add_division_machine_wrong_auth(self): 
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_desk','password':'test_desk'}))

            rv = c.post('/division/1/division_machine',
                        data=json.dumps({'machine_id':1}))        
            self.assertEquals(rv.status_code,
                              403,
                              'Was expecting status code 403, but it was %s' % (rv.status_code))

    def test_delete_division_machine_wrong_auth(self): 
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_desk','password':'test_desk'}))

            rv = c.delete('/division/1/division_machine/1')        
            self.assertEquals(rv.status_code,
                              403,
                              'Was expecting status code 403, but it was %s' % (rv.status_code))
            
    def test_add_player_to_machine(self):
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user.username,'password':self.admin_user_password}))
            rv = c.post('/division/1/division_machine',
                        data=json.dumps({'machine_id':1}))
            rv = c.post('/token/paid_for/1',
                        data=json.dumps({"player_id":1,                                     
                                         "divisions":{1:1},
                                         "teams":{},
                                         "metadivisions":{}}))                        
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_scorekeeper','password':'test_scorekeeper'}))                    
            rv = c.put('/division/1/division_machine/1/player/1')
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            returned_division_machine = json.loads(rv.data)['data']
            self.assertEquals(returned_division_machine['player_id'],1)
            division_machine = self.flask_app.tables.DivisionMachine.query.filter_by(division_machine_id=returned_division_machine['division_machine_id']).first()
            self.assertEquals(division_machine.player_id,returned_division_machine['player_id'])

    def test_undo_player_add_to_machine(self):
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user.username,'password':self.admin_user_password}))
            rv = c.post('/division/1/division_machine',
                        data=json.dumps({'machine_id':1}))
            rv = c.post('/token/paid_for/1',
                        data=json.dumps({"player_id":1,                                     
                                         "divisions":{1:1},
                                         "teams":{},
                                         "metadivisions":{}}))                        
            
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_scorekeeper','password':'test_scorekeeper'}))                    
            rv = c.put('/division/1/division_machine/1/player/1')
            rv = c.put('/division/1/division_machine/1/undo')            
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            returned_division_machine = json.loads(rv.data)['data']
            self.assertEquals(returned_division_machine['player_id'],None)
            division_machine = self.flask_app.tables.DivisionMachine.query.filter_by(division_machine_id=returned_division_machine['division_machine_id']).first()
            self.assertEquals(division_machine.player_id,None)
            
    def test_remove_player_from_machine(self):
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user.username,'password':self.admin_user_password}))
            rv = c.post('/division/1/division_machine',
                        data=json.dumps({'machine_id':1}))
            rv = c.post('/token/paid_for/1',
                        data=json.dumps({"player_id":1,                                     
                                         "divisions":{1:1},
                                         "teams":{},
                                         "metadivisions":{}}))                                    
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_scorekeeper','password':'test_scorekeeper'}))        
            rv = c.put('/division/1/division_machine/1/player/1')            
            rv = c.delete('/division/1/division_machine/1/player')
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            returned_division_machine = json.loads(rv.data)['data']
            self.assertEquals(returned_division_machine['player_id'],None)
            division_machine = self.flask_app.tables.DivisionMachine.query.filter_by(division_machine_id=returned_division_machine['division_machine_id']).first()
            self.assertEquals(division_machine.player_id,None)

    def test_remove_player_from_machine_badrequest(self):
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user.username,'password':self.admin_user_password}))
            rv = c.post('/division/1/division_machine',
                        data=json.dumps({'machine_id':1}))
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_scorekeeper','password':'test_scorekeeper'}))                    
            rv = c.delete('/division/1/division_machine/1/player')
            self.assertEquals(rv.status_code,
                              400,
                              'Was expecting status code 400, but it was %s' % (rv.status_code))
            division_machine = self.flask_app.tables.DivisionMachine.query.filter_by(division_machine_id=1).first()
            self.assertEquals(division_machine.player_id,None)

            
    def test_player_add_to_division_machine_conflict(self):
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user.username,'password':self.admin_user_password}))
            rv = c.post('/division/1/division_machine',
                        data=json.dumps({'machine_id':1}))
            rv = c.post('/token/paid_for/1',
                        data=json.dumps({"player_id":1,                                     
                                         "divisions":{1:1},
                                         "teams":{},
                                         "metadivisions":{}}))                                    
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_scorekeeper','password':'test_scorekeeper'}))        
            rv = c.put('/division/1/division_machine/1/player/1')
            rv = c.put('/division/1/division_machine/1/player/2')            
            self.assertEquals(rv.status_code,
                              409,
                              'Was expecting status code 409, but it was %s : %s' % (rv.status_code,rv.data))            
            division_machine = self.flask_app.tables.DivisionMachine.query.filter_by(division_machine_id=1).first()
            self.assertEquals(division_machine.player_id,1)

    def test_remove_player_from_machine_badauth(self):
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user.username,'password':self.admin_user_password}))
            rv = c.post('/division/1/division_machine',
                        data=json.dumps({'machine_id':1}))
        with self.flask_app.test_client() as c:
            rv = c.delete('/division/1/division_machine/1/player')
            self.assertEquals(rv.status_code,
                              401,
                              'Was expecting status code 401, but it was %s' % (rv.status_code))

            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_desk','password':'test_desk'}))                    
            rv = c.delete('/division/1/division_machine/1/player')
            self.assertEquals(rv.status_code,
                              403,
                              'Was expecting status code 403, but it was %s' % (rv.status_code))
            
    def test_player_add_to_division_machine_badauth(self):
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user.username,'password':self.admin_user_password}))
            rv = c.post('/division/1/division_machine',
                        data=json.dumps({'machine_id':1}))        
        with self.flask_app.test_client() as c:
            rv = c.put('/division/1/division_machine/1/player/1')            
            self.assertEquals(rv.status_code,
                              401,
                              'Was expecting status code 401, but it was %s' % (rv.status_code))            
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_desk','password':'test_desk'}))        
            rv = c.put('/division/1/division_machine/1/player/1')            
            self.assertEquals(rv.status_code,
                              403,
                              'Was expecting status code 403, but it was %s' % (rv.status_code))            

    def test_add_team_to_machine(self):
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user.username,'password':self.admin_user_password}))
            rv = c.post('/division/1/division_machine',
                        data=json.dumps({'machine_id':1}))
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_scorekeeper','password':'test_scorekeeper'}))                    
            rv = c.put('/division/1/division_machine/1/team/1')
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            returned_division_machine = json.loads(rv.data)['data']
            self.assertEquals(returned_division_machine['team_id'],1)
            division_machine = self.flask_app.tables.DivisionMachine.query.filter_by(division_machine_id=returned_division_machine['division_machine_id']).first()
            self.assertEquals(division_machine.team_id,returned_division_machine['team_id'])

    def test_remove_team_from_machine(self):
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user.username,'password':self.admin_user_password}))
            rv = c.post('/division/1/division_machine',
                        data=json.dumps({'machine_id':1}))
            rv = c.post('/token/paid_for/1',
                        data=json.dumps({"player_id":1,                                     
                                         "divisions":{1:1},
                                         "teams":{},
                                         "metadivisions":{}}))                                    
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_scorekeeper','password':'test_scorekeeper'}))        
            rv = c.put('/division/1/division_machine/1/team/1')            
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            rv = c.delete('/division/1/division_machine/1/team')
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            returned_division_machine = json.loads(rv.data)['data']
            self.assertEquals(returned_division_machine['team_id'],None)
            division_machine = self.flask_app.tables.DivisionMachine.query.filter_by(division_machine_id=returned_division_machine['division_machine_id']).first()
            self.assertEquals(division_machine.team_id,None)

    def test_remove_team_from_machine_badrequest(self):
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user.username,'password':self.admin_user_password}))
            rv = c.post('/division/1/division_machine',
                        data=json.dumps({'machine_id':1}))
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_scorekeeper','password':'test_scorekeeper'}))                    
            rv = c.delete('/division/1/division_machine/1/team')
            self.assertEquals(rv.status_code,
                              400,
                              'Was expecting status code 400, but it was %s' % (rv.status_code))
            division_machine = self.flask_app.tables.DivisionMachine.query.filter_by(division_machine_id=1).first()
            self.assertEquals(division_machine.team_id,None)

            
    def test_team_add_to_division_machine_conflict(self):
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user.username,'password':self.admin_user_password}))
            rv = c.post('/division/1/division_machine',
                        data=json.dumps({'machine_id':1}))        
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_scorekeeper','password':'test_scorekeeper'}))        
            rv = c.put('/division/1/division_machine/1/team/1')
            rv = c.put('/division/1/division_machine/1/team/2')            
            self.assertEquals(rv.status_code,
                              409,
                              'Was expecting status code 409, but it was %s : %s' % (rv.status_code,rv.data))            
            division_machine = self.flask_app.tables.DivisionMachine.query.filter_by(division_machine_id=1).first()
            self.assertEquals(division_machine.team_id,1)

    def test_remove_team_from_machine_badauth(self):
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user.username,'password':self.admin_user_password}))
            rv = c.post('/division/1/division_machine',
                        data=json.dumps({'machine_id':1}))
        with self.flask_app.test_client() as c:
            rv = c.delete('/division/1/division_machine/1/team')
            self.assertEquals(rv.status_code,
                              401,
                              'Was expecting status code 401, but it was %s' % (rv.status_code))

            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_desk','password':'test_desk'}))                    
            rv = c.delete('/division/1/division_machine/1/team')
            self.assertEquals(rv.status_code,
                              403,
                              'Was expecting status code 403, but it was %s' % (rv.status_code))
            
    def test_team_add_to_division_machine_badauth(self):
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user.username,'password':self.admin_user_password}))
            rv = c.post('/division/1/division_machine',
                        data=json.dumps({'machine_id':1}))        
        with self.flask_app.test_client() as c:
            rv = c.put('/division/1/division_machine/1/team/1')            
            self.assertEquals(rv.status_code,
                              401,
                              'Was expecting status code 401, but it was %s' % (rv.status_code))            
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_desk','password':'test_desk'}))        
            rv = c.put('/division/1/division_machine/1/team/1')            
            self.assertEquals(rv.status_code,
                              403,
                              'Was expecting status code 403, but it was %s' % (rv.status_code))            

            
            
