import unittest
import os
from mock import MagicMock
import td_integration_test_base
import json
from routes import orm_creation
class RouteDivisionTD(td_integration_test_base.TdIntegrationDispatchTestBase):
    def setUp(self):
        super(RouteDivisionTD,self).setUp()
        response,results = self.dispatch_request('/%s/util/healthcheck' % self.poop_db_name)                
        self.flask_app = self.app.instances[self.poop_db_name]
        self.admin_user,self.scorekeeper_user,self.desk_user = orm_creation.create_stanard_roles_and_users(self.flask_app)
        self.admin_user_name='test_admin'        
        self.admin_user_password='test_admin'
        self.desk_user_name='test_desk'
        self.desk_user_password='test_desk'
        self.new_player = orm_creation.create_player(self.flask_app,{'first_name':'aiton','last_name':'goldman','ifpa_ranking':'123'})        
        
    def test_add_division(self):        
        new_tournament = orm_creation.create_tournament(self.flask_app,{
            'tournament_name':'test_tournament_1',
            'single_division':False
        })
        #self.flask_app.tables.db_handle.session.add(new_tournament)
        #self.flask_app.tables.db_handle.session.commit()
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user_name,'password':self.admin_user_password}))
            rv = c.post('/division',
                        data=json.dumps({'division_name':'test_division_1',
                                         'scoring_type':'HERB',
                                         'finals_num_qualifiers':24,
                                         'active':False,
                                         'team_tournament':False,
                                         'use_stripe':False,
                                         'local_price':'5',
                                         'tournament_id':new_tournament.tournament_id
                        }))        
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s' % (rv.status_code))
            division = json.loads(rv.data)['data']
            self.assertTrue('division_id' in division)
            division = self.flask_app.tables.Division.query.filter_by(division_id=division['division_id']).first()
            self.assertEquals(division.division_name,'test_division_1')            
            self.assertEquals(division.active,False)
            self.assertEquals(division.team_tournament,False)
            self.assertEquals(division.scoring_type,"HERB")
            self.assertEquals(division.use_stripe,False)
            self.assertEquals(division.local_price,5)
            #self.assertEquals(division.stripe_sku,"poop")
            self.assertEquals(division.finals_num_qualifiers,24)

    @unittest.skipIf(os.getenv('TEST_STRIPE_SKU',None) is None or os.getenv('STRIPE_API_KEY',None) is None,
                     "SKIPPING BECAUSE NO TEST_STRIPE_SKU SET")
    def test_add_division_stripe(self):        
        new_tournament = orm_creation.create_tournament(self.flask_app,{
            'tournament_name':'test_tournament_1',
            'single_division':False
        })
        #self.flask_app.tables.db_handle.session.add(new_tournament)
        #self.flask_app.tables.db_handle.session.commit()
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user_name,'password':self.admin_user_password}))
            rv = c.post('/division',
                        data=json.dumps({'division_name':'test_division_1',
                                         'scoring_type':'HERB',
                                         'finals_num_qualifiers':24,
                                         'active':False,
                                         'team_tournament':False,
                                         'use_stripe':True,
                                         'stripe_sku':os.getenv('TEST_STRIPE_SKU'),
                                         'tournament_id':new_tournament.tournament_id
                        }))        
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s' % (rv.status_code))
            division = json.loads(rv.data)['data']
            self.assertTrue('division_id' in division)
            division = self.flask_app.tables.Division.query.filter_by(division_id=division['division_id']).first()
            self.assertEquals(division.division_name,'test_division_1')            
            self.assertEquals(division.active,False)
            self.assertEquals(division.team_tournament,False)
            self.assertEquals(division.scoring_type,"HERB")
            self.assertEquals(division.use_stripe,True)
            self.assertEquals(division.stripe_sku,os.getenv('TEST_STRIPE_SKU'))
            #self.assertEquals(division.stripe_sku,"poop")
            self.assertEquals(division.finals_num_qualifiers,24)
            
    def test_add_duplicate_division(self):        
        new_tournament = orm_creation.create_tournament(self.flask_app,{
            'tournament_name':'test_tournament_1',
            'single_division':False
        })
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user_name,'password':self.admin_user_password}))
            rv = c.post('/division',
                        data=json.dumps({'division_name':'test_division_1',
                                         'scoring_type':'HERB',
                                         'finals_num_qualifiers':24,
                                         'active':False,
                                         'team_tournament':False,
                                         'use_stripe':False,
                                         'local_price':'5',
                                         'tournament_id':new_tournament.tournament_id
                        }))        
            rv = c.post('/division',
                        data=json.dumps({'division_name':'test_division_1',
                                         'scoring_type':'HERB',
                                         'finals_num_qualifiers':24,
                                         'active':False,
                                         'team_tournament':False,
                                         'use_stripe':False,
                                         'tournament_id':new_tournament.tournament_id
                        }))        

            self.assertEquals(rv.status_code,
                              409,
                              'Was expecting status code 409, but it was %s' % (rv.status_code))
            
    def test_edit_division(self):        
        new_tournament = orm_creation.create_tournament(self.flask_app,{
            'tournament_name':'test_tournament_1',
            'single_division':False
        })
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user_name,'password':self.admin_user_password}))
            rv = c.post('/division',
                        data=json.dumps({'division_name':'test_division_1',
                                         'scoring_type':'HERB',
                                         'finals_num_qualifiers':24,
                                         'active':False,
                                         'team_tournament':False,
                                         'use_stripe':False,
                                         'local_price':5,
                                         'tournament_id':new_tournament.tournament_id
                        }))
            division = json.loads(rv.data)['data']                        
            rv = c.put('/division/%s'%division['division_id'],
                        data=json.dumps({'scoring_type':'PAPA',
                                         'division_id':division['division_id'],
                                         'finals_num_qualifiers':14,
                                         'active':True,
                                         'team_tournament':True,
                                         'use_stripe':False,
                                         'local_price':10,
                                         'tournament_id':new_tournament.tournament_id
                        }))                    
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s' % (rv.status_code))
            division = json.loads(rv.data)['data']
            self.assertTrue('division_id' in division)
            division = self.flask_app.tables.Division.query.filter_by(division_id=division['division_id']).first()
            self.assertEquals(division.division_name,'test_division_1')            
            self.assertEquals(division.active,True)
            self.assertEquals(division.team_tournament,True)            
            self.assertEquals(division.use_stripe,False)
            self.assertEquals(division.local_price,10)
            self.assertEquals(division.finals_num_qualifiers,14)

    @unittest.skipIf(os.getenv('TEST_STRIPE_SKU',None) is None or os.getenv('STRIPE_API_KEY',None) is None,
                     "SKIPPING BECAUSE NO TEST_STRIPE_SKU SET")
    def test_edit_division_stripe(self):        
        new_tournament = orm_creation.create_tournament(self.flask_app,{
            'tournament_name':'test_tournament_1',
            'single_division':False
        })
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user_name,'password':self.admin_user_password}))
            rv = c.post('/division',
                        data=json.dumps({'division_name':'test_division_1',
                                         'scoring_type':'HERB',
                                         'finals_num_qualifiers':24,
                                         'active':False,
                                         'team_tournament':False,
                                         'use_stripe':False,
                                         'local_price':5,
                                         'tournament_id':new_tournament.tournament_id
                        }))
            division = json.loads(rv.data)['data']                        
            rv = c.put('/division/%s'%division['division_id'],
                        data=json.dumps({'scoring_type':'PAPA',
                                         'division_id':division['division_id'],
                                         'finals_num_qualifiers':14,
                                         'active':True,
                                         'team_tournament':True,
                                         'use_stripe':True,
                                         'stripe_sku':os.getenv('TEST_STRIPE_SKU'),
                                         'tournament_id':new_tournament.tournament_id
                        }))                    
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s' % (rv.status_code))
            division = json.loads(rv.data)['data']
            self.assertTrue('division_id' in division)
            division = self.flask_app.tables.Division.query.filter_by(division_id=division['division_id']).first()
            self.assertEquals(division.division_name,'test_division_1')            
            self.assertEquals(division.active,True)
            self.assertEquals(division.team_tournament,True)            
            self.assertEquals(division.use_stripe,True)
            self.assertEquals(division.stripe_sku,os.getenv('TEST_STRIPE_SKU'))
            self.assertEquals(division.finals_num_qualifiers,14)
            
    def test_get_divisions(self):                
        new_tournament = orm_creation.create_tournament(self.flask_app,{
            'tournament_name':'test_tournament_1',
            'single_division':False
        })
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user_name,'password':self.admin_user_password}))
            rv = c.post('/division',
                        data=json.dumps({'division_name':'test_division_1',
                                         'scoring_type':'HERB',
                                         'finals_num_qualifiers':24,
                                         'active':False,
                                         'team_tournament':False,
                                         'use_stripe':False,
                                         'local_price':5,
                                         'tournament_id':new_tournament.tournament_id
                        }))
            rv = c.post('/division',
                        data=json.dumps({'division_name':'test_division_2',
                                         'scoring_type':'HERB',
                                         'finals_num_qualifiers':24,
                                         'active':False,
                                         'team_tournament':False,
                                         'use_stripe':False,
                                         'local_price':10,
                                         'tournament_id':new_tournament.tournament_id
                        }))                
            
        with self.flask_app.test_client() as c:                                
            rv = c.get('/division')
            
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s' % (rv.status_code))
            division = json.loads(rv.data)['data']
            #FIXME : looking for 3 keys, not 2 - this is because we shove metadivisions in the results
            self.assertTrue('metadivisions' in division.keys())
            self.assertEquals(len(division.keys()),3)
            
            
    def test_get_division(self):        
        new_tournament = orm_creation.create_tournament(self.flask_app,{
            'tournament_name':'test_tournament_1',
            'single_division':False
        })         
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user_name,'password':self.admin_user_password}))
            rv = c.post('/division',
                        data=json.dumps({'division_name':'test_division_1',
                                         'scoring_type':'HERB',
                                         'finals_num_qualifiers':24,
                                         'active':False,
                                         'team_tournament':False,
                                         'use_stripe':False,
                                         'local_price':5,
                                         'tournament_id':new_tournament.tournament_id
                        }))
            division = json.loads(rv.data)['data']

        with self.flask_app.test_client() as c:                                
            rv = c.get('/division/%s' % division['division_id'])
            
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s' % (rv.status_code))
            division = json.loads(rv.data)['data']
            self.assertIsNotNone(division,
                                 "Could not find the division we just created")
            self.assertEquals(division['division_name'],'test_division_1')
            self.assertEquals(division['tournament_name'],'test_tournament_1, test_division_1')
            self.assertEquals(division['active'],False)
            self.assertEquals(division['team_tournament'],False)
            self.assertEquals(division['scoring_type'],"HERB")
            self.assertEquals(division['use_stripe'],False)
            self.assertEquals(division['local_price'],5)
            self.assertEquals(division['finals_num_qualifiers'],24)
                                    
    def test_add_division_no_auth(self):        
        with self.flask_app.test_client() as c:
            self.checkWrongPermissions(c,'post','/division')            
    def test_add_division_wrong_auth(self):        
        with self.flask_app.test_client() as c:
            self.checkWrongPermissions(c,'post','/division', 'test_scorekeeper')
    def test_add_division_with_player_auth(self):        
        with self.flask_app.test_client() as c:
            self.checkWrongPermissions(c,'post','/division', pin=self.new_player.pin)                        
    def test_edit_division_no_auth(self):        
        with self.flask_app.test_client() as c:
            self.checkWrongPermissions(c,'put','/division/1')            
    def test_edit_division_wrong_auth(self):        
        with self.flask_app.test_client() as c:
            self.checkWrongPermissions(c,'put','/division/1', 'test_scorekeeper')            
    def test_edit_division_with_player_auth(self):        
        with self.flask_app.test_client() as c:
            self.checkWrongPermissions(c,'put','/division/1', pin=self.new_player.pin)            

            
