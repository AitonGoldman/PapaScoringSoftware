import unittest
import os
from mock import MagicMock
import td_integration_test_base
import json

class RouteAuthTD(td_integration_test_base.TdIntegrationDispatchTestBase):
    def setUp(self):
        super(RouteAuthTD,self).setUp()
        response,results = self.dispatch_request('/%s/util/healthcheck' % self.poop_db_name)                
        self.flask_app = self.app.instances[self.poop_db_name]
        self.admin_role = self.flask_app.tables.Role(name='admin')
        self.flask_app.tables.db_handle.session.add(self.admin_role)
        self.flask_app.tables.db_handle.session.commit()

        self.admin_role_id = self.admin_role.role_id
        
        self.admin_user = self.flask_app.tables.User(username='test_admin')
        self.admin_user.crypt_password('test_admin_password')
        self.admin_user.roles.append(self.admin_role)
        self.flask_app.tables.db_handle.session.add(self.admin_user)
        self.flask_app.tables.db_handle.session.commit()


    def test_tournament_create_no_teams_single(self):        
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                   data=json.dumps({'username':self.admin_user.username,'password':'test_admin_password'}))            
            
            rv = c.post('/tournament',
                       data=json.dumps({'tournament_name':'test_tournament',                                        
                                        'single_division':True,
                                        'scoring_type':'HERB',
                                        'finals_num_qualifiers':24
                                        ,}))
            
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s' % (rv.status_code))
            new_tourney = json.loads(rv.data)
            retrieved_tourney = self.flask_app.tables.Tournament.query.filter_by(tournament_id=new_tourney['data']['tournament_id']).first()
            retrieved_division = retrieved_tourney.divisions[0] if len(retrieved_tourney.divisions)==1 else None
            self.assertIsNotNone(retrieved_tourney,
                                 "Could not find the tournament we just created")
            self.assertIsNotNone(retrieved_division,
                                 "Could not find the division we just created")
            self.assertEquals(retrieved_division.division_name,'test_tournament_single')
            self.assertEquals(new_tourney['data']['tournament_name'],'test_tournament')            
            self.assertEquals(new_tourney['data']['single_division'],True)
            self.assertEquals(retrieved_division.scoring_type,"HERB")
            self.assertEquals(retrieved_division.team_tournament,False)            

    def test_tournament_create_multiple_divisions(self):        
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                   data=json.dumps({'username':self.admin_user.username,'password':'test_admin_password'}))            
            rv = c.post('/tournament',
                       data=json.dumps({'tournament_name':'test_tournament',                                        
                                        'single_division':False,
                                        'scoring_type':'HERB'
                                        ,}))            
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s' % (rv.status_code))
            new_tourney = json.loads(rv.data)
            retrieved_tourney = self.flask_app.tables.Tournament.query.filter_by(tournament_id=new_tourney['data']['tournament_id']).first()
            retrieved_division = retrieved_tourney.divisions[0] if len(retrieved_tourney.divisions)==1 else None
            self.assertIsNotNone(retrieved_tourney,
                                 "Could not find the tournament we just created")
            self.assertIsNone(retrieved_division,
                              "Found a division we were not expecting")
                        
            
    def test_tournament_create_invalid(self):        
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                   data=json.dumps({'username':self.admin_user.username,'password':'test_admin_password'}))            
            rv = c.post('/tournament',
                       data=json.dumps({'team_tournament':False,
                                        'single_division':True,
                                        'scoring_type':'POOP'                                        
                                        ,}))            
            self.assertEquals(rv.status_code,
                              400,
                              'Was expecting status code 400, but it was %s' % (rv.status_code))

    def test_tournament_create_duplicate(self):        
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                   data=json.dumps({'username':self.admin_user.username,'password':'test_admin_password'}))            
            
            rv = c.post('/tournament',
                       data=json.dumps({'tournament_name':'test_tournament',                                        
                                        'single_division':True,
                                        'scoring_type':'HERB',
                                        'finals_num_qualifiers':24
                                        ,}))            
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s' % (rv.status_code))
            
            rv = c.post('/tournament',
                       data=json.dumps({'tournament_name':'test_tournament',                                        
                                        'single_division':True,
                                        'scoring_type':'HERB',
                                        'finals_num_qualifiers':24                                        
                                        ,}))            
            self.assertEquals(rv.status_code,
                              409,
                              'Was expecting status code 409, but it was %s' % (rv.status_code))
            
            
    def test_tournament_edit(self):        
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                   data=json.dumps({'username':self.admin_user.username,'password':'test_admin_password'}))            
            rv = c.post('/tournament',
                       data=json.dumps({'tournament_name':'test_tournament',
                                        'team_tournament':False,
                                        'single_division':False,
                                        'scoring_type':'HERB'                                        
                                        ,}))            
            new_tourney = json.loads(rv.data)
            rv = c.put('/tournament/%s' % new_tourney['data']['tournament_id'],
                       data=json.dumps({'tournament_name':'test_tournament_rename',
                                        'team_tournament':True,
                                        'single_division':True,
                                        'scoring_type':'PAPA'                                        
                                        ,}))            
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s' % (rv.status_code))

            edited_tourney = json.loads(rv.data)            
            self.assertEquals(edited_tourney['data']['tournament_name'],'test_tournament_rename')
            

            
