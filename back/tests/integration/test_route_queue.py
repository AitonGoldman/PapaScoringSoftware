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
        db_util.load_machines_from_json(self.flask_app,True)
        orm_creation.init_papa_tournaments_divisions(self.flask_app)
        self.player = orm_creation.create_player(self.flask_app,{'first_name':'test','last_name':'player','ifpa_ranking':'123','linked_division_id':'1'})
        self.player_two = orm_creation.create_player(self.flask_app,{'first_name':'test_two','last_name':'player_two','ifpa_ranking':'321','linked_division_id':'1'})        
        self.player_three = orm_creation.create_player(self.flask_app,{'first_name':'test_three','last_name':'player_three','ifpa_ranking':'444','linked_division_id':'1'})
        self.player_four = orm_creation.create_player(self.flask_app,{'first_name':'test_three','last_name':'player_four','ifpa_ranking':'555','linked_division_id':'1'})        
        self.machine = self.flask_app.tables.Machine.query.filter_by(machine_id=1).first()
        self.division = self.flask_app.tables.Division.query.filter_by(division_id=1).first()
        self.division_machine = orm_creation.create_division_machine(self.flask_app,self.machine,self.division)
        self.division_machine_2 = orm_creation.create_division_machine(self.flask_app,self.machine,self.division)
        
    def test_add_first_player_to_queue_no_player_on_machine(self):        
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.score_user_name_password,
                                        'password':self.score_user_name_password}))
            rv = c.post('/queue',
                       data=json.dumps({"player_id":"1",                                        
                                        "division_machine_id":"1"}))
            self.assertEquals(rv.status_code,
                              400,
                              'Was expecting status code 400, but it was %s : %s' % (rv.status_code,rv.data))
        
    def test_add_first_player_to_queue(self):        
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.score_user_name_password,
                                        'password':self.score_user_name_password}))
            self.division_machine.player_id=4
            self.flask_app.tables.db_handle.session.commit()            
            rv = c.post('/queue',
                       data=json.dumps({"player_id":"1",                                        
                                        "division_machine_id":"1"}))
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            queue = json.loads(rv.data)['data']                                    
            self.assertEquals(queue['queue_position'],1)
            self.assertEquals(queue['player']['player_id'],1)
            self.assertEquals(queue['division_machine']['division_machine_id'],1)                        
            added_queue = self.flask_app.tables.Queue.query.filter_by(division_machine_id=1,player_id=1).first()
            self.assertIsNotNone(added_queue)
            division_machine = self.flask_app.tables.DivisionMachine.query.filter_by(division_machine_id=1).first()
            self.assertEquals(division_machine.queue_id,1)

    def test_add_second_player_to_queue(self):                
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.score_user_name_password,
                                        'password':self.score_user_name_password}))
            self.division_machine.player_id=4
            self.flask_app.tables.db_handle.session.commit()            
            rv = c.post('/queue',
                       data=json.dumps({"player_id":"1",                                        
                                        "division_machine_id":"1"}))
            rv = c.post('/queue',
                       data=json.dumps({"player_id":"2",                                        
                                        "division_machine_id":"1"}))            
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            queue = json.loads(rv.data)['data']                                    
            self.assertEquals(queue['queue_position'],2)
            self.assertEquals(queue['player']['player_id'],2)
            self.assertEquals(queue['division_machine']['division_machine_id'],1)                        
            added_queue = self.flask_app.tables.Queue.query.filter_by(division_machine_id=1,player_id=2).first()
            self.assertIsNotNone(added_queue)
            division_machine = self.flask_app.tables.DivisionMachine.query.filter_by(division_machine_id=1).first()
            self.assertEquals(division_machine.queue_id,1)
            self.assertEquals(division_machine.queue.queue_child[0].queue_id,2)

    def test_add_third_player_to_queue(self):                
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.score_user_name_password,
                                        'password':self.score_user_name_password}))
            self.division_machine.player_id=4
            self.flask_app.tables.db_handle.session.commit()            
            rv = c.post('/queue',
                       data=json.dumps({"player_id":"1",                                        
                                        "division_machine_id":"1"}))
            rv = c.post('/queue',
                       data=json.dumps({"player_id":"2",                                        
                                        "division_machine_id":"1"}))
            rv = c.post('/queue',
                       data=json.dumps({"player_id":"3",                                        
                                        "division_machine_id":"1"}))                        
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            queue = json.loads(rv.data)['data']                                    
            self.assertEquals(queue['queue_position'],3)
            self.assertEquals(queue['player']['player_id'],3)
            self.assertEquals(queue['division_machine']['division_machine_id'],1)                        
            added_queue = self.flask_app.tables.Queue.query.filter_by(division_machine_id=1,player_id=3).first()
            self.assertIsNotNone(added_queue)
            division_machine = self.flask_app.tables.DivisionMachine.query.filter_by(division_machine_id=1).first()
            self.assertEquals(division_machine.queue_id,1)
            self.assertEquals(division_machine.queue.queue_child[0].queue_child[0].queue_id,3)

    def test_remove_player_from_queue(self):                        
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.score_user_name_password,
                                        'password':self.score_user_name_password}))
            self.division_machine.player_id=4
            self.flask_app.tables.db_handle.session.commit()            
            rv = c.post('/queue',
                       data=json.dumps({"player_id":"1",                                        
                                        "division_machine_id":"1"}))
            rv = c.post('/queue',
                       data=json.dumps({"player_id":"2",                                        
                                        "division_machine_id":"1"}))
            rv = c.post('/queue',
                       data=json.dumps({"player_id":"3",                                        
                                        "division_machine_id":"1"}))                                    
            rv = c.delete('/queue/player/2')            
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            queue = json.loads(rv.data)['data']                                    
            modified_queue = []
            division_machine = self.flask_app.tables.DivisionMachine.query.filter_by(division_machine_id=1).first()
            queue_from_db = division_machine.queue
            
            while queue_from_db is not None:                
                modified_queue.append(queue_from_db)                
                if len(queue_from_db.queue_child) > 0:                    
                    queue_from_db = queue_from_db.queue_child[0]                    
                else:
                    queue_from_db = None
            
            self.assertIsNotNone(modified_queue)
            self.assertEquals(len(modified_queue),2)
            self.assertEquals(modified_queue[0].player_id,1)
            self.assertEquals(modified_queue[1].player_id,3)                        


    def test_get_queues(self):                
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.score_user_name_password,
                                        'password':self.score_user_name_password}))
            self.division_machine.player_id=4
            self.flask_app.tables.db_handle.session.commit()            
            rv = c.post('/queue',
                       data=json.dumps({"player_id":"1",                                        
                                        "division_machine_id":"1"}))
            rv = c.post('/queue',
                       data=json.dumps({"player_id":"3",                                        
                                        "division_machine_id":"1"}))
            rv = c.post('/queue',
                       data=json.dumps({"player_id":"2",                                        
                                        "division_machine_id":"1"}))
            rv = c.get('/queue/division/1')            
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            returned_queues = json.loads(rv.data)['data']
            self.assertEquals(returned_queues['1']['division_machine_name'],'Glamor Girls')            
            self.assertEquals(returned_queues['1']['queues'][0]['player']['player_id'],1)
            self.assertEquals(returned_queues['1']['queues'][0]['queue_position'],1)
            self.assertEquals(returned_queues['1']['queues'][1]['player']['player_id'],3)
            self.assertEquals(returned_queues['1']['queues'][1]['queue_position'],2)            
            self.assertEquals(returned_queues['1']['queues'][2]['player']['player_id'],2)            
            self.assertEquals(returned_queues['1']['queues'][2]['queue_position'],3)

    def test_get_empty_queues(self):                
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.score_user_name_password,
                                        'password':self.score_user_name_password}))
            self.division_machine.player_id=4
            self.flask_app.tables.db_handle.session.commit()            
            rv = c.get('/queue/division/1')            
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            returned_queues = json.loads(rv.data)['data']
            self.assertEquals(returned_queues['1']['division_machine_name'],'Glamor Girls')
            self.assertEquals(len(returned_queues['1']['queues']),0)
            
    def test_remove_player_from_queue_and_re_add(self):                
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.score_user_name_password,
                                        'password':self.score_user_name_password}))
            self.division_machine.player_id=4
            self.flask_app.tables.db_handle.session.commit()            
            rv = c.post('/queue',
                       data=json.dumps({"player_id":"1",                                        
                                        "division_machine_id":"1"}))
            rv = c.post('/queue',
                       data=json.dumps({"player_id":"2",                                        
                                        "division_machine_id":"1"}))
            rv = c.post('/queue',
                       data=json.dumps({"player_id":"3",                                        
                                        "division_machine_id":"1"}))                        
            rv = c.delete('/queue/player/2')                                    
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            queue = json.loads(rv.data)['data']                                    
            modified_queue = []
            queue = self.flask_app.tables.DivisionMachine.query.filter_by(division_machine_id=1).first().queue 
            while queue is not None:
                modified_queue.append(queue)
                if len(queue.queue_child) > 0:
                    queue = queue.queue_child[0]
                else:
                    queue = None
            self.assertIsNotNone(modified_queue)
            self.assertEquals(len(modified_queue),2)
            self.assertEquals(modified_queue[0].player_id,1)
            self.assertEquals(modified_queue[1].player_id,3)            

            rv = c.post('/queue',
                       data=json.dumps({"player_id":"2",                                        
                                        "division_machine_id":"1"}))
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            modified_queue = []
            queue = self.flask_app.tables.DivisionMachine.query.filter_by(division_machine_id=1).first().queue 
            while queue is not None:
                modified_queue.append(queue)
                if len(queue.queue_child) > 0:
                    queue = queue.queue_child[0]
                else:
                    queue = None
            self.assertIsNotNone(modified_queue)
            self.assertEquals(len(modified_queue),3)
            self.assertEquals(modified_queue[0].player_id,1)
            self.assertEquals(modified_queue[1].player_id,3)
            self.assertEquals(modified_queue[2].player_id,2)
            
            
    def test_bump_player_from_three_player_queue(self):                
        with self.flask_app.test_client() as c:                                
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.score_user_name_password,
                                        'password':self.score_user_name_password}))
            self.division_machine.player_id=4
            self.flask_app.tables.db_handle.session.commit()            
            rv = c.post('/queue',
                       data=json.dumps({"player_id":"1",                                        
                                        "division_machine_id":"1"}))
            rv = c.post('/queue',
                       data=json.dumps({"player_id":"2",                                        
                                        "division_machine_id":"1"}))
            rv = c.post('/queue',
                       data=json.dumps({"player_id":"3",                                        
                                        "division_machine_id":"1"}))
            rv = c.put('/queue/division_machine/1/bump')
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            modified_queue = []
            queue = self.flask_app.tables.DivisionMachine.query.filter_by(division_machine_id=1).first().queue 
            while queue is not None:
                modified_queue.append(queue)
                if len(queue.queue_child) > 0:
                    queue = queue.queue_child[0]
                else:
                    queue = None
            self.assertIsNotNone(modified_queue)
            self.assertEquals(len(modified_queue),3)
            self.assertEquals(modified_queue[0].player_id,2)
            self.assertEquals(modified_queue[1].player_id,3)
            self.assertEquals(modified_queue[2].player_id,1)


    def test_bump_player_from_three_player_queue_and_one_bump(self):                
        self.flask_app.td_config['QUEUE_BUMP_AMOUNT']=1
        with self.flask_app.test_client() as c:                                            
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.score_user_name_password,
                                        'password':self.score_user_name_password}))
            self.division_machine.player_id=4
            self.flask_app.tables.db_handle.session.commit()            
            rv = c.post('/queue',
                       data=json.dumps({"player_id":"1",                                        
                                        "division_machine_id":"1"}))
            rv = c.post('/queue',
                       data=json.dumps({"player_id":"2",                                        
                                        "division_machine_id":"1"}))
            rv = c.post('/queue',
                       data=json.dumps({"player_id":"3",                                        
                                        "division_machine_id":"1"}))
            rv = c.put('/queue/division_machine/1/bump')
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))            
            modified_queue = []
            queue = self.flask_app.tables.DivisionMachine.query.filter_by(division_machine_id=1).first().queue 
            while queue is not None:
                modified_queue.append(queue)
                if len(queue.queue_child) > 0:
                    queue = queue.queue_child[0]
                else:
                    queue = None
            self.assertIsNotNone(modified_queue)
            self.assertEquals(len(modified_queue),3)
            self.assertEquals(modified_queue[0].player_id,2)
            self.assertEquals(modified_queue[1].player_id,1)
            self.assertEquals(modified_queue[2].player_id,3)
            
    def test_bump_player_from_one_player_queue(self):                
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.score_user_name_password,
                                        'password':self.score_user_name_password}))
            self.division_machine.player_id=4
            self.flask_app.tables.db_handle.session.commit()            
            rv = c.post('/queue',
                       data=json.dumps({"player_id":"1",                                        
                                        "division_machine_id":"1"}))
            rv = c.put('/queue/division_machine/1/bump')
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            modified_queue = self.flask_app.tables.Queue.query.filter_by(division_machine_id=1).all()
            self.assertEquals(len(modified_queue),0)
            

    def test_add_player_to_machine_from_queue_with_one_player(self):                        
        self.division_machine.player_id=4
        self.flask_app.tables.db_handle.session.commit()            

        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_desk','password':'test_desk'}))
            rv = c.post('/token/paid_for/1',
                        data=json.dumps({"player_id":1,                                     
                                         "divisions":{1:1},
                                         "teams":{},
                                         "metadivisions":{}}))
        with self.flask_app.test_client() as c:                            
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.score_user_name_password,
                                        'password':self.score_user_name_password}))
            rv = c.post('/queue',
                       data=json.dumps({"player_id":"1",                                        
                                        "division_machine_id":"1"}))            
            #FIXME : need to have a generic way of dealing with multiple test contexts wrt orm objects
            division_machine = self.flask_app.tables.DivisionMachine.query.filter_by(division_machine_id=1).first()
            division_machine.player_id=None
            self.flask_app.tables.db_handle.session.commit()            
            rv = c.put('/queue/division_machine/1')
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            add_player_to_machine_from_queue = json.loads(rv.data)['data']                                    
            self.assertEquals(add_player_to_machine_from_queue['division_machine']['player_id'],1)
            self.assertFalse('next_queue' in add_player_to_machine_from_queue)
            division_machine = self.flask_app.tables.DivisionMachine.query.filter_by(division_machine_id=1).first()
            self.assertEquals(division_machine.queue_id,None)
            self.assertEquals(division_machine.player_id,1)                        

    def test_add_player_to_machine_from_queue_with_one_player_already_on_machine(self):                
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_desk','password':'test_desk'}))
            rv = c.post('/token/paid_for/1',
                        data=json.dumps({"player_id":1,                                     
                                         "divisions":{1:1},
                                         "teams":{},
                                         "metadivisions":{}}))
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.score_user_name_password,
                                        'password':self.score_user_name_password}))
            self.division_machine.player_id=4
            self.flask_app.tables.db_handle.session.commit()            
            rv = c.post('/queue',
                       data=json.dumps({"player_id":"1",                                        
                                        "division_machine_id":"1"}))
            self.division_machine.player_id=None
            self.division_machine_2.player_id=1
            self.flask_app.tables.db_handle.session.commit()            
            
            rv = c.put('/queue/division_machine/1')
            self.assertEquals(rv.status_code,
                              400,
                              'Was expecting status code 400, but it was %s : %s' % (rv.status_code,rv.data))            
            
            
    def test_add_player_to_machine_from_queue_with_one_player_no_tokens(self):                
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.score_user_name_password,
                                        'password':self.score_user_name_password}))
            self.division_machine.player_id=4
            self.flask_app.tables.db_handle.session.commit()                        
            rv = c.post('/queue',
                       data=json.dumps({"player_id":"1",                                        
                                        "division_machine_id":"1"}))
            self.division_machine.player_id=None
            self.flask_app.tables.db_handle.session.commit()                                    
            rv = c.put('/queue/division_machine/1')
            self.assertEquals(rv.status_code,
                              400,
                              'Was expecting status code 400, but it was %s : %s' % (rv.status_code,rv.data))            

            
    def test_add_player_to_two_queues(self):        
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.score_user_name_password,
                                        'password':self.score_user_name_password}))
            self.division_machine.player_id=4
            self.division_machine_2.player_id=3            
            self.flask_app.tables.db_handle.session.commit()            
            rv = c.post('/queue',
                       data=json.dumps({"player_id":"1",                                        
                                        "division_machine_id":"1"}))
            first_queue = json.loads(rv.data)['data']            
            rv = c.post('/queue',
                       data=json.dumps({"player_id":"1",                                        
                                        "division_machine_id":"2"}))            
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            second_queue = json.loads(rv.data)['data']
            self.assertEquals(second_queue['queue_position'],1)
            self.assertEquals(second_queue['player']['player_id'],1)
            self.assertEquals(second_queue['division_machine']['division_machine_id'],2)                        

            second_added_queue = self.flask_app.tables.Queue.query.filter_by(division_machine_id=2,player_id=1).first()
            self.assertIsNotNone(second_added_queue)
            first_added_queue = self.flask_app.tables.Queue.query.filter_by(division_machine_id=1,player_id=1).first()
            self.assertIsNone(first_added_queue)            
            division_machine = self.flask_app.tables.DivisionMachine.query.filter_by(division_machine_id=1).first()
            self.assertEquals(division_machine.queue_id,None)
            division_machine_two = self.flask_app.tables.DivisionMachine.query.filter_by(division_machine_id=2).first()
            self.assertEquals(division_machine_two.queue_id,second_queue['queue_id'])
