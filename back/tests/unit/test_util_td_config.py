import unittest
from app.util import td_config
import tempfile
from flask import Flask

class ModelUserTD(unittest.TestCase):
    def setUp(self):
        self.good_td_public_config_path = tempfile.mkstemp()[1]
        self.good_td_secret_config_path = tempfile.mkstemp()[1]
        self.bad_td_secret_config_path = tempfile.mkstemp()[1]        
        self.good_td_public_config = open(self.good_td_public_config_path,'w')        
        self.good_td_public_config.close()
        self.good_td_secret_config = open(self.good_td_secret_config_path,'w')
        self.good_td_secret_config.write('flask_secret_key="poop"')
        self.good_td_secret_config.close()
        self.bad_td_secret_config = open(self.bad_td_secret_config_path,'w')
        self.bad_td_secret_config.close()                
    
    def test_assign_loaded_config(self):                 
        flask_app = Flask("dummy_app")
        td_config.assign_loaded_config(flask_app,self.good_td_public_config_path,self.good_td_secret_config_path)
        self.assertTrue(hasattr(flask_app,'td_secret_config'))
        self.assertTrue(hasattr(flask_app,'td_config'))
        with self.assertRaises(Exception):
            td_config.assign_loaded_config(flask_app,self.good_td_public_config_path,self.bad_td_secret_config_path)
