import unittest
from mock import MagicMock
from pss_unit_test_base import PssUnitTestBase,MockRequest
from pss_models_v2.PssUsers import generate_pss_users_class
from pss_models_v2.Events import generate_events_class
from flask_sqlalchemy import SQLAlchemy
from lib_v2.serializers import generic,deserializer


class SerializersTest(PssUnitTestBase):            

    def setUp(self):
        self.sqlalchemy_pss_user = generate_pss_users_class(SQLAlchemy())()
        self.sqlalchemy_pss_user.first_name='test_first'
        self.sqlalchemy_pss_user.last_name='test_last'
        self.sqlalchemy_pss_user.pss_user_id=1

        self.sqlalchemy_event = generate_events_class(SQLAlchemy())()
        self.sqlalchemy_event.name='test_event'
        self.sqlalchemy_event.stripe_api_key='test_private'
        self.sqlalchemy_event.stripe_public_key='test_private'
        self.sqlalchemy_event.ionic_profile='test_private'
        self.sqlalchemy_event.ionic_api_key='test_private'
        self.sqlalchemy_event.ifpa_api_key='test_private'
         
    def test_deserializer(self):
        self.sqlalchemy_pss_user_empty = generate_pss_users_class(SQLAlchemy())()
        test_input={
            'first_name':'test_first',
            'last_name':'test_last',
            'pss_user_id':1,
            'username':'test_username'
        }
        deserializer.deserialize_json(self.sqlalchemy_pss_user_empty,test_input)
        self.assertEquals(self.sqlalchemy_pss_user_empty.pss_user_id,None)
        self.assertEquals(self.sqlalchemy_pss_user_empty.first_name,'test_first')
        self.assertEquals(self.sqlalchemy_pss_user_empty.last_name,'test_last')
        self.assertEquals(self.sqlalchemy_pss_user_empty.username,'test_username')        

    def test_deserializer_with_foreign_keys(self):
        pass

    def test_pss_user_serializer(self):                
        pss_user_dict = generic.serialize_pss_user_public(self.sqlalchemy_pss_user)
        self.assertEquals(pss_user_dict['first_name'],'test_first')
        self.assertEquals(pss_user_dict['last_name'],'test_last')        
        self.assertFalse('password_crypt' in pss_user_dict)

    def test_pss_event_serializer(self):                
        event_dict = generic.serialize_event_public(self.sqlalchemy_event)
        self.assertEquals(event_dict['name'],'test_event')
        self.assertFalse('stripe_api_key' in event_dict)
        self.assertFalse('stripe_public_key' in event_dict)
        self.assertFalse('ionic_profile' in event_dict)
        self.assertFalse('ionic_api_key' in event_dict) 
        self.assertFalse('ifpa_api_key' in event_dict)
            
