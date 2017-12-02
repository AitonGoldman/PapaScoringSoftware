import os 
from pss_models_v2.PssUsers import generate_pss_users_class
#from pss_models_v2.TestMapping import generate_test_class



class TableProxy():
    def initialize_tables(self,db_handle):
        self.db_handle=db_handle
        self.PssUsers = generate_pss_users_class(self.db_handle)
        #self.TestMapping = generate_test_class(self.db_handle)
        
    def get_user_by_username(self,username):
        #return self.PssUsers.query.options(joinedload("admin_roles"),joinedload("event_roles"),joinedload("events"),joinedload("event_user")).filter_by(username=input_data['username']).first()
        return self.PssUsers.query.filter_by(username=username).first()            
        
    def create_user(self, username,
                    first_name,last_name,
                    password, event_creator=False,
                    event_roles=[],
                    extra_title=None, commit=False,
                    add_user_to_session=True):        
        user = self.PssUsers()
        user.username=username
        user.first_name=first_name
        user.last_name=last_name
        if extra_title:
            user.extra_title=extra_title
        if event_creator:
            user.event_creator=True
        else:
            user.event_creator=False
        user.crypt_password(password)
        #user.test_mapping.append(self.TestMapping())        
        if add_user_to_session:
            self.db_handle.session.add(user)
        if commit:            
            self.db_handle.session.commit()
        #self.db_handle.session.delete(user)
        #self.db_handle.session.commit()
        return user
    
