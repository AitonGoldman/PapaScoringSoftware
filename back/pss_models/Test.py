from passlib.hash import sha512_crypt

def generate_test_mapping(db_handle):
    test_mapping = db_handle.Table(
        'test_mapping',
        db_handle.Column('pss_user_id', db_handle.Integer, db_handle.ForeignKey('pss_users.pss_user_id')),
        db_handle.Column('event_role_id', db_handle.Integer, db_handle.ForeignKey('event_roles.event_role_id')),
        db_handle.Column('event_id', db_handle.Integer, db_handle.ForeignKey('event.event_id'))        
    )
    return test_mapping

def generate_test_class(db_handle,event_name):
    test_mapping = generate_test_mapping(db_handle)    
    class TestClass(db_handle.Model):
        pass
