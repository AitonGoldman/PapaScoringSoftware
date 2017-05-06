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
        for i in range(20):
            self.players.append(orm_creation.create_player(self.flask_app,{'first_name':'test','last_name':'player%s'%i,'ifpa_ranking':'123','linked_division_id':'1'}))
        for i in range(10):
            for division in self.flask_app.tables.Division.query.filter_by(team_tournament=False).all():
                self.division_machines.append(orm_creation.create_division_machine(self.flask_app,self.machine,division))
            for division in self.flask_app.tables.Division.query.filter_by(team_tournament=True).all():
                self.team_division_machines.append(orm_creation.create_division_machine(self.flask_app,self.machine,division))
                
        self.division = self.flask_app.tables.Division.query.filter_by(team_tournament=False).all()[0]
        self.team_division = self.flask_app.tables.Division.query.filter_by(team_tournament=True).all()[0]
        
        for i in range(1,10,2):            
            self.teams.append(orm_creation.create_team(self.flask_app,{
                'team_name':'test_team_%s'%i,
                'players':['%s'%i,'%s'%(i+1)]
            }))
    def populate_scores_for_finals_testing(self,with_ties=True):
        for division_machine in self.flask_app.tables.DivisionMachine.query.filter_by(division_id=self.division.division_id).all():            
            score=3
            if with_ties:
                increment=2
            else:
                increment=1
            while score <= 20:
                orm_creation.create_entry(self.flask_app,division_machine.division_machine_id,self.division.division_id,score,score-2)            
                if with_ties:
                    orm_creation.create_entry(self.flask_app,division_machine.division_machine_id,self.division.division_id,score,score-1)
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
            self.assertEquals(tiebreakers_returned['tiebreakers'][2][0]['initial_seed'],6)
            self.assertEquals(tiebreakers_returned['tiebreakers'][2][0]['final_player_id'],7)

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
                        
            
    # def test_division_results(self):
    #     with self.flask_app.test_client() as c:
    #         rv = c.get('/results/division/%s'%self.division.division_id)
    #         results_returned = json.loads(rv.data)['data']            
    #         for player_id in range(150):
    #             self.assertEquals(len(results_returned['top_machines'][str(self.division.division_id)][str(player_id+1)]),0)            
                
    #     for player in self.players:
    #         for division_machine in self.flask_app.tables.DivisionMachine.query.filter_by(division_id=self.division.division_id).all():
    #             orm_creation.create_entry(self.flask_app,division_machine.division_machine_id,self.division.division_id,player.player_id-5,player.player_id)
    #             orm_creation.create_entry(self.flask_app,division_machine.division_machine_id,self.division.division_id,player.player_id,player.player_id)
    
    #     players_in_returned_results = {}
    #     with self.flask_app.test_client() as c:
    #         rv = c.get('/results/division/%s'%self.division.division_id)
    #         results_returned = json.loads(rv.data)['data']            
    #         for player in results_returned['ranked_player_list'][str(self.division.division_id)]:
    #             if player[1]['player_id']==150:
    #                 self.assertEquals(player[1]['sum'],600)
    #                 self.assertEquals(player[0],0)                    
    #             if player[1]['player_id']==149:
    #                 self.assertEquals(player[1]['sum'],600-60)
    #                 self.assertEquals(player[0],1)                                        
    #             if player[1]['player_id']==148:
    #                 self.assertEquals(player[1]['sum'],600-90)
    #                 self.assertEquals(player[0],2)                                        
    #             if player[1]['player_id'] < 148 and player[1]['player_id'] > 63:                                        
    #                 player_points = player[1]['player_id']-63
    #                 sum_points = player_points*6
    #                 self.assertEquals(player[1]['sum'],sum_points)
    #                 self.assertEquals(player[0],150-player[1]['player_id'])                                        
    #             if player[1]['player_id'] < 64:                                                            
    #                 self.assertEquals(player[1]['sum'],0)
    #                 self.assertEquals(player[0],87,"Expected rank to be 87 but instead got %s"%player[0])                                                            
    #         for player_id in range(2,151):                
    #             player_rank_machine = [None]*6
    #             for machine_index in range(6):                    
    #                 player_rank_machine[machine_index]= results_returned['top_machines'][str(self.division.division_id)][str(player_id)][machine_index]['rank']

    #             if player_id == 150:                    
    #                 for machine_index in range(6):
    #                     self.assertEquals(player_rank_machine[machine_index],1)                        
                    
    #             if player_id == 149:
    #                 for machine_index in range(6):
    #                     self.assertEquals(player_rank_machine[machine_index],2)                        

    #             if player_id == 148:
    #                 for machine_index in range(6):
    #                     self.assertEquals(player_rank_machine[machine_index],3)                        
                   
    #             if player_id < 148 and player_id > 63:                    
    #                 for machine_index in range(6):
    #                     self.assertEquals(player_rank_machine[machine_index],150-player_id+1)                        
                   
    #             if player_id < 64:
    #                 for machine_index in range(6):
    #                     self.assertEquals(player_rank_machine[machine_index],150-player_id+1)                        
                    

    # def test_team_division_results(self):
    #     with self.flask_app.test_client() as c:
    #         rv = c.get('/results/division/%s'%self.team_division.division_id)
    #         results_returned = json.loads(rv.data)['data']            
    #         for team_id in range(1,70):
    #             self.assertEquals(len(results_returned['top_machines'][str(self.team_division.division_id)][str(team_id)]),0)            
                
    #     for team in self.teams:
    #         for division_machine in self.flask_app.tables.DivisionMachine.query.filter_by(division_id=self.team_division.division_id).all():
    #             orm_creation.create_entry(self.flask_app,division_machine.division_machine_id,self.team_division.division_id,team.team_id-5,team_id=team.team_id)
    #             orm_creation.create_entry(self.flask_app,division_machine.division_machine_id,self.team_division.division_id,team.team_id,team_id=team.team_id)
    
    #     teams_in_returned_results = {}
    #     with self.flask_app.test_client() as c:
    #         rv = c.get('/results/division/%s'%self.team_division.division_id)
    #         results_returned = json.loads(rv.data)['data']            
    #         for team in results_returned['ranked_team_list'][str(self.team_division.division_id)]:
    #             if team[1]['team_id']==70:
    #                 self.assertEquals(team[1]['sum'],600)
    #                 self.assertEquals(team[0],0)                    
    #             if team[1]['team_id']==69:
    #                 self.assertEquals(team[1]['sum'],600-60)
    #                 self.assertEquals(team[0],1)                                        
    #             if team[1]['team_id']==68:
    #                 self.assertEquals(team[1]['sum'],600-90)
    #                 self.assertEquals(team[0],2)                                        
    #             if team[1]['team_id'] < 68:
    #                 team_points = team[1]['team_id']+17
    #                 sum_points = team_points*6                    
    #                 self.assertEquals(team[1]['sum'],
    #                                   sum_points,
    #                                   "was expecting team_id %s to have points of %s, but instead found %s" % (team[1]['team_id'],sum_points,team[1]['sum']))
    #                 self.assertEquals(team[0],70-team[1]['team_id'])                                        
    #         for team_id in range(1,71):                
    #             team_rank_machine = [None]*6
    #             for machine_index in range(6):                    
    #                 team_rank_machine[machine_index]= results_returned['top_machines'][str(self.team_division.division_id)][str(team_id)][machine_index]['rank']
    #             if team_id == 70:
    #                 for machine_index in range(6):
    #                     self.assertEquals(team_rank_machine[machine_index],1)                        
                    
    #             if team_id == 69:
    #                 for machine_index in range(6):
    #                     self.assertEquals(team_rank_machine[machine_index],2)                        
                                       
    #             if team_id == 68:
    #                 for machine_index in range(6):
    #                     self.assertEquals(team_rank_machine[machine_index],3)                        
                    
    #             if team_id < 67:
    #                 for machine_index in range(6):
    #                     self.assertEquals(team_rank_machine[machine_index],70-team_id+1)                                           
                   
            
