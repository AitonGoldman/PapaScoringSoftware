import unittest
from mock import MagicMock
from pss_unit_test_base import PssUnitTestBase
from lib.flask_lib import app_build
from lib import CustomJsonEncoder
from flask import Flask
from flask_principal import Principal
from lib.PssConfig import PssConfig
from routes import auth,player
from lib import roles_constants
import json
from werkzeug.exceptions import BadRequest,Unauthorized

class RoutePlayer(PssUnitTestBase):    
        
    def setUp(self):
        self.mock_user_with_admin_permissions = self.create_mock_user([roles_constants.PSS_ADMIN])
        self.mock_user_with_user_permissions = self.create_mock_user([roles_constants.PSS_USER])
        self.mock_user_with_incorrect_permissions = self.create_mock_user([roles_constants.PSS_PLAYER])        
        self.mock_new_user = self.create_mock_user([])
        self.mock_new_player = self.create_mock_player([])

        self.mock_request = MagicMock()        
        self.mock_tables = MagicMock()
        self.mock_app.tables = self.mock_tables
        
    def test_create_player_route(self):
        self.mock_request.data = json.dumps({'ifpa_ranking':99,
                                             'first_name':'test_player_first_name',
                                             'last_name':'test_player_last_name'})
        mock_role = self.create_mock_role(roles_constants.PSS_PLAYER)
        mock_role.role_id=1
        self.mock_tables.PlayerRoles.query.filter_by().first.return_value = mock_role
        
        self.mock_tables.Players.return_value = self.mock_new_player
        self.mock_tables.Players.query.filter_by().first.return_value = None
        
        created_player = player.create_player_route(self.mock_request,self.mock_app)
        self.assertEquals(self.mock_new_player,created_player)        
        
    def test_add_existing_player_to_event_route(self):
        mock_player_role = self.create_mock_role(roles_constants.PSS_PLAYER)
        mock_player_role.player_role_id=1
        mock_event = MagicMock()
        mock_event_player = MagicMock()
        self.mock_tables.Events.query.filter_by().first.return_value = mock_event
        self.mock_tables.EventPlayers.return_value = mock_event_player

        self.mock_tables.PlayerRoles.query.filter_by().first.return_value = mock_player_role
        mock_request_data={'ifpa_ranking':9999,
                           'first_name':'test_player_first_name',
                           'last_name':'test_player_last_name'}
        returned_event_player = player.add_existing_player_to_event_route(mock_request_data,
                                                                          self.mock_new_player,
                                                                          self.mock_app)
        self.mock_new_player.events.append.assert_called_once_with(mock_event)
        #self.mock_new_player.player_roles.append.assert_called_once_with(mock_player_role)
        self.assertEquals(1,len(self.mock_new_player.player_roles))
        self.assertEquals(mock_player_role.player_role_id,self.mock_new_player.player_roles[0].player_role_id)        
        self.assertEquals(returned_event_player,self.mock_new_player)
        self.assertEquals(self.mock_new_player.event_player,mock_event_player)
            
    def test_create_player_route_fails_with_bad_request_data(self):                
        self.mock_tables.Players.query.filter_by().first.return_value = None
        with self.assertRaises(Exception) as cm:        
            created_player = player.create_player_route(json.dumps({}),self.mock_app)
            
        request_data = {'ifpa_ranking':1,
                        'first_name':'test_first_name',
                        'last_name':'test_last_name'}
        request_data_copy = request_data.copy()
        request_data_copy.pop('ifpa_ranking')
        with self.assertRaises(Exception) as cm:        
            created_player = player.create_player_route(json.dumps(request_data_copy),self.mock_app)

        request_data_copy = request_data.copy()
        request_data_copy.pop('first_name')
        with self.assertRaises(Exception) as cm:        
            created_player = player.create_player_route(json.dumps(request_data_copy),self.mock_app)

        request_data_copy = request_data.copy()
        request_data_copy.pop('last_name')
        with self.assertRaises(Exception) as cm:        
            created_player = player.create_player_route(json.dumps(request_data_copy),self.mock_app)
            
    
    
