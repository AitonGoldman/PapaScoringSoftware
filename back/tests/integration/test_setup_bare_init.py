import unittest
import os
from mock import MagicMock
import td_integration_test_base
import json
from routes import orm_creation
from util import db_util
import random

class SetupBareInitTD(td_integration_test_base.TdIntegrationSetupTestBase):
    def setUp(self):
        super(SetupBareInitTD,self).setUp()
        response,results = self.dispatch_request('/%s/util/healthcheck' % self.poop_db_name)                
        self.flask_app = self.app.instances[self.poop_db_name]
        self.admin_user, self.scorekeeper_user,self.desk_user = orm_creation.create_stanard_roles_and_users(self.flask_app)        
        db_util.load_machines_from_json(self.flask_app,False)
                
    def test_setup_before_token(self):        
        pass
