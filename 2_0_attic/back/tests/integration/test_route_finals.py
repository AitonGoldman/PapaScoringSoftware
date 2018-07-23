import unittest
import os
from mock import MagicMock
import td_integration_test_base
import json
from routes import orm_creation
from util import db_util

class RouteFinalsTD(td_integration_test_base.TdIntegrationDispatchTestBase):
    def setUp(self):
        super(RouteFinalsTD,self).setUp()
        response,results = self.dispatch_request('/%s/util/healthcheck' % self.poop_db_name)                
        self.flask_app = self.app.instances[self.poop_db_name]
        self.admin_user, self.scorekeeper_user,self.desk_user = orm_creation.create_stanard_roles_and_users(self.flask_app)
        #FIXME : password/username should be passed in to create_roles_and_users()
        self.score_user_name_password='test_scorekeeper'
        self.admin_user_name_password='test_admin'        
        db_util.load_machines_from_json(self.flask_app,True)        
        orm_creation.init_papa_tournaments_divisions(self.flask_app)        

        self.machine = self.flask_app.tables.Machine.query.filter_by(machine_id=1).first()
        self.division_machines = []
        self.team_division_machines = []
        
        self.players = []
        self.teams = []
        self.flask_app.tables.db_handle.session.commit()
        for i in range(100,140):
            self.players.append(orm_creation.create_player(self.flask_app,{'first_name':'test','last_name':'player%s'%i,'ifpa_ranking':'123','linked_division_id':'1'}))
        for i in range(100,110):
            for division in self.flask_app.tables.Division.query.filter_by(team_tournament=False).all():
                self.division_machines.append(orm_creation.create_division_machine(self.flask_app,self.machine,division))
            for division in self.flask_app.tables.Division.query.filter_by(team_tournament=True).all():
                self.team_division_machines.append(orm_creation.create_division_machine(self.flask_app,self.machine,division))
                
        self.division = self.flask_app.tables.Division.query.filter_by(team_tournament=False).all()[0]
        self.team_division = self.flask_app.tables.Division.query.filter_by(team_tournament=True).all()[0]
        
        for i in range(100,110,2):            
            self.teams.append(orm_creation.create_team(self.flask_app,{
                'team_name':'test_team_%s'%i,
                'players':['%s'%i,'%s'%(i+1)]
            }))

    
    def populate_scores_for_finals_testing(self,with_ties=True,max_players=20,tie_increment=2):
        for division_machine in self.flask_app.tables.DivisionMachine.query.filter_by(division_id=self.division.division_id).all():            
            score=100+tie_increment
            player_id=100
            if with_ties:
                increment=tie_increment
            else:
                increment=1
            while score <= 100+max_players:                
                orm_creation.create_entry(self.flask_app,division_machine.division_machine_id,self.division.division_id,score,player_id)                
                player_id=player_id+1
                if with_ties:                    
                    for index in range(tie_increment-1):
                        orm_creation.create_entry(self.flask_app,division_machine.division_machine_id,self.division.division_id,score,player_id)                        
                        player_id=player_id+1
                score=score+increment
                
    def test_division_final_initialize(self):        
        self.division.finals_num_qualifiers = 8
        self.flask_app.tables.db_handle.session.commit()
        self.populate_scores_for_finals_testing()
        
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_admin','password':'test_admin'}))
            rv = c.post('/finals/division_final/division_id/%s'%self.division.division_id)
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            
            division_final_returned = json.loads(rv.data)['data']
            self.assertEquals(division_final_returned['division_final_id'],1)

    def test_division_final_get_important_tiebreakers_with_ties(self):        
        self.division.finals_num_qualifiers = 12
        self.flask_app.tables.db_handle.session.commit()
        self.populate_scores_for_finals_testing(tie_increment=5)
        
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_admin','password':'test_admin'}))
            rv = c.post('/finals/division_final/division_id/%s'%self.division.division_id)
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            
            division_final_returned = json.loads(rv.data)['data']
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_scorekeeper','password':'test_scorekeeper'}))            
            rv = c.get('/finals/division_final/division_id/%s/tiebreakers/important'%division_final_returned['division_final_id'])
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            
            important_tiebreakers_returned = json.loads(rv.data)['data']                        
            self.assertEquals(important_tiebreakers_returned['important_tiebreakers']['qualifying'],10)            
            self.assertEquals(important_tiebreakers_returned['important_tiebreakers']['bye'],0)

    def test_division_final_get_important_tiebreakers_without_ties(self):        
        self.division.finals_num_qualifiers = 12
        self.flask_app.tables.db_handle.session.commit()
        self.populate_scores_for_finals_testing(with_ties=False)
        
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_admin','password':'test_admin'}))
            rv = c.post('/finals/division_final/division_id/%s'%self.division.division_id)
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            
            division_final_returned = json.loads(rv.data)['data']
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_scorekeeper','password':'test_scorekeeper'}))            
            rv = c.get('/finals/division_final/division_id/%s/tiebreakers/important'%division_final_returned['division_final_id'])
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            
            important_tiebreakers_returned = json.loads(rv.data)['data']                        
            self.assertFalse('qualifying' in important_tiebreakers_returned['important_tiebreakers'])
            self.assertFalse('bye' in important_tiebreakers_returned['important_tiebreakers'])
 
            
            
    def test_division_final_get_tiebreakers_with_ties(self):        
        self.division.finals_num_qualifiers = 8
        self.flask_app.tables.db_handle.session.commit()
        self.populate_scores_for_finals_testing()
        
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_admin','password':'test_admin'}))
            rv = c.post('/finals/division_final/division_id/%s'%self.division.division_id)
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            
            division_final_returned = json.loads(rv.data)['data']
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_scorekeeper','password':'test_scorekeeper'}))            
            rv = c.get('/finals/division_final/division_id/%s/tiebreakers'%self.division.division_id)
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            
            tiebreakers_returned = json.loads(rv.data)['data']
            self.assertEquals(len(tiebreakers_returned['tiebreakers']),4)
            self.assertEquals(tiebreakers_returned['tiebreakers'][2][0]['initial_seed'],4)
            self.assertEquals(tiebreakers_returned['tiebreakers'][2][0]['final_player_id'],5)

    def test_division_final_get_tiebreakers_without_ties(self):        
        self.division.finals_num_qualifiers = 8
        self.flask_app.tables.db_handle.session.commit()
        self.populate_scores_for_finals_testing(with_ties=False)
        
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_admin','password':'test_admin'}))
            rv = c.post('/finals/division_final/division_id/%s'%self.division.division_id)
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            
            division_final_returned = json.loads(rv.data)['data']
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_scorekeeper','password':'test_scorekeeper'}))            
            rv = c.get('/finals/division_final/division_id/%s/tiebreakers'%self.division.division_id)
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            
            tiebreakers_returned = json.loads(rv.data)['data']
            self.assertEquals(len(tiebreakers_returned['tiebreakers']),0)

    def test_division_final_record_tiebreakers(self):        
        self.division.finals_num_qualifiers = 8
        self.flask_app.tables.db_handle.session.commit()
        self.populate_scores_for_finals_testing()
        
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_admin','password':'test_admin'}))
            rv = c.post('/finals/division_final/division_id/%s'%self.division.division_id)
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            
            division_final_returned = json.loads(rv.data)['data']
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_scorekeeper','password':'test_scorekeeper'}))            
            rv = c.get('/finals/division_final/division_id/%s/tiebreakers'%self.division.division_id)
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            
            tiebreakers_returned = json.loads(rv.data)['data']            
            tiebreakers_returned['tiebreakers'][0][0]['player_score']="1"
            tiebreakers_returned['tiebreakers'][0][1]['player_score']="2"
            rv = c.post('/finals/division_final/division_id/%s/tiebreakers' % division_final_returned['division_final_id'],
                       data=json.dumps(tiebreakers_returned['tiebreakers'][0]))
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            rv = c.get('/finals/division_final/division_id/%s/tiebreakers'%self.division.division_id)
            modified_tiebreakers_returned = json.loads(rv.data)['data']            
            self.assertEquals(len(modified_tiebreakers_returned['tiebreakers']),3)
            rv = c.get('/finals/division_final/division_id/%s/qualifiers'%division_final_returned['division_final_id'])
            qualifiers_returned = json.loads(rv.data)['data']                        
            self.assertEquals(qualifiers_returned[0]['initial_seed'],0)
            self.assertEquals(qualifiers_returned[1]['initial_seed'],1)
    
    def test_division_final_get_qualifiers(self):        
        self.division.finals_num_qualifiers = 8
        self.flask_app.tables.db_handle.session.commit()
        self.populate_scores_for_finals_testing()
        
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_admin','password':'test_admin'}))
            rv = c.post('/finals/division_final/division_id/%s'%self.division.division_id)
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            
            division_final_returned = json.loads(rv.data)['data']
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_scorekeeper','password':'test_scorekeeper'}))            
            rv = c.get('/finals/division_final/division_id/%s/qualifiers'%division_final_returned['division_final_id'])
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))            
            qualifiers_returned = json.loads(rv.data)['data']
            self.assertEquals(len(qualifiers_returned), 41)            

    def test_division_final_remove_qualifier_with_ties(self):        
        self.division.finals_num_qualifiers = 8
        self.flask_app.tables.db_handle.session.commit()
        self.populate_scores_for_finals_testing()
        
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_admin','password':'test_admin'}))
            rv = c.post('/finals/division_final/division_id/%s'%self.division.division_id)
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            
            division_final_returned = json.loads(rv.data)['data']
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_scorekeeper','password':'test_scorekeeper'}))            
            rv = c.get('/finals/division_final/division_id/%s/qualifiers'%division_final_returned['division_final_id'])
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))            
            qualifiers_returned = json.loads(rv.data)['data']                        
            self.assertEquals(qualifiers_returned[8]['type'],'divider')
            qualifiers_returned[0]['removed']=True            
            rv = c.put('/finals/division_final/division_id/%s/qualifiers'%division_final_returned['division_final_id'],
                       data=json.dumps(qualifiers_returned))
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))            
            qualifiers_returned = json.loads(rv.data)['data']            
            rv = c.get('/finals/division_final/division_id/%s/qualifiers'%division_final_returned['division_final_id'],
                       data=json.dumps(qualifiers_returned))
            qualifiers_returned = json.loads(rv.data)['data']
            self.assertEquals(qualifiers_returned[10]['type'],'divider')
            self.assertEquals(qualifiers_returned[9]['reranked_seed'],7)

    def test_division_final_generate_brackets(self):        
        self.division.finals_num_qualifiers = 24
        self.flask_app.tables.db_handle.session.commit()
        for i in range(120,140):
            self.players.append(orm_creation.create_player(self.flask_app,{'first_name':'test','last_name':'player%s'%i,'ifpa_ranking':'123','linked_division_id':'1'}))
        self.populate_scores_for_finals_testing(max_players=30,with_ties=False)
        
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_admin','password':'test_admin'}))
            rv = c.post('/finals/division_final/division_id/%s'%self.division.division_id)
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            
            division_final_returned = json.loads(rv.data)['data']
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_scorekeeper','password':'test_scorekeeper'}))            
            rv = c.get('/finals/division_final/division_id/%s/qualifiers'%division_final_returned['division_final_id'])
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))            
            qualifiers_returned = json.loads(rv.data)['data']                        
            rv = c.post('/finals/division_final/division_id/%s/rounds'%division_final_returned['division_final_id'],
                        data=json.dumps(qualifiers_returned))
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))            
            brackets_returned = json.loads(rv.data)['data']                                
        
        round = brackets_returned[0]
        self.assertEquals(round['round_number'],"1")        
        self.assertEquals(len(round['division_final_matches']),4)
        match = round['division_final_matches'][0]
        self.assertEquals(len(match['final_match_game_results']),3)
        self.assertEquals(len(match['final_match_player_results']),4)                
        final_match_game_result = match['final_match_game_results'][0]
        final_match_player_result = match['final_match_player_results'][0]                
        self.assertTrue(final_match_player_result['final_player_id'] in [9,16,17,24])
        self.assertEquals(len(final_match_game_result['division_final_match_game_player_results']),4)                
        final_match_game_player_result = final_match_game_result['division_final_match_game_player_results'][0]
        self.assertTrue(final_match_game_player_result['final_player_id'] in [9,16,17,24])         
        self.assertEquals(len(self.flask_app.tables.DivisionFinalMatchGameResult.query.all()),11*3)
        self.assertEquals(len(self.flask_app.tables.DivisionFinalMatchGamePlayerResult.query.all()),11*3*4)
        self.assertEquals(len(self.flask_app.tables.DivisionFinalMatch.query.all()),11)
        self.assertEquals(len(self.flask_app.tables.DivisionFinalRound.query.all()),4)        
        self.assertEquals(len(self.flask_app.tables.DivisionFinalMatchPlayerResult.query.all()),11*4)        
 
    def fill_in_final_bracket_scores(self,division_final_id,rounds_to_fill_in):
        division_final = self.flask_app.tables.DivisionFinal.query.filter_by(division_final_id=division_final_id).first()
        for division_final_round in division_final.division_final_rounds:
            if division_final_round.round_number not in rounds_to_fill_in:
                continue
            for match in division_final_round.division_final_matches:
                for game_result in match.final_match_game_results:
                    temp_score = 1
                    for game_player_result in game_result.division_final_match_game_player_results:                        
                        game_player_result.score=temp_score
                        temp_score=temp_score+1
        self.flask_app.tables.db_handle.session.commit()                                
    
    def test_division_final_round_reopen(self):        
        self.division.finals_num_qualifiers = 24
        self.flask_app.tables.db_handle.session.commit()
        for i in range(120,140):
            self.players.append(orm_creation.create_player(self.flask_app,{'first_name':'test','last_name':'player%s'%i,'ifpa_ranking':'123','linked_division_id':'1'}))
        self.populate_scores_for_finals_testing(max_players=30,with_ties=False)
        
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_admin','password':'test_admin'}))
            rv = c.post('/finals/division_final/division_id/%s'%self.division.division_id)
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            
            division_final_returned = json.loads(rv.data)['data']
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_scorekeeper','password':'test_scorekeeper'}))            
            rv = c.get('/finals/division_final/division_id/%s/qualifiers'%division_final_returned['division_final_id'])
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))            
            qualifiers_returned = json.loads(rv.data)['data']                        
            rv = c.post('/finals/division_final/division_id/%s/rounds'%division_final_returned['division_final_id'],
                        data=json.dumps(qualifiers_returned))
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))            
            brackets_returned = json.loads(rv.data)['data']
            round_one_division_final_round_id=brackets_returned[0]['division_final_round_id']
            round_two_division_final_round_id=brackets_returned[1]['division_final_round_id']
            self.fill_in_final_bracket_scores(division_final_returned['division_final_id'],['1'])
            
            rv = c.put('/finals/scorekeeping/division_final_round/%s/complete'%round_one_division_final_round_id)
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))            
            self.fill_in_final_bracket_scores(division_final_returned['division_final_id'],['2'])
            rv = c.put('/finals/scorekeeping/division_final_round/%s/reopen'%round_one_division_final_round_id)
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))            
            round_two_division_final_round = self.flask_app.tables.DivisionFinalRound.query.filter_by(division_final_round_id=round_two_division_final_round_id).first()
            round_one_division_final_round = self.flask_app.tables.DivisionFinalRound.query.filter_by(division_final_round_id=round_one_division_final_round_id).first()
            
            self.assertEquals(round_one_division_final_round.completed,False)
            for match in round_two_division_final_round.division_final_matches:
                for player_result in match.final_match_player_results:
                    self.assertEquals(player_result.needs_tiebreaker,False)
                    self.assertEquals(player_result.won_tiebreaker,None)
                    self.assertEquals(player_result.final_player_id,None)
                for game in match.final_match_game_results:                    
                    for score in game.division_final_match_game_player_results:
                        self.assertEquals(score.score,None)                        
                        self.assertEquals(score.final_player_id,None)                        

    def test_route_scorekeeping_get_division_final(self):        
        pass

    def test_route_get_division_final(self):        
        pass
    
    def test_route_scorekeeping_record_game(self):        
        pass

    def test_route_delete_division_final_rounds(self):
        pass

    def test_route_get_division_final_round_count(self):
        pass

    def test_route_get_division_final_round_count(self):
        pass

    def test_route_complete_division_final_round(self):
        pass
    
