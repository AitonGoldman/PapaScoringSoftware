import unittest
from mock import MagicMock
from pss_unit_test_base import PssUnitTestBase
from lib.flask_lib import app_build
from lib import CustomJsonEncoder
from flask import Flask
from flask_principal import Principal
from lib.PssConfig import PssConfig
from routes import auth,pss_user
from lib import roles_constants
import json
from werkzeug.exceptions import BadRequest,Unauthorized

# change name to auth
class RoutePssUser(PssUnitTestBase):    

    
    def create_mock_role(self,role_name):
        mock_role = MagicMock()
        mock_role.name = role_name
        return mock_role
    
    def create_mock_user(self,role_names):
        mock_user = MagicMock()        
        mock_user.admin_roles=[]
        for role_name in role_names:
            mock_role = self.create_mock_role(role_name)            
            mock_user.admin_roles.append(mock_role)
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
        self.mock_user_with_admin_permissions = self.create_mock_user([roles_constants.PSS_ADMIN])
        self.mock_user_with_user_permissions = self.create_mock_user([roles_constants.PSS_USER])
        self.mock_user_with_incorrect_permissions = self.create_mock_user([roles_constants.PSS_PLAYER])
        self.mock_new_user = self.create_mock_user([])

        self.mock_request = MagicMock()        
        self.mock_tables = MagicMock()
            
    def test_create_pss_user_route(self):
        self.mock_request.data = json.dumps({'username':'new_user_for_test_create_pss_user_route','password':'new_password','role_id':1})
        mock_role = self.create_mock_role(roles_constants.PSS_ADMIN)
        mock_role.role_id=1
        self.mock_tables.AdminRoles.query.filter_by().first.return_value = mock_role
        
        self.mock_tables.PssUsers.return_value = self.mock_new_user
        self.mock_tables.PssUsers.query.filter_by().first.return_value = None
        
        created_user = pss_user.create_pss_user_route(self.mock_tables,self.mock_request,self.mock_app)
        self.assertEquals(self.mock_new_user,created_user)

    def test_create_pss_user_route_fails_with_incomplete_request_data(self):
        self.mock_request.data = json.dumps({})
        with self.assertRaises(Exception) as cm:        
            created_user = pss_user.create_pss_user_route(self.mock_tables,self.mock_request,self.mock_app)

    def test_create_pss_user_route_fails_with_invalid_role_id(self):
        self.mock_request.data = json.dumps({'username':'new_user','password':'new_password','role_id':1})
        self.mock_tables.AdminRoles.query.filter_by().first.return_value = None
        with self.assertRaises(Exception) as cm:        
            created_user = pss_user.create_pss_user_route(self.mock_tables,self.mock_request,self.mock_app)
        
    def test_check_pss_user_admin_site_access_throws_exception_with_incorrect_roles(self):        
        with self.assertRaises(Exception) as cm:
            auth.check_pss_user_has_admin_site_access(self.mock_user_with_incorrect_permissions)            

