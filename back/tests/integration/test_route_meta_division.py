import unittest
import os
from mock import MagicMock
import td_integration_test_base
import json
from routes import orm_creation

class RouteMetaDivisionTD(td_integration_test_base.TdIntegrationDispatchTestBase):
    def setUp(self):
        super(RouteMetaDivisionTD,self).setUp()
        response,results = self.dispatch_request('/%s/util/healthcheck' % self.poop_db_name)                
        self.flask_app = self.app.instances[self.poop_db_name]
        self.admin_user,self.scorekeeper_user,self.desk_user = orm_creation.create_stanard_roles_and_users(self.flask_app)
        self.admin_user_password='test_admin'
        self.desk_user_password='test_desk'        

        self.new_tournament_one = orm_creation.create_tournament(self.flask_app,{
            'tournament_name':'test_tournament_1',
            'single_division':True,
            'finals_num_qualifiers':'24',
            'scoring_type':"HERB",
            'team_tournament':False,
            'local_price':'5',
            'use_stripe':False
        })

        self.new_tournament_two = orm_creation.create_tournament(self.flask_app,{
            'tournament_name':'test_tournament_2',
            'single_division':True,
            'finals_num_qualifiers':'24',
            'scoring_type':"HERB",
            'team_tournament':False,
            'local_price':'5',
            'use_stripe':False
        })

        self.new_tournament_three = orm_creation.create_tournament(self.flask_app,{
            'tournament_name':'test_tournament_3',
            'single_division':True,
            'finals_num_qualifiers':'24',
            'scoring_type':"HERB",
            'team_tournament':False,
            'local_price':'5',
            'use_stripe':False
        })

        self.division_one = self.new_tournament_one.divisions[0]
        self.division_two = self.new_tournament_two.divisions[0]
        self.division_three = self.new_tournament_three.divisions[0]

    def test_add_meta_division(self):        
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user.username,'password':self.admin_user_password}))
            rv = c.post('/meta_division',
                        data=json.dumps({'divisions':['1','2'],'meta_division_name':'test_meta_division'}))        
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s' % (rv.status_code))
            meta_division = json.loads(rv.data)['data']
            self.assertTrue('meta_division_id' in meta_division)
            meta_division = self.flask_app.tables.MetaDivision.query.filter_by(meta_division_id=meta_division['meta_division_id']).first()
            self.assertIsNotNone(meta_division)
            self.assertEquals(meta_division.meta_division_name,'test_meta_division')
            self.assertEquals(len(meta_division.divisions),2)
            
    def test_edit_meta_division(self):        
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user.username,'password':self.admin_user_password}))
            rv = c.post('/meta_division',
                        data=json.dumps({'divisions':['1','2'],'meta_division_name':'test_meta_division'}))        
            rv = c.put('/meta_division/1',
                        data=json.dumps({'divisions':['1'],'meta_division_name':'test_meta_division_new'}))        
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s' % (rv.status_code))
            meta_division = json.loads(rv.data)['data']
            self.assertTrue('meta_division_id' in meta_division)
            meta_division = self.flask_app.tables.MetaDivision.query.filter_by(meta_division_id=meta_division['meta_division_id']).first()
            self.assertEquals(meta_division.meta_division_name,'test_meta_division_new')            
            self.assertEquals(len(meta_division.divisions),1)
            rv = c.put('/meta_division/1',
                        data=json.dumps({'divisions':['1','3']}))        
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s' % (rv.status_code))
            meta_division = json.loads(rv.data)['data']
            self.assertTrue('meta_division_id' in meta_division)
            meta_division_table  = self.flask_app.tables.MetaDivision.query.filter_by(meta_division_id=meta_division['meta_division_id']).first()
            self.assertEquals(meta_division['meta_division_name'],'test_meta_division_new')            
            self.assertEquals(len(meta_division['divisions']),2)
            self.assertTrue('3' in meta_division['divisions'])

    def test_add_meta_division_badauth(self):        
        with self.flask_app.test_client() as c:                    
            rv = c.post('/meta_division',
                        data=json.dumps({'divisions':['1','2'],'meta_division_name':'test_meta_division'}))        
            self.assertEquals(rv.status_code,
                              401,
                              'Was expecting status code 401, but it was %s' % (rv.status_code))
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_desk','password':'test_desk'}))
            rv = c.post('/meta_division',
                        data=json.dumps({'divisions':['1','2'],'meta_division_name':'test_meta_division'}))        
            self.assertEquals(rv.status_code,
                              403,
                              'Was expecting status code 403, but it was %s' % (rv.status_code))
            
    def test_edit_meta_division_badauth(self):        
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user.username,'password':self.admin_user_password}))
            rv = c.post('/meta_division',
                        data=json.dumps({'divisions':['1','2'],'meta_division_name':'test_meta_division'}))        
        with self.flask_app.test_client() as c:                    
            rv = c.put('/meta_division/1',
                        data=json.dumps({'divisions':['1'],'meta_division_name':'test_meta_division_new'}))        
            self.assertEquals(rv.status_code,
                              401,
                              'Was expecting status code 401, but it was %s' % (rv.status_code))
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_desk','password':'test_desk'}))
            rv = c.put('/meta_division/1',
                        data=json.dumps({'divisions':['1'],'meta_division_name':'test_meta_division_new'}))        
            self.assertEquals(rv.status_code,
                              403,
                              'Was expecting status code 403, but it was %s' % (rv.status_code))
            
