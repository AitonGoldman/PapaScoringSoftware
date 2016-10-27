import unittest
from util.db_info import DbInfo
import tempfile
from flask import Flask
import os

class UtilPgInfoTD(unittest.TestCase):
    #FIXME : need to take new config structure into account
    def test_sqlite_DbInfo(self):
        public_config = {'DB_TYPE':'sqlite'}
        new_db_info = DbInfo({'DB_TYPE':'sqlite'})
        self.assertEqual(new_db_info.is_sqlite(),True)
        self.assertEqual(new_db_info.is_postgres(),False)                 

    def test_postgres_DbInfo(self):
        db_config = {'DB_TYPE':'postgres','DB_USERNAME':'user','DB_PASSWORD':'password'}        
        new_db_info = DbInfo(db_config)
        self.assertEqual(new_db_info.is_sqlite(),False)
        self.assertEqual(new_db_info.is_postgres(),True)                 
        self.assertEqual(new_db_info.db_username,'user')                 
        self.assertEqual(new_db_info.db_password,'password')                 
                
    def test_invalid_DbInfo(self):
        with self.assertRaises(Exception):
            new_db_info = DbInfo({},{})            
        with self.assertRaises(Exception):
            public_config = {'DB_TYPE':'postgres'}            
            new_db_info = DbInfo(public_config,{})            
        with self.assertRaises(Exception):
            public_config = {'DB_TYPE':'postgres','DB_USERNAME':'user'}                        
            new_db_info = DbInfo(public_config)            
 
                                
        
