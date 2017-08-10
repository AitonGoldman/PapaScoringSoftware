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

    def create_mock_role(self,role_name):
        mock_role = MagicMock()
        mock_role.name = role_name
        return mock_role
    
    def create_mock_user(self,role_names):
        mock_user = MagicMock()        
        mock_user.roles=[]
        for role_name in role_names:
            mock_role = self.create_mock_role(role_name)            
            mock_user.roles.append(mock_role)
        mock_user.verify_password.return_value=True            
        return mock_user

    def generate_fake_verify_password(self,password_to_compare):
        def fake_verify_password(password):            
            if password == password_to_compare:                
                return True            
            else:                
                return False
        return fake_verify_password
    
    def setUp(self):
        self.mock_user_with_admin_permissions = self.create_mock_user([roles.PSS_ADMIN])
        self.mock_user_with_user_permissions = self.create_mock_user([roles.PSS_USER])
        self.mock_user_with_incorrect_permissions = self.create_mock_user([roles.PSS_PLAYER])
        self.mock_request = MagicMock()        
        self.mock_tables = MagicMock()
        
    
    def test_check_pss_user_admin_site_access_throws_exception_with_incorrect_roles(self):        
        self.mock_tables.Roles.query.filter_by().all.return_value = [self.create_mock_role(roles.PSS_ADMIN)]
        with self.assertRaises(Exception) as cm:
            auth.check_pss_user_has_admin_site_access(self.mock_user_with_incorrect_permissions,self.mock_tables)            

    def test_check_pss_user_admin_site_access_with_correct_roles(self):
        self.mock_tables.Roles.query.filter_by().all.return_value = [self.create_mock_role(roles.PSS_ADMIN)]        
        self.assertTrue(auth.check_pss_user_has_admin_site_access(self.mock_user_with_admin_permissions,self.mock_tables))
        
    def test_pss_admin_login_route(self):
        self.mock_tables.PssUsers.query.options().filter_by().first.return_value = self.mock_user_with_admin_permissions 
        self.mock_tables.Roles.query.filter_by().all.return_value = [self.create_mock_role(roles.PSS_ADMIN)]

        self.mock_request.data = json.dumps({'username':'test_user','password':'password'})
        pss_user_returned = auth.pss_admin_login_route(self.mock_request,self.mock_tables)
        self.assertEquals(pss_user_returned,self.mock_user_with_admin_permissions)

    def test_pss_admin_login_route_fails_when_bad_password_provided(self):
        self.mock_user_with_admin_permissions.verify_password = self.generate_fake_verify_password('password')
        self.mock_tables.PssUsers.query.options().filter_by().first.return_value = self.mock_user_with_admin_permissions 
        self.mock_request.data = json.dumps({'username':'test_user','password':'password2'})
        with self.assertRaises(Unauthorized) as cm:
            auth.pss_admin_login_route(self.mock_request,self.mock_tables)        

    def test_pss_admin_login_route_fails_when_bad_user_provided(self):        
        self.mock_tables.PssUsers.query.options().filter_by().first.return_value = None
        self.mock_request.data = json.dumps({'username':'test_user2','password':'password'})
        with self.assertRaises(Unauthorized) as cm:
            auth.pss_admin_login_route(self.mock_request,self.mock_tables)        
            
    def test_pss_admin_login_route_fails_with_incorrect_permissions(self):
        self.mock_tables.PssUsers.query.options().filter_by().first.return_value = self.mock_user_with_incorrect_permissions 
        self.mock_request.data = json.dumps({'username':'test_user','password':'password'})
        with self.assertRaises(Unauthorized) as cm:
            auth.pss_admin_login_route(self.mock_request,self.mock_tables)
