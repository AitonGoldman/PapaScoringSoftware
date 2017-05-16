from flask_restless.helpers import to_dict

def generate_division_final_round_class(db_handle,relationship=None,fk=None):    
    class DivisionFinalRound(db_handle.Model):        
        division_final_round_id = db_handle.Column(db_handle.Integer, primary_key=True)
        division_final_id = db_handle.Column(db_handle.Integer,db_handle.ForeignKey('division_final.division_final_id'))
        round_number = db_handle.Column(db_handle.String(5))
        number_of_matches = db_handle.Column(db_handle.Integer)
        completed = db_handle.Column(db_handle.Boolean,default=False)
        division_final_matches = db_handle.relationship('DivisionFinalMatch',cascade="all, delete, delete-orphan")
        
        def to_dict_simple(self):
            division_final_round_dict = to_dict(self)
            if len(self.division_final_matches) > 0:
                division_final_round_dict['division_final_matches'] = []
                for match in self.division_final_matches:
                    division_final_round_dict['division_final_matches'].append(match.to_dict_simple())
            return division_final_round_dict
        
    return DivisionFinalRound
