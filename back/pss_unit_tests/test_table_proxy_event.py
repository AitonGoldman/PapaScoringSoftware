import unittest
from mock import MagicMock
from pss_unit_test_base import PssUnitTestBase
from pss_models_v2.PssUsers import generate_pss_users_class
from pss_models_v2.Events import generate_events_class
from flask_sqlalchemy import SQLAlchemy


class TablesProxyEventTest(PssUnitTestBase):        
    def setUp(self):
        self.sqlalchemy_event = generate_events_class(SQLAlchemy())()
        self.sqlalchemy_pss_user = generate_pss_users_class(SQLAlchemy())()
        self.tables_proxy.Events = MagicMock()

    def test_create_event(self):
        self.tables_proxy.Events.return_value=self.sqlalchemy_event
        self.sqlalchemy_pss_user.pss_user_id=1 
        self.sqlalchemy_event.event_id=1
        event_input_info={
            'name':'test_event'            
        }
        return_value = self.tables_proxy.create_event(self.sqlalchemy_pss_user,event_input_info)
        self.assertEquals(self.sqlalchemy_event.event_id,1)
        self.assertEquals(self.sqlalchemy_event.name,'test_event')

        
