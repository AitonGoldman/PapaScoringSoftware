from flask_restless.helpers import to_dict

def generate_division_final_round_class(db_handle,relationship=None,fk=None):    
    class DivisionFinalRound(db_handle.Model):        
        division_final_round_id = db_handle.Column(db_handle.Integer, primary_key=True)
        round_number = db_handle.Column(db_handle.Integer)
        number_matches = db_handle.Column(db_handle.Integer)
        completed = db_handle.Column(db_handle.Boolean)        

        def to_dict_simple(self):
            return to_dict(self)        
        
    return DivisionFinalRound
