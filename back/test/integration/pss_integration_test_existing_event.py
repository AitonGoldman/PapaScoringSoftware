import json
import pss_integration_test_base
from lib import roles_constants
class PssIntegrationTestExistingEvent(pss_integration_test_base.PssIntegrationTestBase):        
    def setUp(self):
        super(PssIntegrationTestExistingEvent,self).setUp()

    def create_player_for_test(self,app,                               
                               first_name=None,last_name=None,
                               ifpa_ranking=None,
                               extra_title=None):
        if first_name is None:
            first_name=self.create_uniq_id()
        if last_name is None:
            last_name=self.create_uniq_id()
        if ifpa_ranking is None:
            ifpa_ranking=9999
            
        with app.test_client() as c:                                                            
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.admin_pss_user.username,
                                         'password':self.admin_pss_user_password}))
            self.assertHttpCodeEquals(rv,200)                        
            player_dict = {'first_name':first_name,
                           'last_name':last_name,
                           'ifpa_ranking':ifpa_ranking}
            if extra_title:
                player_dict['extra_title']=extra_title
            rv = c.post('/player',
                        data=json.dumps(player_dict))
            self.assertHttpCodeEquals(rv,200)
            return json.loads(rv.data)['new_player']
    
    def create_event_user_for_test(self,app,
                                   username, role_name,
                                   first_name=None,last_name=None,
                                   password=None,extra_title=None):
        with app.test_client() as c:                        
            if password is None:
                password=self.create_uniq_id()
            if first_name is None:
                first_name=self.create_uniq_id()
            if last_name is None:
                last_name=self.create_uniq_id()

            role = self.event_app.tables.EventRoles.query.filter_by(name=role_name).first()
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.admin_pss_user.username,
                                         'password':self.admin_pss_user_password}))
            self.assertHttpCodeEquals(rv,200)            

            rv = c.post('/pss_event_user',
                        data=json.dumps({'username':username,
                                         'password':password,
                                         'first_name':first_name,
                                         'last_name':last_name,
                                         'event_role_id':role.event_role_id}))
            self.assertHttpCodeEquals(rv,200)            
            return json.loads(rv.data)
        
    def create_event_for_test(self,event_name):
        rv = c.post('/auth/pss_user/login',
                    data=json.dumps({'username':self.admin_pss_user.username,'password':self.admin_pss_user_password}))
        self.assertHttpCodeEquals(rv,200)            
        rv = c.post('/event',
                    data=json.dumps({'name':event_name}))
        self.assertHttpCodeEquals(rv,200)
        
    def createEventsAndEventUsers(self):
        #self.new_event_name='newEvent%s'%self.create_uniq_id()
        #self.new_event_name_2='newEvent%s'%self.create_uniq_id()
        self.new_event_name='newEvent'
        self.new_event_name_2='newEventTwo'

        if self.pss_admin_app.tables.Events.query.filter_by(name=self.new_event_name).first():
            #FIXME : should not define these in two places, or make them so generic
            self.event_app = self.get_event_app_in_db(self.new_event_name)
            self.event_app_2 = self.get_event_app_in_db(self.new_event_name_2)
            self.event_user_scorekeeper='eventUserScorekeeper'
            self.event_user_td='eventUserTd'
            self.event_user_scorekeeper_2='eventUserScorekeeper2'
            self.event_user_td_2='eventUserTd2'            
            self.player_one_first_name='playerOneFirstName'
            self.player_two_first_name='playerTwoFirstName'

            return
        
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

        self.event_user_scorekeeper='eventUserScorekeeper'
        self.event_user_td='eventUserTd'
        self.player_one_first_name='playerOneFirstName'
        self.player_one_last_name='test_player_last_name'
        
        self.player_two_first_name='playerTwoFirstName'        
        self.player_two_last_name='test_player_last_name'        
     
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
            created_player = self.create_player_for_test(self.event_app,                               
                                                         first_name=self.player_one_first_name,
                                                         last_name=self.player_one_last_name)
            self.player_one_player_id=created_player['player_id']            
            self.player_one_event_player_id=created_player['event_player']['event_player_id']            
            self.player_one_event_player_pin=created_player['event_player']['event_player_pin']

            created_player = self.create_player_for_test(self.event_app,                               
                                                         first_name=self.player_two_first_name,
                                                         last_name=self.player_two_last_name)
            
            self.assertHttpCodeEquals(rv,200)

        self.event_app_2 = self.get_event_app_in_db(self.new_event_name_2)
        self.event_user_scorekeeper_2='eventUserScorekeeper2'
        self.event_user_td_2='eventUserTd2'

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


    
