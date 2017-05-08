import unittest
import os
from mock import MagicMock
import td_integration_test_base
import json
from routes import orm_creation
from util import db_util

class RouteFinalsTD(td_integration_test_base.TdIntegrationDispatchTestBase):
    def setUp(self):
        super(RouteFinalsTD,self).setUp()
        response,results = self.dispatch_request('/%s/util/healthcheck' % self.poop_db_name)                
        self.flask_app = self.app.instances[self.poop_db_name]
        self.admin_user, self.scorekeeper_user,self.desk_user = orm_creation.create_stanard_roles_and_users(self.flask_app)
        #FIXME : password/username should be passed in to create_roles_and_users()
        self.score_user_name_password='test_scorekeeper'
        self.admin_user_name_password='test_admin'        
        db_util.load_machines_from_json(self.flask_app,True)
        orm_creation.init_papa_tournaments_divisions(self.flask_app)        

        self.machine = self.flask_app.tables.Machine.query.filter_by(machine_id=1).first()
        self.division_machines = []
        self.team_division_machines = []
        
        self.players = []
        self.teams = []
        self.flask_app.tables.db_handle.session.commit()
        for i in range(20):
            self.players.append(orm_creation.create_player(self.flask_app,{'first_name':'test','last_name':'player%s'%i,'ifpa_ranking':'123','linked_division_id':'1'}))
        for i in range(10):
            for division in self.flask_app.tables.Division.query.filter_by(team_tournament=False).all():
                self.division_machines.append(orm_creation.create_division_machine(self.flask_app,self.machine,division))
            for division in self.flask_app.tables.Division.query.filter_by(team_tournament=True).all():
                self.team_division_machines.append(orm_creation.create_division_machine(self.flask_app,self.machine,division))
                
        self.division = self.flask_app.tables.Division.query.filter_by(team_tournament=False).all()[0]
        self.team_division = self.flask_app.tables.Division.query.filter_by(team_tournament=True).all()[0]
        
        for i in range(1,10,2):            
            self.teams.append(orm_creation.create_team(self.flask_app,{
                'team_name':'test_team_%s'%i,
                'players':['%s'%i,'%s'%(i+1)]
            }))

    
    def populate_scores_for_finals_testing(self,with_ties=True):
        for division_machine in self.flask_app.tables.DivisionMachine.query.filter_by(division_id=self.division.division_id).all():            
            score=3
            if with_ties:
                increment=2
            else:
                increment=1
            while score <= 20:
                orm_creation.create_entry(self.flask_app,division_machine.division_machine_id,self.division.division_id,score,score-2)            
                if with_ties:
                    orm_creation.create_entry(self.flask_app,division_machine.division_machine_id,self.division.division_id,score,score-1)
                score=score+increment
                
    def test_division_final_initialize(self):        
        self.division.finals_num_qualifiers = 8
        self.flask_app.tables.db_handle.session.commit()
        self.populate_scores_for_finals_testing()
        
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_admin','password':'test_admin'}))
            rv = c.post('/finals/division_final/division_id/%s'%self.division.division_id)
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            
            division_final_returned = json.loads(rv.data)['data']
            self.assertEquals(division_final_returned['division_final_id'],1)

    def test_division_final_get_tiebreakers_with_ties(self):        
        self.division.finals_num_qualifiers = 8
        self.flask_app.tables.db_handle.session.commit()
        self.populate_scores_for_finals_testing()
        
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_admin','password':'test_admin'}))
            rv = c.post('/finals/division_final/division_id/%s'%self.division.division_id)
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            
            division_final_returned = json.loads(rv.data)['data']
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_scorekeeper','password':'test_scorekeeper'}))            
            rv = c.get('/finals/division_final/division_id/%s/tiebreakers'%self.division.division_id)
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            
            tiebreakers_returned = json.loads(rv.data)['data']
            self.assertEquals(len(tiebreakers_returned['tiebreakers']),4)
            self.assertEquals(tiebreakers_returned['tiebreakers'][2][0]['initial_seed'],4)
            self.assertEquals(tiebreakers_returned['tiebreakers'][2][0]['final_player_id'],5)

    def test_division_final_get_tiebreakers_without_ties(self):        
        self.division.finals_num_qualifiers = 8
        self.flask_app.tables.db_handle.session.commit()
        self.populate_scores_for_finals_testing(with_ties=False)
        
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_admin','password':'test_admin'}))
            rv = c.post('/finals/division_final/division_id/%s'%self.division.division_id)
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            
            division_final_returned = json.loads(rv.data)['data']
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_scorekeeper','password':'test_scorekeeper'}))            
            rv = c.get('/finals/division_final/division_id/%s/tiebreakers'%self.division.division_id)
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            
            tiebreakers_returned = json.loads(rv.data)['data']
            self.assertEquals(len(tiebreakers_returned['tiebreakers']),0)

    def test_division_final_record_tiebreakers(self):        
        self.division.finals_num_qualifiers = 8
        self.flask_app.tables.db_handle.session.commit()
        self.populate_scores_for_finals_testing()
        
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_admin','password':'test_admin'}))
            rv = c.post('/finals/division_final/division_id/%s'%self.division.division_id)
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            
            division_final_returned = json.loads(rv.data)['data']
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_scorekeeper','password':'test_scorekeeper'}))            
            rv = c.get('/finals/division_final/division_id/%s/tiebreakers'%self.division.division_id)
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            
            tiebreakers_returned = json.loads(rv.data)['data']            
            tiebreakers_returned['tiebreakers'][0][0]['player_score']=1
            tiebreakers_returned['tiebreakers'][0][1]['player_score']=2
            rv = c.post('/finals/division_final/division_id/%s/tiebreakers' % division_final_returned['division_final_id'],
                       data=json.dumps(tiebreakers_returned['tiebreakers'][0]))
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            rv = c.get('/finals/division_final/division_id/%s/tiebreakers'%self.division.division_id)
            modified_tiebreakers_returned = json.loads(rv.data)['data']            
            self.assertEquals(len(modified_tiebreakers_returned['tiebreakers']),3)
            rv = c.get('/finals/division_final/division_id/%s/qualifiers'%division_final_returned['division_final_id'])
            qualifiers_returned = json.loads(rv.data)['data']                        
            self.assertEquals(qualifiers_returned[0]['initial_seed'],0)
            self.assertEquals(qualifiers_returned[1]['initial_seed'],1)
    
    def test_division_final_get_qualifiers(self):        
        self.division.finals_num_qualifiers = 8
        self.flask_app.tables.db_handle.session.commit()
        self.populate_scores_for_finals_testing()
        
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_admin','password':'test_admin'}))
            rv = c.post('/finals/division_final/division_id/%s'%self.division.division_id)
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            
            division_final_returned = json.loads(rv.data)['data']
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_scorekeeper','password':'test_scorekeeper'}))            
            rv = c.get('/finals/division_final/division_id/%s/qualifiers'%division_final_returned['division_final_id'])
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))            
            qualifiers_returned = json.loads(rv.data)['data']
            self.assertEquals(len(qualifiers_returned), 21)            

    def test_division_final_remove_qualifier_with_ties(self):        
        self.division.finals_num_qualifiers = 8
        self.flask_app.tables.db_handle.session.commit()
        self.populate_scores_for_finals_testing()
        
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_admin','password':'test_admin'}))
            rv = c.post('/finals/division_final/division_id/%s'%self.division.division_id)
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            
            division_final_returned = json.loads(rv.data)['data']
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_scorekeeper','password':'test_scorekeeper'}))            
            rv = c.get('/finals/division_final/division_id/%s/qualifiers'%division_final_returned['division_final_id'])
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))            
            qualifiers_returned = json.loads(rv.data)['data']            
            self.assertEquals(qualifiers_returned[8]['type'],'divider')
            qualifiers_returned[0]['removed']=True            
            rv = c.put('/finals/division_final/division_id/%s/qualifiers'%division_final_returned['division_final_id'],
                       data=json.dumps({'data':qualifiers_returned}))
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))            
            qualifiers_returned = json.loads(rv.data)['data']            
            rv = c.get('/finals/division_final/division_id/%s/qualifiers'%division_final_returned['division_final_id'],
                       data=json.dumps({'data':qualifiers_returned}))
            qualifiers_returned = json.loads(rv.data)['data']
            self.assertEquals(qualifiers_returned[10]['type'],'divider')
            
            
            
