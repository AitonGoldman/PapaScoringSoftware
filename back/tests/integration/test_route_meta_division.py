import unittest
import os
from mock import MagicMock
import td_integration_test_base
import json

class RouteMetaDivisionTD(td_integration_test_base.TdIntegrationDispatchTestBase):
    def setUp(self):
        super(RouteMetaDivisionTD,self).setUp()
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

        self.tournament_one = self.flask_app.tables.Tournament(            
            tournament_name='test_tournament_one',
            single_division=True
        )
        self.tournament_two = self.flask_app.tables.Tournament(            
            tournament_name='test_tournament_two',
            single_division=True
        )
        self.tournament_three = self.flask_app.tables.Tournament(            
            tournament_name='test_tournament_three',
            single_division=True
        )                
        self.division_one = self.flask_app.tables.Division(
            division_name='one',            
            tournament_id=1,
            division_id=1,
            tournament=self.tournament_one
        )
        self.division_two = self.flask_app.tables.Division(
            division_name='two',            
            tournament_id=2,
            division_id=2,
            tournament=self.tournament_two
        )
        self.division_three = self.flask_app.tables.Division(
            division_name='three',            
            tournament_id=3,
            division_id=3,
            tournament=self.tournament_three
        )                
        self.flask_app.tables.db_handle.session.add(self.tournament_one)
        self.flask_app.tables.db_handle.session.add(self.tournament_two)
        self.flask_app.tables.db_handle.session.add(self.tournament_three)
        self.flask_app.tables.db_handle.session.add(self.division_one)
        self.flask_app.tables.db_handle.session.add(self.division_two)
        self.flask_app.tables.db_handle.session.add(self.division_three)
        self.flask_app.tables.db_handle.session.commit()

    def test_add_meta_division(self):        
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user.username,'password':'test_admin_password'}))
            rv = c.post('/meta_division',
                        data=json.dumps({'divisions':['1','2'],'meta_division_name':'test_meta_division'}))        
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s' % (rv.status_code))
            meta_division = json.loads(rv.data)['data']
            self.assertTrue('meta_division_id' in meta_division)
            meta_division = self.flask_app.tables.MetaDivision.query.filter_by(meta_division_id=meta_division['meta_division_id']).first()
            self.assertEquals(meta_division.meta_division_name,'test_meta_division')            
            self.assertEquals(len(meta_division.divisions),2)

    def test_edit_meta_division(self):        
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/login',
                       data=json.dumps({'username':self.admin_user.username,'password':'test_admin_password'}))
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

