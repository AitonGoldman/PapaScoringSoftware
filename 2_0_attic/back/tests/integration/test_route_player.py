import unittest
import os
from mock import MagicMock
import td_integration_test_base
import json
from routes import orm_creation
from util import db_util
class RoutePlayerTD(td_integration_test_base.TdIntegrationDispatchTestBase):
    def add_user_through_route(self,c):
        return c.post('/player',
                    data=json.dumps({'first_name':'test',
                                     'last_name':'player',
                                     'ifpa_ranking':1234,
                                     'email_address':'test@test.com',
                                     'linked_division_id':1
                    }))
    
    def setUp(self):
        super(RoutePlayerTD,self).setUp()
        response,results = self.dispatch_request('/%s/util/healthcheck' % self.poop_db_name)                
        self.flask_app = self.app.instances[self.poop_db_name]
        orm_creation.create_stanard_roles_and_users(self.flask_app)
        self.new_tournament = orm_creation.create_tournament(self.flask_app,{
            'tournament_name':'test_tournament',
            'single_division':False
        })
        self.create_division = orm_creation.create_division(self.flask_app,{
            'division_name':'all 1',
            'finals_num_qualifiers':24,
            'tournament_id':self.new_tournament.tournament_id,
            'scoring_type':'HERB',
            'use_stripe':False
        })

        new_tournament_data = {            
            'tournament_name':'test_tournament',
            'finals_num_qualifiers':'24',            
            'team_tournament':False,
            'single_division':True,
            'scoring_type':'HERB',
            'active':True,
            'use_stripe':False
        }
        self.new_tournament = orm_creation.create_tournament(self.flask_app,new_tournament_data)
        self.machine = self.flask_app.tables.Machine(machine_name='test_machine')
        self.flask_app.tables.db_handle.session.add(self.machine)
        self.flask_app.tables.db_handle.session.commit()        
        self.division_machine = orm_creation.create_division_machine(self.flask_app,self.machine,self.new_tournament.divisions[0])
        
    def test_get_players(self):
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_desk','password':'test_desk'}))
            rv = self.add_user_through_route(c)            
        with self.flask_app.test_client() as c:
            rv = c.get('/player')
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            returned_players = json.loads(rv.data)['data']
            returned_player = returned_players['1']
            self.assertEquals(returned_player['first_name'],'test')
            self.assertEquals(returned_player['last_name'],'player')
            self.assertEquals(returned_player['ifpa_ranking'],1234)
            self.assertEquals(returned_player['email_address'],'test@test.com')
            self.assertEquals(returned_player['linked_division_id'],1)
            self.assertEquals(returned_player['pin'],None)

    def test_get_player_on_machine(self):
        self.new_player = orm_creation.create_player(self.flask_app,{'first_name':'aiton','last_name':'goldman','ifpa_ranking':'123'})        
        self.division_machine.player_id=1
        self.flask_app.tables.db_handle.session.commit()
        with self.flask_app.test_client() as c:
            rv = c.get('/player/1')
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            returned_player = json.loads(rv.data)['data']                                    
            self.assertEquals(returned_player['division_machine']['division_machine_name'],'test_machine')

    def test_get_player_on_team(self):
        self.new_player = orm_creation.create_player(self.flask_app,{'first_name':'aiton','last_name':'goldman','ifpa_ranking':'123'})        
        self.new_team = orm_creation.create_team(self.flask_app,{
            'team_name':'test_team',
            'players':['1']
        })
        
        with self.flask_app.test_client() as c:
            rv = c.get('/player/1')
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            returned_player = json.loads(rv.data)['data']                                    
            
            self.assertEquals(returned_player['teams'][0]['team_name'],'test_team')
            
    def test_add_with_wrong_permissions(self):
        with self.flask_app.test_client() as c:
            self.checkWrongPermissions(c,'post','/player','test_scorekeeper')            

    def test_add_with_player_permissions(self):
        self.new_player = orm_creation.create_player(self.flask_app,{'first_name':'aiton','last_name':'goldman','ifpa_ranking':'123'})        
        with self.flask_app.test_client() as c:
            self.checkWrongPermissions(c,'post','/player',pin=self.new_player.pin)            

    def test_add_with_no_permissions(self):        
        with self.flask_app.test_client() as c:
            self.checkWrongPermissions(c,'post','/player')            
            
    def test_add_player(self):
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_desk','password':'test_desk'}))
            rv = self.add_user_through_route(c)
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            returned_player = json.loads(rv.data)['data']
            self.assertEquals(returned_player['player_id'],1)
            player = self.flask_app.tables.Player.query.filter_by(player_id=returned_player['player_id']).first()
            self.assertEquals(player.player_id,returned_player['player_id'])

    def test_edit_with_wrong_permissions(self):
        with self.flask_app.test_client() as c:
            self.checkWrongPermissions(c,'put','/player/1','test_scorekeeper')            

    def test_edit_with_player_permissions(self):
        self.new_player = orm_creation.create_player(self.flask_app,{'first_name':'aiton','last_name':'goldman','ifpa_ranking':'123'})        
        with self.flask_app.test_client() as c:
            self.checkWrongPermissions(c,'put','/player/1',pin=self.new_player.pin)            

    def test_edit_with_no_permissions(self):        
        with self.flask_app.test_client() as c:
            self.checkWrongPermissions(c,'put','/player/1')            
            
    def test_edit_player(self):
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_desk','password':'test_desk'}))
            rv = self.add_user_through_route(c)
            rv = c.put('/player/1',
                        data=json.dumps({'first_name':'test_changed',
                                         'last_name':'player_changed',
                                         'ifpa_ranking':4321,
                                         'email_address':'testchanged@test_changed.com',
                                         'linked_division_id':2
                        }))
            
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            returned_player = json.loads(rv.data)['data']
            self.assertEquals(1,returned_player['player_id'])
            player = self.flask_app.tables.Player.query.filter_by(player_id=returned_player['player_id']).first()
            self.assertEquals(player.first_name,'test_changed')
            self.assertEquals(player.last_name,'player_changed')
            self.assertEquals(player.ifpa_ranking,4321)
            self.assertEquals(player.email_address,'testchanged@test_changed.com')
            self.assertEquals(player.linked_division_id,2)
            
            
            
