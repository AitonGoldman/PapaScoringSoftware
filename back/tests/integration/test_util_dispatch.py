import unittest
from app.util import app_build 
from app.util.dispatch import PathDispatcher
import os
from tempfile import mkstemp
from gunicorn.http.wsgi import Response,WSGIErrorsWrapper, FileWrapper
from gunicorn.http.body import Body
from app.types import ImportedTables
from mock import MagicMock
import td_integration_test_base

class UtilDispatchTD(td_integration_test_base.TdIntegrationDispatchTestBase):
    
    def test_dispatch_admin_first_hit(self):                         
        self.assertFalse(self.poop_db_name in self.app.instances)
        response,results = self.dispatch_request('/%s/util/healthcheck' % self.poop_db_name)
        self.assertTrue(self.poop_db_name in self.app.instances,
                        "App for %s was not instantiated " % self.poop_db_name)
        self.assertEqual(self.admin_health_check_string % "0",results.next(),
                         "Did not recieve a good health check")
        self.assertEqual(response.status,
                         '200 OK',
                         "Expected a response code of 200 but got %s instead" % response.status)           

    def test_dispatch_admin_second_hit(self):
        first_response,first_results = self.dispatch_request('/%s/util/healthcheck' % self.poop_db_name)
        self.assertEqual(self.admin_health_check_string % "0",first_results.next(),
                         "Did not recieve a good health check")
        self.assertEqual(first_response.status,
                         '200 OK',
                         "Expected a response code of 200 but got %s instead" % first_response.status)

        second_response,second_results = self.dispatch_request('/%s/util/healthcheck' % self.poop_db_name)
        self.assertEqual(self.admin_health_check_string % "0",second_results.next(),
                         "Did not recieve a good health check")
        self.assertEqual(second_response.status,
                         '200 OK',
                         "Expected a response code of 200 but got %s instead" % second_response.status)
                        
    def test_dispatch_metaadmin(self):
        self.assertTrue(hasattr(self.app,'default_app'))
        response,results = self.dispatch_request('/meta_admin/healthcheck')        
        self.assertEqual(self.metaadmin_health_check_string,results.next(),
                         "Did not recieve a good health check")
        self.assertEqual(response.status,
                         '200 OK',
                         "Expected a response code of 200 but got %s instead" % response.status)

    def test_dispatch_invalid_route(self):
        self.assertTrue(hasattr(self.app,'default_app'))
        response,results = self.dispatch_request('/does_not_exist/at_all')
        self.assertEqual(response.status,
                         '404 NOT FOUND',
                         "Expected a response code of 404 but got %s instead" % response.status)
        response,results = self.dispatch_request('/meta_admin/at_all')
        self.assertEqual(response.status,
                         '404 NOT FOUND',
                         "Expected a response code of 404 but got %s instead" % response.status)
        
