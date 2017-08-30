import json
import pss_integration_test_base
from lib import roles_constants
class PssIntegrationTestExistingEvent(pss_integration_test_base.PssIntegrationTestBase):        
    def setUp(self):
        super(PssIntegrationTestExistingEvent,self).setUp()        
        self.standard_player_first_name='standardPlayerFirstName'
        self.standard_player_last_name='standardPlayerLastName'        
        self.standard_event_name="standardEvent"                
        self.standard_scorekeeper_username='standardScorkeeper'
        self.standard_td_username='standardTd'
        self.generic_password='password'
        if self.pss_admin_app.tables.Events.query.filter_by(name=self.standard_event_name).first():
            self.event_app = self.get_event_app_in_db(self.standard_event_name)            
            return                
        self.create_event_for_test(self.standard_event_name)
        self.event_app = self.get_event_app_in_db(self.standard_event_name)        
        self.create_event_user_for_test(self.event_app,
                                        self.standard_scorekeeper_username,
                                        password=self.generic_password,
                                        role_name=roles_constants.SCOREKEEPER)['new_pss_user']
        self.create_event_user_for_test(self.event_app,
                                        self.standard_td_username,
                                        password=self.generic_password,
                                        role_name=roles_constants.TOURNAMENT_DIRECTOR)['new_pss_user']
        self.create_player_for_test(self.event_app,
                                    first_name=self.standard_player_first_name,
                                    last_name=self.standard_player_last_name,
                                    ifpa_ranking=9999)
        
    def get_player_id_and_number_and_pin(self,player_first_name,player_last_name,app):
        player = app.tables.Players.query.filter_by(first_name=player_first_name,last_name=player_last_name).first()
        return player.player_id, player.event_player.event_player_id,player.event_player.event_player_pin
        

    def get_existing_event_user(self,username,app):
        return app.tables.PssUsers.query.filter_by(username=username).first()
    
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
        with self.pss_admin_app.test_client() as c:
            rv = c.post('/auth/pss_user/login',
                        data=json.dumps({'username':self.admin_pss_user.username,'password':self.admin_pss_user_password}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.post('/event',
                        data=json.dumps({'name':event_name}))
            self.assertHttpCodeEquals(rv,200)
        
    def createEventsAndEventUsers(self):        
        return
