import unittest
from mock import MagicMock
from pss_unit_test_base import PssUnitTestBase
from lib.flask_lib import app_build
from lib import CustomJsonEncoder
from flask import Flask
from flask_principal import Principal
from lib.PssConfig import PssConfig
from routes import auth
from lib import roles
import json
from werkzeug.exceptions import BadRequest,Unauthorized

# change name to auth
class RouteLoginTest(PssUnitTestBase):    

    def generate_fake_verify_password(self,password_to_compare):
        def fake_verify_password(password):            
            if password == password_to_compare:                
                return True            
            else:                
                return False
        return fake_verify_password
    
    def setUp(self):
        self.mock_user_with_admin_permissions = self.create_mock_user([roles.PSS_ADMIN],is_pss_admin_user=True)
        self.mock_user_with_user_permissions = self.create_mock_user([roles.PSS_USER],is_pss_admin_user=True)
        self.mock_user_with_incorrect_permissions = self.create_mock_user([roles.TEST],is_pss_admin_user=True)
        self.mock_user_with_td_permissions = self.create_mock_user([roles.TOURNAMENT_DIRECTOR],is_pss_admin_user=False)

        self.mock_request = MagicMock()        
        self.mock_tables = MagicMock()
        
    
    def test_check_pss_user_admin_site_access_throws_exception_with_incorrect_roles(self):        
        self.mock_tables.Roles.query.filter_by().all.return_value = [self.create_mock_role(roles.PSS_ADMIN)]
        with self.assertRaises(Exception) as cm:
            auth.check_pss_user_has_admin_site_access(self.mock_user_with_incorrect_permissions,self.mock_tables)            

    def test_check_pss_user_admin_site_access_with_correct_roles(self):
        self.mock_tables.Roles.query.filter_by().all.return_value = [self.create_mock_role(roles.PSS_ADMIN)]        
        self.assertTrue(auth.check_pss_user_has_admin_site_access(self.mock_user_with_admin_permissions,self.mock_tables))

    def test_check_event_user_has_event_access_throws_exception_with_incorrect_roles(self):        
        self.mock_tables.EventRoles.query.all.return_value = [self.create_mock_role(roles.TOURNAMENT_DIRECTOR)]
        with self.assertRaises(Exception) as cm:
            auth.check_event_user_has_event_access(self.mock_user_with_incorrect_permissions,self.mock_tables)            

    def test_check_event_user_has_event_access_with_correct_roles(self):
        self.mock_tables.EventRoles.query.all.return_value = [self.create_mock_role(roles.TOURNAMENT_DIRECTOR)]        
        self.assertTrue(auth.check_event_user_has_event_access(self.mock_user_with_td_permissions,self.mock_tables))


    #FIXME: need a test for the following : user is created for event, then tries to login to another event (including pss_admin)
    def test_pss_login_route(self):
        self.mock_tables.PssUsers.query.options().filter_by().first.return_value = self.mock_user_with_admin_permissions 
        self.mock_tables.Roles.query.filter_by().all.return_value = [self.create_mock_role(roles.PSS_ADMIN)]

        self.mock_request.data = json.dumps({'username':'test_user','password':'password'})
        pss_user_returned = auth.pss_login_route(self.mock_request,self.mock_tables,is_pss_admin_event=True)
        self.assertEquals(pss_user_returned,self.mock_user_with_admin_permissions)

    def test_pss_login_route_fails_when_bad_password_provided(self):
        self.mock_user_with_admin_permissions.verify_password = self.generate_fake_verify_password('password')
        self.mock_tables.PssUsers.query.options().filter_by().first.return_value = self.mock_user_with_admin_permissions 
        self.mock_request.data = json.dumps({'username':'test_user','password':'password2'})
        with self.assertRaises(Unauthorized) as cm:
            auth.pss_login_route(self.mock_request,self.mock_tables,is_pss_admin_event=True)        

    def test_pss_login_route_fails_when_bad_user_provided(self):        
        self.mock_tables.PssUsers.query.options().filter_by().first.return_value = None
        self.mock_request.data = json.dumps({'username':'test_user2','password':'password'})
        with self.assertRaises(Unauthorized) as cm:
            auth.pss_login_route(self.mock_request,self.mock_tables,is_pss_admin_event=True)        
            
    def test_pss_login_route_fails_with_incorrect_permissions_for_pss_admin_event(self):
        self.mock_tables.PssUsers.query.options().filter_by().first.return_value = self.mock_user_with_incorrect_permissions 
        self.mock_tables.Roles.query.filter_by().all.return_value = [self.create_mock_role(roles.PSS_ADMIN)]
        self.mock_request.data = json.dumps({'username':'test_user','password':'password'})
        with self.assertRaises(Unauthorized) as cm:
            auth.pss_login_route(self.mock_request,self.mock_tables,is_pss_admin_event=True)
            
    def test_pss_login_route_fails_with_incorrect_permissions_for_pss_event(self):
        self.mock_tables.PssUsers.query.options().filter_by().first.return_value = self.mock_user_with_incorrect_permissions 
        self.mock_tables.Roles.query.filter_by().all.return_value = [self.create_mock_role(roles.TOURNAMENT_DIRECTOR)]
        self.mock_request.data = json.dumps({'username':'test_user','password':'password'})
        with self.assertRaises(Unauthorized) as cm:
            auth.pss_login_route(self.mock_request,self.mock_tables,is_pss_admin_event=False)

            
