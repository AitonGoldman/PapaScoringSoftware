import unittest
from mock import MagicMock
from pss_unit_test_base import PssUnitTestBase
from lib.flask_lib import app_build
from lib import CustomJsonEncoder
from flask import Flask
from flask_principal import Principal
from lib.PssConfig import PssConfig
from routes import auth

class RouteLoginTest(PssUnitTestBase):    
    def setUp(self):
        pass    
    
    def test_login(self):
        pass
