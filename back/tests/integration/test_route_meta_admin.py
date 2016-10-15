import unittest
import os
from mock import MagicMock
import td_integration_test_base
import json
from flask_login import current_user
import re
from sqlalchemy_utils import database_exists

class RouteMetaAdminTD(td_integration_test_base.TdIntegrationDispatchTestBase):
    def setUp(self):
        super(RouteMetaAdminTD,self).setUp()        
        self.flask_app = self.app.default_app        
        
    def test_db_create(self):        
        with self.flask_app.test_client() as c:                    
            rv = c.post('/meta_admin/db',
                        data=json.dumps({'db_name':'test_db'}))            
            db_url = 'sqlite:////%s' % self.poop_db_file_name            
            self.assertTrue(database_exists(db_url),
                            "Database %s does not exist" % self.poop_db_name)            
        response,results = self.dispatch_request('/%s/util/healthcheck' % self.poop_db_name)                
        created_app = self.app.instances[self.poop_db_name]
        self.assertTrue(hasattr(created_app,'tables'),
                        "Database %s does not exist" % self.poop_db_name)            

    def test_db_test_create(self):        
        test_db_file = open('/tmp/test.db','w')
        test_db_file.close()

        with self.flask_app.test_client() as c:                    
            rv = c.post('/meta_admin/test_db')            
            db_url = 'sqlite:////%s' % '/tmp/test.db'
            self.assertTrue(database_exists(db_url),
                            "Database %s does not exist" % 'test')            
        response,results = self.dispatch_request('/%s/util/healthcheck' % 'test')                
        created_app = self.app.instances['test']
        self.assertTrue(hasattr(created_app,'tables'),
                        "Database %s does not exist" % 'test')            
        
            

