import unittest
import pss_integration_tests
from lib_v2.PssConfig import PssConfig
from lib_v2 import roles_constants
import json
import random
import os

class PssIntegrationTestBase(unittest.TestCase):                
    def create_uniq_id(self):
        random_string = ""
        for x in range(5):
            random_string = random_string+chr(random.randrange(97,122))        
        return random_string

    def count_users_in_database(self):
        return self.test_app.table_proxy.PssUsers.query.count()

    def count_roles_in_database(self):
        return self.test_app.table_proxy.EventRoles.query.count()
    
    def bootstrap_pss_users(self):        
        self.admin_pss_username='test_user_admin'
        self.normal_pss_username='test_user_normal'

        if self.count_users_in_database()==0:
            add_user_to_session=True
            commit=True
            self.test_app.table_proxy.create_user(self.admin_pss_username,
                                                  'test_first',
                                                  'test_last',
                                                  'password',
                                                  event_creator=True,
                                                  commit=commit,
                                                  add_user_to_session=add_user_to_session)
            self.test_app.table_proxy.create_user(self.normal_pss_username,
                                                  'test_first',
                                                  'test_last',
                                                  'password',
                                                  commit=commit,
                                                  add_user_to_session=add_user_to_session)        
            
    def setUp(self):                
        os.environ['pss_db_name']='test_db'        
        pss_integration_tests.static_setup('test_db')
        self.pss_config = PssConfig()
        self.test_app = pss_integration_tests.test_app                                
        self.bootstrap_pss_users()                
        #FIXME : bootstrapping of users and roles should come from a standard bootstraping function
        if self.count_roles_in_database()==0:
            self.td_event_role_id=self.test_app.table_proxy.create_role(roles_constants.TOURNAMENT_DIRECTOR,True).event_role_id
        else:
            self.td_event_role_id=self.test_app.table_proxy.EventRoles.query.filter_by(event_role_name=roles_constants.TOURNAMENT_DIRECTOR).first().event_role_id
            
    def assertHttpCodeEquals(self,http_response, http_response_code_expected,http_error_message=None):
        if http_error_message:
            expecting_message_string=' and expecting message "%s"'%http_error_message
        else:
            expecting_message_string=''
        error_string = 'Was expecting status code %s %s, but it was %s with message of %s' % (http_response_code_expected, expecting_message_string, http_response.status_code,http_response.data)
        self.assertEquals(http_response.status_code,
                          http_response_code_expected,
                          error_string)
        if http_error_message:
            response_error = json.loads(http_response.data)['message']
            self.assertEquals(response_error,
                              http_error_message,
                              error_string)
        
