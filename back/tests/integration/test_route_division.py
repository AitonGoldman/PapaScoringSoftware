import unittest
import os
from mock import MagicMock
import td_integration_test_base
import json

class RouteDivisionTD(td_integration_test_base.TdIntegrationDispatchTestBase):
    def setUp(self):
        super(RouteDivisionTD,self).setUp()
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

        self.desk_role = self.flask_app.tables.Role(name='desk')
        self.flask_app.tables.db_handle.session.add(self.desk_role)
        self.flask_app.tables.db_handle.session.commit()        
        self.desk_user = self.flask_app.tables.User(username='test_desk')
        self.desk_user.crypt_password('test_desk')
        self.desk_user.roles.append(self.desk_role)
        self.flask_app.tables.db_handle.session.add(self.desk_user)
        self.flask_app.tables.db_handle.session.commit()
        

    def test_add_division(self):        
        new_tournament = self.flask_app.tables.Tournament(
            tournament_name='test_tournament_1',
            single_division=True
        )
        self.flask_app.tables.db_handle.session.add(new_tournament)
        self.flask_app.tables.db_handle.session.commit()
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user.username,'password':'test_admin_password'}))
            rv = c.post('/division',
                        data=json.dumps({'division_name':'test_division_1',
                                         'scoring_type':'HERB',
                                         'finals_num_qualifiers':24,
                                         'active':False,
                                         'team_tournament':False,
                                         'use_stripe':True,
                                         'stripe_sku':'poop',
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
            self.assertEquals(division.stripe_sku,"poop")
            self.assertEquals(division.finals_num_qualifiers,24)

    def test_add_duplicate_division(self):        
        new_tournament = self.flask_app.tables.Tournament(
            tournament_name='test_tournament_1',
            single_division=True
        )
        self.flask_app.tables.db_handle.session.add(new_tournament)
        self.flask_app.tables.db_handle.session.commit()
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user.username,'password':'test_admin_password'}))
            rv = c.post('/division',
                        data=json.dumps({'division_name':'test_division_1',
                                         'scoring_type':'HERB',
                                         'finals_num_qualifiers':24,
                                         'active':False,
                                         'team_tournament':False,
                                         'use_stripe':True,
                                         'stripe_sku':'poop',
                                         'tournament_id':new_tournament.tournament_id
                        }))        
            rv = c.post('/division',
                        data=json.dumps({'division_name':'test_division_1',
                                         'scoring_type':'HERB',
                                         'finals_num_qualifiers':24,
                                         'active':False,
                                         'team_tournament':False,
                                         'use_stripe':True,
                                         'stripe_sku':'poop',
                                         'tournament_id':new_tournament.tournament_id
                        }))        

            self.assertEquals(rv.status_code,
                              409,
                              'Was expecting status code 409, but it was %s' % (rv.status_code))
            
    def test_edit_division(self):        
        new_tournament = self.flask_app.tables.Tournament(
            tournament_name='test_tournament_1',
            single_division=True
        )
        self.flask_app.tables.db_handle.session.add(new_tournament)
        self.flask_app.tables.db_handle.session.commit()
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user.username,'password':'test_admin_password'}))
            rv = c.post('/division',
                        data=json.dumps({'division_name':'test_division_1',
                                         'scoring_type':'HERB',
                                         'finals_num_qualifiers':24,
                                         'active':False,
                                         'team_tournament':False,
                                         'use_stripe':True,
                                         'stripe_sku':'poop',
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
                                         'local_price':5,
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
            self.assertEquals(division.local_price,5)
            self.assertEquals(division.finals_num_qualifiers,14)

    def test_get_divisions(self):        
        new_tournament = self.flask_app.tables.Tournament(
            tournament_name='test_tournament_1',
            single_division=True
        )
        new_tournament_two = self.flask_app.tables.Tournament(
            tournament_name='test_tournament_2',
            single_division=True
        )
        
        self.flask_app.tables.db_handle.session.add(new_tournament)
        self.flask_app.tables.db_handle.session.add(new_tournament_two)
        self.flask_app.tables.db_handle.session.commit()
        new_division = self.flask_app.tables.Division(
            division_name='test_division_1',
            active=False,
            team_tournament=False,
            scoring_type="HERB",
            use_stripe=True,
            stripe_sku="1234",
            finals_num_qualifiers=24
        )
        new_division_two = self.flask_app.tables.Division(
            division_name='test_division_2',
            active=False,
            team_tournament=False,
            scoring_type="HERB",
            use_stripe=True,
            stripe_sku="1234",
            finals_num_qualifiers=24
        )
        
        self.flask_app.tables.db_handle.session.add(new_division)
        self.flask_app.tables.db_handle.session.add(new_division_two)
        self.flask_app.tables.db_handle.session.commit()
        
        new_tournament.divisions.append(new_division)
        self.flask_app.tables.db_handle.session.commit()

        new_tournament_two.divisions.append(new_division_two)
        self.flask_app.tables.db_handle.session.commit()
        
        with self.flask_app.test_client() as c:                                
            rv = c.get('/division')
            
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s' % (rv.status_code))
            division = json.loads(rv.data)['data']
            self.assertEquals(len(division.keys()),2)
            
            
    def test_get_division(self):        
        new_tournament = self.flask_app.tables.Tournament(
            tournament_name='test_tournament_1',
            single_division=True
        )
        multi_div_tournament = self.flask_app.tables.Tournament(
            tournament_name='test_tournament_2',
            single_division=False
        )
        self.flask_app.tables.db_handle.session.add(new_tournament)
        self.flask_app.tables.db_handle.session.add(multi_div_tournament)
        self.flask_app.tables.db_handle.session.commit()
        new_division = self.flask_app.tables.Division(
            division_name='test_division_1',
            active=False,
            team_tournament=False,
            scoring_type="HERB",
            use_stripe=True,
            stripe_sku="1234",
            finals_num_qualifiers=24
        )
        self.flask_app.tables.db_handle.session.add(new_division)
        self.flask_app.tables.db_handle.session.commit()
        
        new_tournament.divisions.append(new_division)
        self.flask_app.tables.db_handle.session.commit()

        with self.flask_app.test_client() as c:                                
            rv = c.get('/division/%s' % new_division.division_id)
            
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s' % (rv.status_code))
            division = json.loads(rv.data)['data']
            self.assertIsNotNone(division,
                                 "Could not find the division we just created")
            self.assertEquals(division['division_name'],'test_division_1')
            self.assertEquals(division['tournament_name'],'test_tournament_1')
            self.assertEquals(division['active'],False)
            self.assertEquals(division['team_tournament'],False)
            self.assertEquals(division['scoring_type'],"HERB")
            self.assertEquals(division['use_stripe'],True)
            self.assertEquals(division['stripe_sku'],"1234")
            self.assertEquals(division['finals_num_qualifiers'],24)
                        
    def test_edit_division_no_auth(self):        
        new_tournament = self.flask_app.tables.Tournament(
            tournament_name='test_tournament_1',
            single_division=True
        )
        self.flask_app.tables.db_handle.session.add(new_tournament)
        self.flask_app.tables.db_handle.session.commit()
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user.username,'password':'test_admin_password'}))
            rv = c.post('/division',
                        data=json.dumps({'division_name':'test_division_1',
                                         'scoring_type':'HERB',
                                         'finals_num_qualifiers':24,
                                         'active':False,
                                         'team_tournament':False,
                                         'use_stripe':True,
                                         'stripe_sku':'poop',
                                         'tournament_id':new_tournament.tournament_id
                        }))
        division = json.loads(rv.data)['data']                        
        with self.flask_app.test_client() as c:                    
            rv = c.put('/division/%s'%division['division_id'],
                        data=json.dumps({'scoring_type':'PAPA',
                                         'division_id':division['division_id'],
                                         'finals_num_qualifiers':14,
                                         'active':True,
                                         'team_tournament':True,
                                         'use_stripe':False,
                                         'local_price':5,
                                         'tournament_id':new_tournament.tournament_id
                        }))                    
            self.assertEquals(rv.status_code,
                              401,
                              'Was expecting status code 401, but it was %s' % (rv.status_code))
            
            
    def test_add_division_no_auth(self):        
        new_tournament = self.flask_app.tables.Tournament(
            tournament_name='test_tournament_1',
            single_division=True
        )
        self.flask_app.tables.db_handle.session.add(new_tournament)
        self.flask_app.tables.db_handle.session.commit()
        with self.flask_app.test_client() as c:                    
            rv = c.post('/division',
                        data=json.dumps({'division_name':'test_division_1',
                                         'scoring_type':'HERB',
                                         'finals_num_qualifiers':24,
                                         'active':False,
                                         'team_tournament':False,
                                         'use_stripe':True,
                                         'stripe_sku':'poop',
                                         'tournament_id':new_tournament.tournament_id
                        }))        
            self.assertEquals(rv.status_code,
                              401,
                              'Was expecting status code 401, but it was %s' % (rv.status_code))


    def test_edit_division_wrong_auth(self):        
        new_tournament = self.flask_app.tables.Tournament(
            tournament_name='test_tournament_1',
            single_division=True
        )
        self.flask_app.tables.db_handle.session.add(new_tournament)
        self.flask_app.tables.db_handle.session.commit()
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user.username,'password':'test_admin_password'}))
            rv = c.post('/division',
                        data=json.dumps({'division_name':'test_division_1',
                                         'scoring_type':'HERB',
                                         'finals_num_qualifiers':24,
                                         'active':False,
                                         'team_tournament':False,
                                         'use_stripe':True,
                                         'stripe_sku':'poop',
                                         'tournament_id':new_tournament.tournament_id
                        }))
        division = json.loads(rv.data)['data']                        
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                   data=json.dumps({'username':'test_desk','password':'test_desk'}))

            rv = c.put('/division/%s'%division['division_id'],
                        data=json.dumps({'scoring_type':'PAPA',
                                         'division_id':division['division_id'],
                                         'finals_num_qualifiers':14,
                                         'active':True,
                                         'team_tournament':True,
                                         'use_stripe':False,
                                         'local_price':5,
                                         'tournament_id':new_tournament.tournament_id
                        }))                    
            self.assertEquals(rv.status_code,
                              403,
                              'Was expecting status code 403, but it was %s' % (rv.status_code))
            
            
    def test_add_division_wrong_auth(self):        
        new_tournament = self.flask_app.tables.Tournament(
            tournament_name='test_tournament_1',
            single_division=True
        )
        self.flask_app.tables.db_handle.session.add(new_tournament)
        self.flask_app.tables.db_handle.session.commit()
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                   data=json.dumps({'username':'test_desk','password':'test_desk'}))

            rv = c.post('/division',
                        data=json.dumps({'division_name':'test_division_1',
                                         'scoring_type':'HERB',
                                         'finals_num_qualifiers':24,
                                         'active':False,
                                         'team_tournament':False,
                                         'use_stripe':True,
                                         'stripe_sku':'poop',
                                         'tournament_id':new_tournament.tournament_id
                        }))        
            self.assertEquals(rv.status_code,
                              403,
                              'Was expecting status code 403, but it was %s' % (rv.status_code))
            
            
