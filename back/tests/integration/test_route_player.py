import unittest
import os
from mock import MagicMock
import td_integration_test_base
import json
from routes import orm_creation

class RoutePlayerTD(td_integration_test_base.TdIntegrationDispatchTestBase):
    def setUp(self):
        super(RoutePlayerTD,self).setUp()
        response,results = self.dispatch_request('/%s/util/healthcheck' % self.poop_db_name)                
        self.flask_app = self.app.instances[self.poop_db_name]
        
        orm_creation.create_roles(self.flask_app)
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
        orm_creation.create_user(self.flask_app,'test_admin','test_admin',[orm_creation.RolesEnum.admin.value,
                                                                           orm_creation.RolesEnum.desk.value])
        # self.player_role = self.flask_app.tables.Role(name='player')
        # self.flask_app.tables.db_handle.session.add(self.player_role)
        # self.flask_app.tables.db_handle.session.commit()

        # self.score_role = self.flask_app.tables.Role(name='scorekeeper')
        # self.flask_app.tables.db_handle.session.add(self.score_role)
        # self.flask_app.tables.db_handle.session.commit()        
        # self.score_user = self.flask_app.tables.User(username='test_score')
        # self.score_user.crypt_password('test_score')
        # self.score_user.roles.append(self.score_role)
        # self.flask_app.tables.db_handle.session.add(self.score_user)
        # self.flask_app.tables.db_handle.session.commit()


        # self.admin_role = self.flask_app.tables.Role(name='admin')
        # self.flask_app.tables.db_handle.session.add(self.admin_role)
        # self.flask_app.tables.db_handle.session.commit()

        # self.admin_role_id = self.admin_role.role_id
        
        # self.admin_user = self.flask_app.tables.User(username='test_admin')
        # self.admin_user.crypt_password('test_admin_password')
        # self.admin_user.roles.append(self.admin_role)
        # self.flask_app.tables.db_handle.session.add(self.admin_user)
        # self.flask_app.tables.db_handle.session.commit()

        # self.desk_role = self.flask_app.tables.Role(name='desk')
        # self.flask_app.tables.db_handle.session.add(self.desk_role)
        # self.flask_app.tables.db_handle.session.commit()        
        # self.desk_user = self.flask_app.tables.User(username='test_desk')
        # self.desk_user.crypt_password('test_desk')
        # self.desk_user.roles.append(self.desk_role)
        # self.flask_app.tables.db_handle.session.add(self.desk_user)
        # self.flask_app.tables.db_handle.session.commit()

        # self.tournament_one = self.flask_app.tables.Tournament(            
        #     tournament_name='test_tournament_one',
        #     single_division=False
        # )
        # self.division_one = self.flask_app.tables.Division(
        #     division_name='one',            
        #     tournament_id=1            
        # )
        # self.division_two = self.flask_app.tables.Division(
        #     division_name='two',            
        #     tournament_id=1                        
        # )
        
        # self.flask_app.tables.db_handle.session.add(self.tournament_one)
        # self.flask_app.tables.db_handle.session.add(self.division_one)
        # self.flask_app.tables.db_handle.session.add(self.division_two)
        # self.flask_app.tables.db_handle.session.commit()

    # def test_get_players(self):
    #     with self.flask_app.test_client() as c:
    #         rv = c.put('/auth/login',
    #                    data=json.dumps({'username':'test_desk','password':'test_desk'}))
    #         rv = c.post('/player',
    #                     data=json.dumps({'first_name':'test',
    #                                      'last_name':'player',
    #                                      'ifpa_ranking':1234,
    #                                      'email_address':'test@test.com',
    #                                      'linked_division_id':1
    #                     }))
    #     with self.flask_app.test_client() as c:
    #         rv = c.get('/player')
    #         self.assertEquals(rv.status_code,
    #                           200,
    #                           'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
    #         returned_players = json.loads(rv.data)['data']            
    #         returned_player = returned_players['1']
    #         self.assertEquals(returned_player['first_name'],'test')
    #         self.assertEquals(returned_player['last_name'],'player')
    #         self.assertEquals(returned_player['ifpa_ranking'],1234)
    #         self.assertEquals(returned_player['email_address'],'test@test.com')
    #         self.assertEquals(returned_player['linked_division_id'],1)


    # def test_get_player_on_machine(self):
    #     with self.flask_app.test_client() as c:
    #         rv = c.put('/auth/login',
    #                    data=json.dumps({'username':'test_admin','password':'test_admin_password'}))
    #         rv = c.post('/division/1/division_machine',
    #                     data=json.dumps({'machine_id':1}))
    #     with self.flask_app.test_client() as c:
    #         rv = c.put('/auth/login',
    #                    data=json.dumps({'username':'test_desk','password':'test_desk'}))
    #         rv = c.post('/player',
    #                     data=json.dumps({'first_name':'test',
    #                                      'last_name':'player',
    #                                      'ifpa_ranking':1234,
    #                                      'email_address':'test@test.com',
    #                                      'linked_division_id':1
    #                     }))
    #         self.assertEquals(rv.status_code,
    #                           200,
    #                           'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            
    #     with self.flask_app.test_client() as c:
    #         rv = c.put('/auth/login',
    #                    data=json.dumps({'username':'test_score','password':'test_score'}))                    
    #         rv = c.put('/division/1/division_machine/1/player/1')
    #     with self.flask_app.test_client() as c:
    #         rv = c.get('/player/1')
    #         self.assertEquals(rv.status_code,
    #                           200,
    #                           'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
    #         returned_player = json.loads(rv.data)['data']                                    
    #         self.assertEquals(returned_player['division_machine']['division_machine_name'],'test_machine')

            
    def test_add_player(self):
        with self.flask_app.test_client() as c:
            rv = c.put('/auth/login',
                       data=json.dumps({'username':'test_admin','password':'test_admin'}))
            rv = c.post('/player',
                        data=json.dumps({'first_name':'test',
                                         'last_name':'player',
                                         'ifpa_ranking':1234,
                                         'email_address':'test@test.com',
                                         'linked_division_id':1
                        }))
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            returned_player = json.loads(rv.data)['data']
            self.assertEquals(returned_player['player_id'],1)
            player = self.flask_app.tables.Player.query.filter_by(player_id=returned_player['player_id']).first()
            self.assertEquals(player.player_id,returned_player['player_id'])

    # def test_edit_player(self):
    #     with self.flask_app.test_client() as c:
    #         rv = c.put('/auth/login',
    #                    data=json.dumps({'username':'test_desk','password':'test_desk'}))
    #         rv = c.post('/player',
    #                     data=json.dumps({'first_name':'test',
    #                                      'last_name':'player',
    #                                      'ifpa_ranking':1234,
    #                                      'email_address':'test@test.com',
    #                                      'linked_division_id':1
    #                     }))
    #         rv = c.put('/player/1',
    #                     data=json.dumps({'first_name':'test_changed',
    #                                      'last_name':'player_changed',
    #                                      'ifpa_ranking':4321,
    #                                      'email_address':'testchanged@test_changed.com',
    #                                      'linked_division_id':2
    #                     }))
            
    #         self.assertEquals(rv.status_code,
    #                           200,
    #                           'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
    #         returned_player = json.loads(rv.data)['data']
    #         self.assertEquals(1,returned_player['player_id'])
    #         player = self.flask_app.tables.Player.query.filter_by(player_id=returned_player['player_id']).first()
    #         self.assertEquals(player.first_name,'test_changed')
    #         self.assertEquals(player.last_name,'player_changed')
    #         self.assertEquals(player.ifpa_ranking,4321)
    #         self.assertEquals(player.email_address,'testchanged@test_changed.com')
    #         self.assertEquals(player.linked_division_id,2)
            
            
            
