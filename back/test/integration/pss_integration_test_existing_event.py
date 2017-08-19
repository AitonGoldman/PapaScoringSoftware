import json
import pss_integration_test_base
from lib import roles_constants
class PssIntegrationTestExistingEvent(pss_integration_test_base.PssIntegrationTestBase):        
    def setUp(self):
        super(PssIntegrationTestExistingEvent,self).setUp()
        
    def createEventsAndEventUsers(self):
        self.new_event_name='newEvent%s'%self.create_uniq_id()
        self.new_event_name_2='newEvent%s'%self.create_uniq_id()
        
        with self.pss_admin_app.test_client() as c:            
            rv = c.post('/auth/pss_user/login',
                        data=json.dumps({'username':self.admin_pss_user.username,'password':self.admin_pss_user_password}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.post('/event',
                       data=json.dumps({'name':self.new_event_name}))
            self.assertHttpCodeEquals(rv,200)
            rv = c.post('/event',
                       data=json.dumps({'name':self.new_event_name_2}))
            self.assertHttpCodeEquals(rv,200)
            
        self.event_app = self.get_event_app_in_db(self.new_event_name)

        self.event_user_scorekeeper='eventUserScorekeeper%s'%self.create_uniq_id()        
        self.event_user_td='eventUserTd%s'%self.create_uniq_id()        
        
        with self.event_app.test_client() as c:                        
            scorekeeper_role = self.event_app.tables.EventRoles.query.filter_by(name=roles_constants.SCOREKEEPER).first()
            td_role = self.event_app.tables.EventRoles.query.filter_by(name=roles_constants.TOURNAMENT_DIRECTOR).first()
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.admin_pss_user.username,
                                         'password':self.admin_pss_user_password}))
            self.assertHttpCodeEquals(rv,200)            

            rv = c.post('/pss_event_user',
                        data=json.dumps({'username':self.event_user_scorekeeper,
                                         'password':'password',
                                         'first_name':'test_event_sc_first_name',
                                         'last_name':'test_event_sc_last_name',
                                         'event_role_id':scorekeeper_role.event_role_id}))
            self.assertHttpCodeEquals(rv,200)
            rv = c.post('/pss_event_user',
                        data=json.dumps({'username':self.event_user_td,
                                         'password':'password',
                                         'first_name':'test_event_td_first_name',
                                         'last_name':'test_event_td_last_name',
                                         'event_role_id':td_role.event_role_id}))
            self.assertHttpCodeEquals(rv,200)            
            
        
        self.event_app_2 = self.get_event_app_in_db(self.new_event_name_2)
        self.event_user_scorekeeper_2='eventUserScorekeeper%s'%self.create_uniq_id()
        self.event_user_td_2='eventUserTd%s'%self.create_uniq_id()
        
        with self.event_app_2.test_client() as c:                        
            scorekeeper_role = self.event_app.tables.EventRoles.query.filter_by(name=roles_constants.SCOREKEEPER).first()
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.admin_pss_user.username,
                                         'password':self.admin_pss_user_password}))
            self.assertHttpCodeEquals(rv,200)                        
            rv = c.post('/pss_event_user',
                        data=json.dumps({'username':self.event_user_scorekeeper_2,
                                         'password':'password',
                                         'first_name':'test_event_2_sc_first_name',
                                         'last_name':'test_event_2_sc_last_name',                                         
                                         'event_role_id':scorekeeper_role.event_role_id}))
            self.assertHttpCodeEquals(rv,200)                        
            rv = c.post('/pss_event_user',
                        data=json.dumps({'username':self.event_user_td_2,
                                         'password':'password',
                                         'first_name':'test_event_2_td_first_name',
                                         'last_name':'test_event_2_td_last_name',                                         
                                         'event_role_id':td_role.event_role_id}))
            
            self.assertHttpCodeEquals(rv,200)            
        

    
