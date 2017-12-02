import unittest
from mock import MagicMock
from pss_unit_test_base import PssUnitTestBase
from pss_models_v2.PssUsers import generate_pss_users_class
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha512_crypt

class TablesProxyPssUserTest(PssUnitTestBase):        
    def setUp(self):
        self.sqlalchemy_pss_user_class = generate_pss_users_class(SQLAlchemy())()
        self.tables_proxy.PssUsers = MagicMock()
        
    def test_get_pss_by_username(self):                
        self.set_mock_single_user_query(self.tables_proxy,self.sqlalchemy_pss_user)        
        return_value = self.tables_proxy.get_user_by_username('whatever')
        self.assertEquals(return_value,self.sqlalchemy_pss_user)        
        filter_by = self.tables_proxy.PssUsers.query.filter_by
        self.assertTrue('username' in filter_by.call_args[1])
        self.assertEquals(filter_by.call_args[1]['username'],'whatever')

    def test_create_user(self):                
        self.tables_proxy.PssUsers.return_value=self.sqlalchemy_pss_user
        return_value = self.tables_proxy.create_user('test_username','test_first_name','test_last_name','password')
        self.assertEquals(return_value.username,'test_username')
        self.assertEquals(return_value.first_name,'test_first_name')
        self.assertEquals(return_value.last_name,'test_last_name')                        
        self.assertTrue(return_value.password_crypt is not None)                        
        self.assertTrue(sha512_crypt.verify('password', return_value.password_crypt))

        
    
