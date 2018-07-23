def generate_machines_class(db_handle):
    class Machines(db_handle.Model):        
        # pylint: disable=no-init
        # pylint can't find SQLAlchemy's __init__() method for some reason                
        machine_id = db_handle.Column(db_handle.Integer, primary_key=True)
        machine_name = db_handle.Column(db_handle.String(1000))
        search_name = db_handle.Column(db_handle.String(1000))
        year = db_handle.Column(db_handle.SmallInteger())
        abbreviation = db_handle.Column(db_handle.String(10))
        
    return Machines
    
