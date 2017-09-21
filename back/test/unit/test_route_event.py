import unittest
from mock import MagicMock
from pss_unit_test_base import PssUnitTestBase
from lib.flask_lib import app_build
from lib import CustomJsonEncoder
from flask import Flask
from flask_principal import Principal
from lib.PssConfig import PssConfig
from routes import event
from lib import roles_constants,orm_factories
import json
from werkzeug.exceptions import BadRequest,Unauthorized

class RouteEventTest(PssUnitTestBase):
    def setUp(self):
        self.mock_user_with_admin_permissions = self.create_mock_user([roles_constants.PSS_ADMIN],is_pss_admin_user=True)
        self.mock_user_with_user_permissions = self.create_mock_user([roles_constants.PSS_USER],is_pss_admin_user=True)
        self.mock_user_with_incorrect_permissions = self.create_mock_user([roles_constants.TEST],is_pss_admin_user=True)
        self.mock_user_with_td_permissions = self.create_mock_user([roles_constants.TOURNAMENT_DIRECTOR],is_pss_admin_user=False)

        self.mock_request = MagicMock()        
        self.mock_tables = MagicMock()
        self.mock_event = MagicMock()
        self.mock_pss_config = MagicMock()
        self.mock_new_app = MagicMock()
        self.mock_new_app.name='poop'
        
    # er - this should be testing the route, not the orm factories 
    def test_create_event_route(self):
        mock_input_data={'name':'poop'}
        self.mock_event.name='poop'
        self.mock_tables.Events.query.filter_by().first.return_value=None
        self.mock_tables.Events.return_value=self.mock_event                        
        self.mock_tables.EventRoles.query.filter_by().first.return_value=self.create_mock_role(roles_constants.TOURNAMENT_DIRECTOR)
        new_event_tables = MagicMock()
        returned_event = orm_factories.create_event(self.mock_user_with_user_permissions,self.mock_tables,mock_input_data,new_event_tables)
        self.assertEquals(self.mock_event,returned_event)
        
    def test_create_event_route_fails_with_duplicate_event(self):
        mock_input_data={'name':'poop'}
        pss_config_mock = MagicMock()
        existing_event_mock = MagicMock()
        existing_event_mock.Events.query.filter_by().first.return_value = MagicMock()
        pss_config_mock.get_db_info().getImportedTables.return_value=existing_event_mock        
        with self.assertRaises(Exception) as cm:
            orm_factories.create_event_tables(pss_config_mock,self.mock_new_app)
        
    def test_get_events_in_event(self):
        pass

    def test_wizard_mode_cookie(self):
        pass
    
