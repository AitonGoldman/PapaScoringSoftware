from flask_restless.helpers import to_dict

def generate_division_final_qualifier_tiebreaker_class(db_handle,relationship=None,fk=None):    
    class DivisionFinalQualifierTiebreaker(db_handle.Model):        
        division_final_qualifier_tiebreaker_id = db_handle.Column(db_handle.Integer, primary_key=True)
        division_final_id = db_handle.Column(db_handle.Integer,
                                             db_handle.ForeignKey(
                                                 'division_final.division_final_id'))
        machine_name = db_handle.Column(db_handle.String(100))
        def to_dict_simple(self):
            export_dict = to_dict(self)
            return export_dict
        
    return DivisionFinalQualifierTiebreaker
