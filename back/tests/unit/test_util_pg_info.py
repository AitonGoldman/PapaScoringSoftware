import unittest
from app.util import pg_info
import tempfile
from flask import Flask
import os

class UtilPgInfoTD(unittest.TestCase):
    def test_build_PgInfo_from_config_sqlite(self):
        new_pg_info = pg_info.build_PgInfo_from_config({},{'sqlite':'true'})
        self.assertEqual(new_pg_info.use_sqlite,'true')
        self.assertEqual(new_pg_info.pg_username,None)
        self.assertEqual(new_pg_info.pg_password,None)
        self.assertEqual(new_pg_info.pg_hostname,None)        

    def test_build_PgInfo_from_config_pg(self):
        new_pg_info = pg_info.build_PgInfo_from_config({'pg_username':'test_pg_user','pg_password':'test_pg_password'},{})
        self.assertEqual(new_pg_info.use_sqlite,False)
        self.assertEqual(new_pg_info.pg_username,'test_pg_user')
        self.assertEqual(new_pg_info.pg_password,'test_pg_password')
        self.assertEqual(new_pg_info.pg_hostname,None)        
        
    def test_build_PgInfo_invalid(self):
        with self.assertRaises(Exception):
            new_pg_info = pg_info.build_PgInfo_from_config({},{})
                                
        
