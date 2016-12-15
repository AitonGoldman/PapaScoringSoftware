import unittest
import os
from mock import MagicMock
import td_integration_test_base
import json
from routes import orm_creation
from util import db_util

class RouteResultsTD(td_integration_test_base.TdIntegrationDispatchTestBase):
    def setUp(self):
        super(RouteResultsTD,self).setUp()
        response,results = self.dispatch_request('/%s/util/healthcheck' % self.poop_db_name)                
        self.flask_app = self.app.instances[self.poop_db_name]
        self.admin_user, self.scorekeeper_user,self.desk_user = orm_creation.create_stanard_roles_and_users(self.flask_app)
        #FIXME : password/username should be passed in to create_roles_and_users()
        self.score_user_name_password='test_scorekeeper'
        self.admin_user_name_password='test_admin'        
        db_util.load_machines_from_json(self.flask_app,True)
        orm_creation.init_papa_tournaments_divisions(self.flask_app)        

        self.machine = self.flask_app.tables.Machine.query.filter_by(machine_id=1).first()
        #self.division = self.flask_app.tables.Division.query.filter_by(division_id=1).first()
        #self.team_division = self.flask_app.tables.Division.query.filter_by(team_tournament=True).first()        
        self.division_machines = []
        #self.team_division_machines = []
        self.players = []        
        self.flask_app.tables.db_handle.session.commit()
        for i in range(150):
            self.players.append(orm_creation.create_player(self.flask_app,{'first_name':'test','last_name':'player%s'%i,'ifpa_ranking':'123','linked_division_id':'1'}))
        for i in range(10):
            for division in self.flask_app.tables.Division.query.filter_by(team_tournament=False).all():
                self.division_machines.append(orm_creation.create_division_machine(self.flask_app,self.machine,division))
        self.division = self.flask_app.tables.Division.query.filter_by(team_tournament=False).all()[0]

        #for i in range(10):
        #    self.team_division_machines.append(orm_creation.create_division_machine(self.flask_app,self.machine,self.team_division))
        
        #self.new_team = orm_creation.create_team(self.flask_app,{
        #    'team_name':'test_team',
        #    'players':['1','2']
        #})
    def test_division_ties(self):                
        for division_machine in self.flask_app.tables.DivisionMachine.query.filter_by(division_id=self.division.division_id).all():            
            score=5
            while score <= 25:
                orm_creation.create_entry(self.flask_app,division_machine.division_machine_id,self.division.division_id,score,score-3)            
                orm_creation.create_entry(self.flask_app,division_machine.division_machine_id,self.division.division_id,score,score-4)
                score=score+5

        with self.flask_app.test_client() as c:
            rv = c.get('/results/division/%s'%self.division.division_id)
            results_returned = json.loads(rv.data)['data']
            for player in results_returned['ranked_player_list'][str(self.division.division_id)]:
                print "%s at rank %s with points %s" %(player[1]['player_id'],player[0],player[1]['sum'])
                if player[1]['player_id']==22 or player[1]['player_id']==21:
                    self.assertEquals(player[1]['sum'],300)
                    self.assertEquals(player[0],0)                    
                if player[1]['player_id']==16 or player[1]['player_id']==17:
                    self.assertEquals(player[1]['sum'],255)
                    self.assertEquals(player[0],2)
                if player[1]['player_id']==11 or player[1]['player_id']==12:
                    self.assertEquals(player[1]['sum'],249)
                    self.assertEquals(player[0],4)                    
                if player[1]['player_id']==6 or player[1]['player_id']==7:
                    self.assertEquals(player[1]['sum'],243)
                    self.assertEquals(player[0],6)                    
                if player[1]['player_id']==1 or player[1]['player_id']==2:
                    self.assertEquals(player[1]['sum'],237)
                    self.assertEquals(player[0],8)                    
                    
                    
    def test_machine_ties(self):
        score = 5
        division_machine = self.flask_app.tables.DivisionMachine.query.filter_by(division_id=self.division.division_id).first()
        while score <= 25:
            orm_creation.create_entry(self.flask_app,division_machine.division_machine_id,self.division.division_id,score,score-3)            
            orm_creation.create_entry(self.flask_app,division_machine.division_machine_id,self.division.division_id,score,score-4)
            score=score+5
        with self.flask_app.test_client() as c:
            rv = c.get('/results/division_machine/%s'%division_machine.division_machine_id)
            results_returned = json.loads(rv.data)['data']
            for result in results_returned:                
                if result['player_id']==22 or result['player_id']==21:
                    self.assertEquals(result['rank'],1)
                    self.assertEquals(result['points'],100)
                if result['player_id']==17 or result['player_id']==16:                    
                    self.assertEquals(result['rank'],3)
                    self.assertEquals(result['points'],85)                    
                if result['player_id']==12 or result['player_id']==11:
                    self.assertEquals(result['rank'],5)
                    self.assertEquals(result['points'],83)                    
                    
    @unittest.skip('hi there')
    def test_machine_results(self):
        with self.flask_app.test_client() as c:
            rv = c.get('/results/division_machine/%s'%self.division_machines[0].division_machine_id)
            results_returned = json.loads(rv.data)['data']
            self.assertEquals(len(results_returned),0)
        division_machine = self.flask_app.tables.DivisionMachine.query.filter_by(division_id=self.division.division_id).first()
        for player in self.players:
            orm_creation.create_entry(self.flask_app,division_machine.division_machine_id,self.division.division_id,player.player_id-5,player.player_id)
            orm_creation.create_entry(self.flask_app,division_machine.division_machine_id,self.division.division_id,player.player_id,player.player_id)
    
        players_in_returned_results = {}
        with self.flask_app.test_client() as c:
            rv = c.get('/results/division_machine/%s'%division_machine.division_machine_id)
            results_returned = json.loads(rv.data)['data']
            for result in results_returned:
                self.assertFalse(result['player_id'] in players_in_returned_results)
                players_in_returned_results[result['player_id']]=result
                self.assertEquals(result['score'],result['player_id'])                
                
                if result['player_id'] == 150:                    
                    self.assertEquals(result['points'],100)
                    self.assertEquals(result['rank'],1)                    
                if result['player_id'] == 149:
                    self.assertEquals(result['points'],90)
                    self.assertEquals(result['rank'],2)                    
                if result['player_id'] == 148:
                    self.assertEquals(result['points'],85)
                    self.assertEquals(result['rank'],3)                    
                if result['player_id'] < 148 and result['player_id'] > 63:                    
                    self.assertEquals(result['points'],result['player_id']-63)                    
                    self.assertEquals(result['rank'],150-result['player_id']+1)                    
                if result['player_id'] < 64:
                    self.assertEquals(result['points'],0)
                    self.assertEquals(result['rank'],150-result['player_id']+1)                                        
                    
                player_entries = self.flask_app.tables.Entry.query.filter_by(player_id=result['player_id']).all()
                self.assertEquals(len(player_entries),2)
            self.assertEquals(len(players_in_returned_results.keys()),150)

    @unittest.skip('hi there')    
    def test_division_results(self):
        with self.flask_app.test_client() as c:
            rv = c.get('/results/division/%s'%self.division.division_id)
            results_returned = json.loads(rv.data)['data']            
            for player_id in range(150):
                self.assertEquals(len(results_returned['top_machines'][str(self.division.division_id)][str(player_id+1)]),0)            
                
        for player in self.players:
            for division_machine in self.flask_app.tables.DivisionMachine.query.filter_by(division_id=self.division.division_id).all():
                orm_creation.create_entry(self.flask_app,division_machine.division_machine_id,self.division.division_id,player.player_id-5,player.player_id)
                orm_creation.create_entry(self.flask_app,division_machine.division_machine_id,self.division.division_id,player.player_id,player.player_id)
    
        players_in_returned_results = {}
        with self.flask_app.test_client() as c:
            rv = c.get('/results/division/%s'%self.division.division_id)
            results_returned = json.loads(rv.data)['data']
            for player in results_returned['ranked_player_list'][str(self.division.division_id)]:
                if player[1]['player_id']==150:
                    self.assertEquals(player[1]['sum'],300)
                    self.assertEquals(player[0],0)                    
                if player[1]['player_id']==149:
                    self.assertEquals(player[1]['sum'],300-30)
                    self.assertEquals(player[0],1)                                        
                if player[1]['player_id']==148:
                    self.assertEquals(player[1]['sum'],300-45)
                    self.assertEquals(player[0],2)                                        
                if player[1]['player_id'] < 148 and player[1]['player_id'] > 63:                                        
                    player_points = player[1]['player_id']-63
                    sum_points = player_points*3
                    self.assertEquals(player[1]['sum'],sum_points)
                    self.assertEquals(player[0],150-player[1]['player_id'])                                        
                if player[1]['player_id'] < 64:                                                            
                    self.assertEquals(player[1]['sum'],0)
                    self.assertEquals(player[0],87)                                                            
            for player_id in range(2,151):                
                player_rank_machine_0 = results_returned['top_machines'][str(self.division.division_id)][str(player_id)][0]['rank']
                player_rank_machine_1 = results_returned['top_machines'][str(self.division.division_id)][str(player_id)][1]['rank']
                player_rank_machine_2 = results_returned['top_machines'][str(self.division.division_id)][str(player_id)][2]['rank']                
                if player_id == 150:                    
                    self.assertEquals(player_rank_machine_0,1)
                    self.assertEquals(player_rank_machine_1,1)
                    self.assertEquals(player_rank_machine_2,1)
                    
                if player_id == 149:
                   self.assertEquals(player_rank_machine_0,2)
                   self.assertEquals(player_rank_machine_1,2)                                          
                   self.assertEquals(player_rank_machine_2,2)                                          
                   
                if player_id == 148:
                   self.assertEquals(player_rank_machine_0,3)
                   self.assertEquals(player_rank_machine_1,3)
                   self.assertEquals(player_rank_machine_2,3)
                   
                if player_id < 148 and player_id > 63:                    
                   self.assertEquals(player_rank_machine_0,150-player_id+1)
                   self.assertEquals(player_rank_machine_1,150-player_id+1) 
                   self.assertEquals(player_rank_machine_2,150-player_id+1) 
                   
                if player_id < 64:                    
                   self.assertEquals(player_rank_machine_0,150-player_id+1) 
                   self.assertEquals(player_rank_machine_1,150-player_id+1) 
                   self.assertEquals(player_rank_machine_2,150-player_id+1) 
    @unittest.skip('hi there')
    def test_player_results(self):
        with self.flask_app.test_client() as c:
            for player_id in range(150):
                rv = c.get('/results/player/1')
                results_returned = json.loads(rv.data)['data']
                for div_id in results_returned:
                    self.assertEquals(len(results_returned[div_id]['entries']),0)                
        for player in self.players[0:25]:                    
            for division in self.flask_app.tables.Division.query.filter_by(team_tournament=False).all():
                for division_machine in self.flask_app.tables.DivisionMachine.query.filter_by(division_id=division.division_id):
                    orm_creation.create_entry(self.flask_app,division_machine.division_machine_id,division.division_id,player.player_id-5,player.player_id)
                    orm_creation.create_entry(self.flask_app,division_machine.division_machine_id,division.division_id,player.player_id,player.player_id)

        with self.flask_app.test_client() as c:
            for player_id in range(1,26):                
                rv = c.get('/results/player/%s'%player_id)
                results_returned = json.loads(rv.data)['data']                
                for division in self.flask_app.tables.Division.query.filter_by(team_tournament=False).all():                    
                    self.assertEquals(results_returned[str(division.division_id)]['rank'],25-player_id)                    
                    for machine_results in results_returned[str(division.division_id)]['entries']:
                        if player_id==25:
                            self.assertEquals(machine_results['points'],100)
                            self.assertEquals(machine_results['rank'],1)                            
                        if player_id==24:
                            self.assertEquals(machine_results['points'],90)
                            self.assertEquals(machine_results['rank'],2)                                                        
                        if player_id==23:
                            self.assertEquals(machine_results['points'],85)
                            self.assertEquals(machine_results['rank'],3)                                                        
                        if player_id<=22:
                            self.assertEquals(machine_results['points'],87-(25-player_id))
                            self.assertEquals(machine_results['rank'],25-player_id+1)                            
                        
                   
                
            
