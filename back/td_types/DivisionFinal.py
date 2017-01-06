from flask_restless.helpers import to_dict

def generate_division_final_class(db_handle,relationship=None,fk=None):    
    class DivisionFinal(db_handle.Model):        
        division_final_id = db_handle.Column(db_handle.Integer, primary_key=True)
        number_of_qualifiers = db_handle.Column(db_handle.Integer)

        qualifiers = db_handle.relationship('FinalsPlayer')

        def to_dict_simple(self):
            return to_dict(self)        
        
    return DivisionFinal
