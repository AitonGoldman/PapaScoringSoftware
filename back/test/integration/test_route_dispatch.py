import unittest
import os
from mock import MagicMock
import pss_integration_test_base
import json
from lib import db_util

class RouteDispatch(pss_integration_test_base.PssIntegrationTestBase):
    def setUp(self):
        super(RouteDispatch,self).setUp()        
        
    def test_dispatch(self):
        with self.pss_admin_app.test_client() as c:                        
            rv = c.get('/this_does_not_exist')
            self.assertHttpCodeEquals(rv,404)

