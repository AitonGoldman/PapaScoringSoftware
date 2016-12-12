import unittest
import os
from mock import MagicMock
import td_integration_test_base
import json
from flask_login import current_user
import re
from routes import orm_creation

class RouteIfpaTD(td_integration_test_base.TdIntegrationDispatchTestBase):
    def setUp(self):
        super(RouteIfpaTD,self).setUp()
        response,results = self.dispatch_request('/%s/util/healthcheck' % self.poop_db_name)                
        self.flask_app = self.app.instances[self.poop_db_name]
        orm_creation.create_stanard_roles_and_users(self.flask_app)
        self.admin_user_name='test_admin'
        self.admin_user_password='test_admin'
        
    def test_ifpa_get(self):        
        with self.flask_app.test_client() as c:                    
            rv = c.get('/ifpa/aitongoldman')                        
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code, rv.data))
            ifpa_results = json.loads(rv.data)['data']                        
            self.assertTrue('search' in ifpa_results)
            self.assertEquals(len(ifpa_results['search']),1)
            self.assertTrue('first_name' in ifpa_results['search'][0])
            self.assertEquals(ifpa_results['search'][0]['first_name'],'Aiton')
            


