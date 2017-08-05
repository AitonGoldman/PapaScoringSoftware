import unittest
import os
from mock import MagicMock
import td_integration_test_base
import json
from flask_login import current_user
import re
from sqlalchemy_utils import database_exists

class RouteUtilTD(td_integration_test_base.TdIntegrationDispatchTestBase):
    def setUp(self):
        super(RouteUtilTD,self).setUp()
        self.dispatch_request('/%s/util/healthcheck' % self.poop_db_name)
        self.flask_app = self.app.instances[self.poop_db_name]
        self.meta_admin_flask_app = self.app.default_app

    def test_healthcheck(self):
        with self.flask_app.test_client() as c:
            rv = c.get('/util/healthcheck')
            self.assertEquals(rv.data,self.admin_health_check_string % "0")

    def test_meta_admin_healthcheck(self):
        with self.meta_admin_flask_app.test_client() as c:
            rv = c.get('/meta_admin/healthcheck')
            self.assertEquals(rv.data,self.metaadmin_health_check_string)
