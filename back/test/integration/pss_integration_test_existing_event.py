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

        self.event_user='eventUser%s'%self.create_uniq_id()
        
        with self.event_app.test_client() as c:                        
            scorekeeper_role = self.event_app.tables.EventRoles.query.filter_by(name=roles_constants.SCOREKEEPER).first()
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.admin_pss_user.username,
                                         'password':self.admin_pss_user_password}))
            self.assertHttpCodeEquals(rv,200)            

            rv = c.post('/pss_user',
                        data=json.dumps({'username':self.event_user,
                                         'password':'password',
                                         'event_role_id':scorekeeper_role.event_role_id}))
            self.assertHttpCodeEquals(rv,200)            
        
        self.event_app_2 = self.get_event_app_in_db(self.new_event_name_2)
        self.event_user_2='eventUser%s'%self.create_uniq_id()
        with self.event_app_2.test_client() as c:                        
            scorekeeper_role = self.event_app.tables.EventRoles.query.filter_by(name=roles_constants.SCOREKEEPER).first()
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.admin_pss_user.username,
                                         'password':self.admin_pss_user_password}))
            self.assertHttpCodeEquals(rv,200)            

            rv = c.post('/pss_user',
                        data=json.dumps({'username':self.event_user_2,
                                         'password':'password',
                                         'event_role_id':scorekeeper_role.event_role_id}))
            self.assertHttpCodeEquals(rv,200)            
        

    
