import unittest
import os
from mock import MagicMock
import td_integration_test_base
import json
from routes import orm_creation
from util import db_util

class RouteQueueTD(td_integration_test_base.TdIntegrationDispatchTestBase):
    def setUp(self):
        super(RouteQueueTD,self).setUp()
        response,results = self.dispatch_request('/%s/util/healthcheck' % self.poop_db_name)                
        self.flask_app = self.app.instances[self.poop_db_name]
        self.admin_user, self.scorekeeper_user,self.desk_user = orm_creation.create_stanard_roles_and_users(self.flask_app)
        #FIXME : password/username should be passed in to create_roles_and_users()
        self.score_user_name_password='test_scorekeeper'
        self.admin_user_name_password='test_admin'        
        db_util.load_machines_from_json(self.flask_app,True)
        orm_creation.init_papa_tournaments_divisions(self.flask_app)
        self.player = orm_creation.create_player(self.flask_app,{'first_name':'test','last_name':'player','ifpa_ranking':'123','linked_division_id':'1'})
        self.machine = self.flask_app.tables.Machine.query.filter_by(machine_id=1).first()
        self.division = self.flask_app.tables.Division.query.filter_by(division_id=1).first()
        self.division_machine = orm_creation.create_division_machine(self.flask_app,self.machine,self.division)


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
            
    # def test_add_score(self):                                        

    #     with self.flask_app.test_client() as c:                    
    #         rv = c.put('/auth/login',
    #                    data=json.dumps({'username':'test_desk','password':'test_desk'}))
    #         rv = c.post('/token/paid_for/1',
    #                     data=json.dumps({"player_id":1,                                     
    #                                      "divisions":{1:1},
    #                                      "teams":{},
    #                                      "metadivisions":{}}))
    #     with self.flask_app.test_client() as c:                            
    #         rv = c.put('/auth/login',
    #                    data=json.dumps({'username':self.score_user_name_password,
    #                                     'password':self.score_user_name_password}))
    #         rv = c.post('/queue',
    #                    data=json.dumps({"player_id":"1",                                        
    #                                     "division_machine_id":"1"}))
    #         rv = c.post('/queue',
    #                    data=json.dumps({"player_id":"2",                                        
    #                                     "division_machine_id":"1"}))
    #         rv = c.post('/queue',
    #                    data=json.dumps({"player_id":"3",                                        
    #                                     "division_machine_id":"1"}))                        
    #         #FIXME : need to have a generic way of dealing with multiple test contexts wrt orm objects
    #         division_machine = self.flask_app.tables.DivisionMachine.query.filter_by(division_machine_id=1).first()
    #         division_machine.player_id=None
    #         self.flask_app.tables.db_handle.session.commit()            
    #         rv = c.put('/queue/division_machine/1')
    #         self.assertEquals(rv.status_code,
    #                           200,
    #                           'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
    #         add_player_to_machine_from_queue = json.loads(rv.data)['data']                                    
    #         self.assertEquals(add_player_to_machine_from_queue['division_machine']['player_id'],1)
    #         self.assertEquals(add_player_to_machine_from_queue['next_queue']['queue_id'],2)
    #         division_machine = self.flask_app.tables.DivisionMachine.query.filter_by(division_machine_id=1).first()
    #         self.assertEquals(division_machine.queue_id,2)
    #         self.assertEquals(division_machine.player_id,1)                                    
