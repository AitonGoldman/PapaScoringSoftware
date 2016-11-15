"""Model object for a meta division"""

from flask_restless.helpers import to_dict

def generate_meta_division_class(db_handle):
    class MetaDivision(db_handle.Model):
        meta_division_id = db_handle.Column(db_handle.Integer, primary_key=True)
        meta_division_name = db_handle.Column(db_handle.String(1000))
        meta_division_id = db_handle.Column(db_handle.Integer, primary_key=True)
        divisions = db_handle.relationship("Division")
        
        def to_dict_simple(self):
            metadivision = to_dict(self)
            if self.divisions:
                metadivision['divisions'] = {}
                for division in self.divisions:
                    metadivision['divisions'][division.division_id] = division.to_dict_simple()
            return metadivision
    
    return MetaDivision
            

