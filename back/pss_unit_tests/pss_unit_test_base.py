import unittest
from flask_sqlalchemy import SQLAlchemy
from mock import MagicMock
from lib_v2.TableProxy import TableProxy
from pss_models_v2.PssUsers import generate_pss_users_class
from pss_models_v2.Events import generate_events_class
from pss_models_v2.EventRoles import generate_event_roles_class
from pss_models_v2.EventUsers import generate_event_users_class

class MockRequest():
    def __init__(self,data):
        self.data=data

mock_relationship_map={
    'PssUsers':'event_roles'
}

class PssUnitTestBase(unittest.TestCase):    

    def __init__(self,*args, **kwargs):
        super(PssUnitTestBase, self).__init__(*args, **kwargs)                        
        self.tables_proxy = TableProxy()        
        self.tables_proxy.db_handle=MagicMock()

    def initialize_single_mock(self,tables_proxy,attribute):
        mock_object = MagicMock()        
        if mock_relationship_map.get(attribute,None):            
            setattr(mock_object,mock_relationship_map.get(attribute),[])
        setattr(tables_proxy,attribute,mock_object)                        
        getattr(tables_proxy,attribute).return_value=mock_object
        
        return mock_object

    def initialize_multiple_mocks(self,tables_proxy,attribute,count):
        mock_objects=[]
        for i in range(0,count):
            mock_object = MagicMock()        
            if mock_relationship_map.get(attribute,None):            
                setattr(mock_object,mock_relationship_map.get(attribute),[])
            setattr(tables_proxy,attribute,mock_object)                        
            getattr(tables_proxy,attribute).return_value=mock_object
            mock_objects.append(mock_object)
        return mock_objects
    
    def initialize_single_mock_pss_user(self,tables_proxy,mock_user_create=False):        
        tables_proxy.PssUsers = MagicMock()
        user=generate_pss_users_class(SQLAlchemy())()
        if mock_user_create:
            tables_proxy.PssUsers.return_value=user
        return user

    def initialize_single_mock_event(self,tables_proxy,mock_event_create=False):        
        tables_proxy.Events = MagicMock()
        event = generate_events_class(SQLAlchemy())() 
        if mock_event_create:
            tables_proxy.Events.return_value=event
        return event

    def initialize_single_mock_event_user(self,tables_proxy,mock_event_user_create=False):        
        tables_proxy.EventUsers = MagicMock()
        event_user = generate_event_users_class(SQLAlchemy())()        
        event_user.event_roles = []
        if mock_event_user_create:
            tables_proxy.EventUsers.return_value=event_user
        return event_user
    
    def initialize_single_mock_event_role(self,tables_proxy,mock_event_role_create=False):        
        tables_proxy.EventRoles = MagicMock()
        event_role = generate_event_roles_class(SQLAlchemy())()        
        if mock_event_role_create:
            tables_proxy.EventRoles.return_value=event_role
        return event_role    

    def set_mock_single_query(self,tables_proxy,attribute,mock_to_return):
        getattr(tables_proxy,attribute).query.filter_by().first.return_value=mock_to_return
    def set_mock_multiple_query(self,tables_proxy,attribute,mocks_to_return):
        getattr(tables_proxy,attribute).query.filter_by().first.side_effect=mocks_to_return        
    def set_mock_single_user_query(self,tables_proxy,pss_user_to_return):
        tables_proxy.PssUsers.query.filter_by().first.return_value=pss_user_to_return
    def set_mock_single_event_query(self,tables_proxy,event_to_return):
        tables_proxy.Events.query.filter_by().first.return_value=event_to_return
    def set_mock_single_event_role_query(self,tables_proxy,event_role_to_return):        
        tables_proxy.EventRoles.query.filter_by().first.return_value=event_role_to_return
    def set_mock_single_event_user_query(self,tables_proxy,event_user_to_return):
        tables_proxy.EventUsers.query.filter_by().first.return_value=event_user_to_return                
    def set_mock_multiple_event_query(self,tables_proxy,events_to_return):
        tables_proxy.Events.query.filter_by().first.side_effect=events_to_return
        
        
