import json
import pss_integration_test_existing_event
from lib import roles_constants
class PssIntegrationTestExistingTournamentAndMetaTournament(pss_integration_test_existing_event.PssIntegrationTestExistingEvent):        
    def setUp(self):
        super(PssIntegrationTestExistingTournamentAndMetaTournament,self).setUp()
        self.createEventsAndEventUsers()
        self.createTournament()

    def createTeamAndAddPlayers(self,team_name,player_id_1,player_id_2,app):
        #FIXME : this should use real routes once they exist
        with app.test_client() as c:            
            new_team = app.tables.Teams()        
            app.tables.db_handle.session.add(new_team)            
            player_1 = app.tables.Players.query.filter_by(player_id=player_id_1).first()
            player_2 = app.tables.Players.query.filter_by(player_id=player_id_2).first()                                
            new_team.event_players.append(player_1.event_player)
            new_team.event_players.append(player_2.event_player)            
            app.tables.db_handle.session.commit()
        return new_team.team_id

    def createTournamentMachine(self):
        with self.event_app.test_client() as c:            
            existing_machines = self.event_app.tables.TournamentMachines.query.order_by(self.event_app.tables.TournamentMachines.machine_id).all()
            if existing_machines:
                new_machine_id=existing_machines[-1].machine_id+1
            else:
                new_machine_id=1
            existing_tournament = self.event_app.tables.Tournaments.query.filter_by(tournament_id=1).first()
            existing_tournament.queue_size=3
            self.event_app.tables.db_handle.session.commit()
            
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.standard_td_username,
                                         'password':self.generic_password}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.post('/tournament_machine',
                        data=json.dumps({'tournament_id':1,
                                         'machine_id':new_machine_id}))
            self.assertHttpCodeEquals(rv,200)            
            return json.loads(rv.data)['new_tournament_machine']
        
    
    def createTournament(self):
        self.new_tournament_name='newTournament'
        self.new_tournament_name2='newTournament2'
        self.new_tournament_name3='newTournament3'
        self.new_tournament_with_manual_discount_name='newTournamentWithManualDiscount'
        self.new_team_tournament='newTeamTournament'
        
        self.new_meta_tournament_name_='newMetaTournament'
        with self.event_app.test_client() as c:
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.standard_td_username,
                                         'password':self.generic_password}))
            self.player_name_with_no_tokens = 'player_with_no_tokens_%s' % self.create_uniq_id()
            rv = c.post('/player',
                    data=json.dumps({'first_name':self.player_name_with_no_tokens,
                                         'last_name':'test_player_last_name',
                                         'ifpa_ranking':9999}))
            self.assertHttpCodeEquals(rv,200)
            self.player_id_with_no_tokens=json.loads(rv.data)['new_player']['player_id']
            self.player_with_no_tokens=self.event_app.tables.Players.query.filter_by(player_id=self.player_id_with_no_tokens).first()
            self.player_event_id_with_no_tokens=self.player_with_no_tokens.event_player.event_player_id
            self.player_event_pin_with_no_tokens=self.player_with_no_tokens.event_player.event_player_pin
            
        if self.event_app.tables.Tournaments.query.filter_by(tournament_name=self.new_tournament_name).first():
            return

        with self.event_app.test_client() as c:                        
            rv = c.post('/auth/pss_event_user/login',
                        data=json.dumps({'username':self.standard_td_username,
                                         'password':self.generic_password}))
            self.assertHttpCodeEquals(rv,200)                        
            rv = c.post('/tournament',
                        data=json.dumps({'tournament_name':self.new_tournament_name}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.post('/tournament',
                        data=json.dumps({'tournament_name':self.new_tournament_name2}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.post('/tournament',
                        data=json.dumps({'tournament_name':self.new_tournament_name3}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.post('/meta_tournament',
                        data=json.dumps({'meta_tournament_name':self.new_tournament_name3,'tournament_ids':[2,3]}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.post('/tournament',
                        data=json.dumps({'tournament_name':self.new_tournament_with_manual_discount_name}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.put('/tournament/4',
                        data=json.dumps({'number_of_tickets_for_discount':3,'discount_price':40}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.post('/tournament',
                        data=json.dumps({'tournament_name':self.new_team_tournament}))
            self.assertHttpCodeEquals(rv,200)            
            rv = c.put('/tournament/5',
                        data=json.dumps({'team_tournament':True}))
            self.assertHttpCodeEquals(rv,200)            
            
        


    
