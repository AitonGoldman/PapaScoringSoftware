from flask_restless.helpers import to_dict

def generate_division_final_class(db_handle,relationship=None,fk=None):    
    class DivisionFinal(db_handle.Model):        
        division_final_id = db_handle.Column(db_handle.Integer, primary_key=True)
        division_id = db_handle.Column(db_handle.Integer,db_handle.ForeignKey('division.division_id'))
        qualifiers = db_handle.relationship('DivisionFinalPlayer')
        division = db_handle.relationship('Division')        
        division_final_rounds = db_handle.relationship("DivisionFinalRound",cascade="all, delete, delete-orphan",single_parent=True)
        #extra_name_info = db_handle.Column(db_handle.String(100))
        name = db_handle.Column(db_handle.String(100))

        def to_dict_simple(self):
            division_final_dict = to_dict(self)
            # if len(self.qualifiers) > 0:
            #     division_final_dict['qualifiers'] = []
            #     for qualifier in self.qualifiers:
            #         division_final_dict['qualifiers'].append(qualifier.to_dict_simple())
            if len(self.division_final_rounds) > 0:
                division_final_dict['division_final_rounds'] = []
                for round in sorted(self.division_final_rounds, key= lambda e: e.round_number):
                    division_final_dict['division_final_rounds'].append(round.to_dict_simple())
            
            return division_final_dict
        
    return DivisionFinal
