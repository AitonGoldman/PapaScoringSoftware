import unittest
from routes.utils import fetch_entity
from mock import MagicMock

class RouteUtilTD(unittest.TestCase):    
    def setUp(self):
        pass
    def test_fetch_entity(self):
        model_class = MagicMock()
        returned_value="returned_value"
        model_class.query.get.return_value=returned_value
        returned_entity = fetch_entity(model_class,123)
        self.assertEquals(returned_entity,returned_value)
        
