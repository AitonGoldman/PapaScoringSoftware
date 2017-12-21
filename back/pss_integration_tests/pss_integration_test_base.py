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
                                                  commit=True)
            self.test_app.table_proxy.create_user(self.normal_pss_username,
                                                  'test_first',
                                                  'test_last',
                                                  'password',
                                                  commit=True)
            
    def login_and_create_tournament_machine(self,login_dict, post_dict, event_id, event_user=False):
        with self.test_app.test_client() as c:
            if event_user:
                login_endpoint='/auth/pss_event_user/login'
            else:
                login_endpoint='/auth/pss_user/login'
            rv = c.post(login_endpoint,
                        data=json.dumps(login_dict))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.post('/%s/tournament_machine' % event_id,
                        data=json.dumps(post_dict))
            self.assertHttpCodeEquals(rv,200)
            return json.loads(rv.data)

    def login_and_edit_tournament_machine(self,login_dict, post_dict, event_id, event_user=False):
        with self.test_app.test_client() as c:
            if event_user:
                login_endpoint='/auth/pss_event_user/login'
            else:
                login_endpoint='/auth/pss_user/login'
            rv = c.post(login_endpoint,
                        data=json.dumps(login_dict))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.put('/%s/tournament_machine' % event_id,
                       data=json.dumps(post_dict))
            self.assertHttpCodeEquals(rv,200)
            return json.loads(rv.data)
        
    def login_and_create_tournament(self,login_dict, post_dict, event_id, event_user=False):
        with self.test_app.test_client() as c:
            if event_user:
                login_endpoint='/auth/pss_event_user/login'
            else:
                login_endpoint='/auth/pss_user/login'
            rv = c.post(login_endpoint,
                        data=json.dumps(login_dict))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.post('/%s/tournament' % event_id,
                        data=json.dumps(post_dict))
            self.assertHttpCodeEquals(rv,200)
            return json.loads(rv.data)

    def login_and_create_meta_tournament(self,login_dict, post_dict, event_id, event_user=False):
        with self.test_app.test_client() as c:
            if event_user:
                login_endpoint='/auth/pss_event_user/login'
            else:
                login_endpoint='/auth/pss_user/login'
            rv = c.post(login_endpoint,
                        data=json.dumps(login_dict))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.post('/%s/meta_tournament' % event_id,
                        data=json.dumps(post_dict))
            self.assertHttpCodeEquals(rv,200)
            return json.loads(rv.data)
        
    def login_and_edit_meta_tournament(self,login_dict, post_dict, event_id, event_user=False):
        with self.test_app.test_client() as c:
            if event_user:
                login_endpoint='/auth/pss_event_user/login'
            else:
                login_endpoint='/auth/pss_user/login'
            rv = c.post(login_endpoint,
                        data=json.dumps(login_dict))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.put('/%s/meta_tournament' % (event_id),
                        data=json.dumps(post_dict))
            self.assertHttpCodeEquals(rv,200)
            return json.loads(rv.data)

    def login_and_edit_tournament(self,login_dict, post_dict, event_id, event_user=False):
        with self.test_app.test_client() as c:
            if event_user:
                login_endpoint='/auth/pss_event_user/login'
            else:
                login_endpoint='/auth/pss_user/login'
            rv = c.post(login_endpoint,
                        data=json.dumps(login_dict))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.put('/%s/tournament' % (event_id),
                        data=json.dumps(post_dict))
            self.assertHttpCodeEquals(rv,200)
            return json.loads(rv.data)

    def login_and_create_event_and_create_event_player(self,login_dict, post_dict):
        with self.test_app.test_client() as c:

            rv = c.post('/auth/pss_user/login',
                        data=json.dumps(login_dict))
            self.assertHttpCodeEquals(rv,200)
            event_name = 'test_event_'+self.create_uniq_id()
            rv = c.post('/event',
                        data=json.dumps({'name':event_name}))
            self.assertHttpCodeEquals(rv,200)
            results = json.loads(rv.data)
            event_id = results['data']['event_id']            
            rv = c.post('/%s/player' % event_id,
                        data=json.dumps(post_dict))
            self.assertHttpCodeEquals(rv,200)
            return [event_id,json.loads(rv.data)]

    def login_and_create_event_player(self,login_dict, post_dict,event_id):
        with self.test_app.test_client() as c:

            rv = c.post('/auth/pss_user/login',
                        data=json.dumps(login_dict))
            self.assertHttpCodeEquals(rv,200)
            rv = c.post('/%s/player' % event_id,
                        data=json.dumps(post_dict))
            self.assertHttpCodeEquals(rv,200)
            return json.loads(rv.data)

    def login_and_add_player_to_queue(self,login_dict, post_dict,event_id):
        with self.test_app.test_client() as c:
            rv = c.post('/auth/pss_user/login',
                        data=json.dumps(login_dict))
            self.assertHttpCodeEquals(rv,200)
            rv = c.post('/%s/queue' % event_id,
                        data=json.dumps(post_dict))
            self.assertHttpCodeEquals(rv,200)
            return json.loads(rv.data)
        
    def login_and_remove_player_from_queue(self,login_dict, post_dict,event_id):
        with self.test_app.test_client() as c:
            rv = c.post('/auth/pss_user/login',
                        data=json.dumps(login_dict))
            self.assertHttpCodeEquals(rv,200)
            rv = c.delete('/%s/queue' % event_id,
                          data=json.dumps(post_dict))
            self.assertHttpCodeEquals(rv,200)
            return json.loads(rv.data)
    def login_and_bump_player_down_queue(self,login_dict, post_dict,event_id):
        with self.test_app.test_client() as c:
            rv = c.post('/auth/pss_user/login',
                        data=json.dumps(login_dict))
            self.assertHttpCodeEquals(rv,200)
            rv = c.put('/%s/queue' % event_id,
                          data=json.dumps(post_dict))
            self.assertHttpCodeEquals(rv,200)
            return json.loads(rv.data)
        
        
    def login_and_purchase_tickets(self,login_dict,post_dict,event_id,event_user=False):
        if event_user:
            login_endpoint='/auth/pss_event_user/login'
        else:
            login_endpoint='/auth/pss_user/login'
        with self.test_app.test_client() as c:            
            rv = c.post(login_endpoint,
                        data=json.dumps(login_dict))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.post('/%s/token' % (event_id),
                        data=json.dumps(post_dict))            
        
    
    def login_and_create_event_and_create_event_user(self,login_dict, post_dict):
        with self.test_app.test_client() as c:

            rv = c.post('/auth/pss_user/login',
                        data=json.dumps(login_dict))
            self.assertHttpCodeEquals(rv,200)
            event_name = 'test_event_'+self.create_uniq_id()
            rv = c.post('/event',
                        data=json.dumps({'name':event_name}))
            self.assertHttpCodeEquals(rv,200)
            results = json.loads(rv.data)
            event_id = results['data']['event_id']            
            rv = c.post('/%s/event_user' % event_id,
                        data=json.dumps(post_dict))
            self.assertHttpCodeEquals(rv,200)
            return [event_id,json.loads(rv.data)]
           
    def setUp(self):                
        os.environ['pss_db_name']='test_db'        
        pss_integration_tests.static_setup('test_db')
        self.pss_config = PssConfig()
        self.test_app = pss_integration_tests.test_app                                
        self.bootstrap_pss_users()                
        #FIXME : bootstrapping of users and roles should come from a standard bootstraping function
        if self.count_roles_in_database()==0:
            self.test_app.table_proxy.create_role(roles_constants.TOURNAMENT_DIRECTOR,True)
            self.test_app.table_proxy.create_role(roles_constants.SCOREKEEPER,True)
        
        self.td_event_role_id=self.test_app.table_proxy.EventRoles.query.filter_by(event_role_name=roles_constants.TOURNAMENT_DIRECTOR).first().event_role_id
        self.scorekeeper_role_id=self.test_app.table_proxy.EventRoles.query.filter_by(event_role_name=roles_constants.SCOREKEEPER).first().event_role_id
        #self.event_creator_role_id=self.test_app.table_proxy.EventRoles.query.filter_by(event_role_name=roles_constants.EVENT_CREATOR).first().event_role_id
            
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
        
