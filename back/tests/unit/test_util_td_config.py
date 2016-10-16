import unittest
from app.util import td_config
import tempfile
from flask import Flask
import os

class UtilTdConfigTD(unittest.TestCase):
    def create_flask_config_file(self,config_path,contents=None):
        config_file = open(config_path,'w')        
        if contents:
            config_file.write(contents)
        config_file.close()

    def setUp(self):
        self.good_td_public_config_path = tempfile.mkstemp()[1]
        self.good_td_secret_config_path = tempfile.mkstemp()[1]
        self.bad_td_secret_config_path = tempfile.mkstemp()[1]
        self.good_flask_config_path = tempfile.mkstemp()[1]
        self.create_flask_config_file(self.good_td_public_config_path)
        self.create_flask_config_file(self.good_td_secret_config_path,'flask_secret_key="poop"')
        self.create_flask_config_file(self.bad_td_secret_config_path)
        self.create_flask_config_file(self.good_flask_config_path)        
        
    
    def test_assign_loaded_config(self):                 
        flask_app = Flask("dummy_app")
        td_config.assign_loaded_config(flask_app,self.good_td_public_config_path,self.good_td_secret_config_path)
        self.assertTrue(hasattr(flask_app,'td_secret_config'))
        self.assertTrue(hasattr(flask_app,'td_config'))
        with self.assertRaises(Exception):
            td_config.assign_loaded_config(flask_app,self.good_td_public_config_path,self.bad_td_secret_config_path)
        self.assertTrue(flask_app.td_config['sqlite'] is False)
            
    def test_assign_loaded_config_using_env_file_names(self):                 
        flask_app = Flask("dummy_app")
        os.environ['flask_config_filename']=self.good_flask_config_path
        os.environ['td_public_config_filename']=self.good_td_public_config_path
        os.environ['td_secret_config_filename']=self.good_td_secret_config_path

        self.create_flask_config_file(self.good_td_public_config_path,'test_public_param="testing1"')
        self.create_flask_config_file(self.good_td_secret_config_path,'flask_secret_key="testing2"')        
        self.create_flask_config_file(self.good_flask_config_path,'SESSION_COOKIE_NAME="testing3"')        
        
        td_config.assign_loaded_config(flask_app)
        self.assertTrue(flask_app.td_secret_config['flask_secret_key']=='testing2')
        self.assertTrue(flask_app.td_config['test_public_param']=='testing1')
        self.assertTrue(flask_app.config['SESSION_COOKIE_NAME']=='testing3')

        
        
