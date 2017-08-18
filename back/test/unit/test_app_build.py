import unittest
from mock import MagicMock
from pss_unit_test_base import PssUnitTestBase
from lib.flask_lib import app_build
from lib import CustomJsonEncoder
from flask import Flask
from flask_principal import Principal
from lib.PssConfig import PssConfig

class AppBuildTest(PssUnitTestBase):    
    def setUp(self):
        pass    
    
    def test_get_base_app_for_existing_event(self):
        #FIXME : need unit tests for pss config and db_info
        app = Flask('poop')        
        app.tables = MagicMock()
        fake_events = [self.tables.Events(name='poop2'),
                       self.tables.Events(name='poop3'),
                       self.tables.Events(name='poop',flask_secret_key='poop_key',upload_folder='/tmp')]
        
        app.tables.Events.query.all.return_value=fake_events
        mock_pss_config = MagicMock()
        configured_app = app_build.get_base_app(app,mock_pss_config)        
        custom_json_encoder = configured_app.json_encoder("test string to encode")
        principals = configured_app.my_principals
        self.assertTrue(type(custom_json_encoder) is CustomJsonEncoder.CustomJSONEncoder)
        self.assertTrue(type(principals) is Principal)
        mock_pss_config.set_event_config_from_db.assert_called_once_with(app)
        self.assertEquals(len(configured_app.error_handler_spec[None].keys()),27)
        self.assertTrue(400 in configured_app.error_handler_spec[None])

        pass        
        
    def test_get_base_app_for_nonexistent_event(self):
        app = Flask('poop')        
        app.tables = MagicMock()
        fake_events = [self.tables.Events(name='poop2'),
                       self.tables.Events(name='poop3'),
                       self.tables.Events(name='poop4')]
        
        app.tables.Events.query.all.return_value=fake_events
        with self.assertRaises(Exception) as cm:
            app_build.get_base_app(app,PssConfig())                    
        self.assertEquals(cm.exception.message,'event poop does not exist')

    def test_get_base_app_with_nonexistent_flask_secret_key(self):
        app = Flask('poop')        
        app.tables = MagicMock()
        fake_events = [self.tables.Events(name='poop2'),
                       self.tables.Events(name='poop3'),
                       self.tables.Events(name='poop',upload_folder='/tmp')]
        
        app.tables.Events.query.all.return_value=fake_events
        with self.assertRaises(Exception) as cm:
            app_build.get_base_app(app,PssConfig())                    
        self.assertEquals(cm.exception.message,"You didn't configure your flask secret key!")
        
        
    def test_get_event_app_with_existing_event(self):
        app = Flask('poop2')        
        app.tables = MagicMock()
        fake_events = [self.tables.Events(name='poop2', flask_secret_key='poop2_key',upload_folder='/tmp'),
                       self.tables.Events(name='poop3'),
                       self.tables.Events(name='poop',flask_secret_key='poop_key')]
        
        app.tables.Events.query.all.return_value=fake_events
        pss_config=PssConfig()
        pss_config.pss_admin_event_name='poop'
        configured_app = app_build.get_event_app(app,pss_config)                
        self.assertTrue(hasattr(configured_app,'blueprints'))
        self.assertTrue('event' in configured_app.blueprints)
        
    def test_get_pss_admin_event_app_with_existing_event(self):
        app = Flask('poop')        
        app.tables = MagicMock()
        fake_events = [self.tables.Events(name='poop2'),
                       self.tables.Events(name='poop3'),
                       self.tables.Events(name='poop',flask_secret_key='poop_key',upload_folder='/tmp')]
        
        app.tables.Events.query.all.return_value=fake_events
        pss_config=PssConfig()
        pss_config.pss_admin_event_name='poop'
        configured_app = app_build.get_event_app(app,pss_config)                
        self.assertTrue(hasattr(configured_app,'blueprints'))
        self.assertTrue('pss_admin' in configured_app.blueprints)        
