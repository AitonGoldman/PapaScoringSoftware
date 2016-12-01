from flask_restless.helpers import to_dict

def generate_score_class(db_handle):    
    class Score(db_handle.Model):
        score_id = db_handle.Column(db_handle.Integer, primary_key=True)
        score = db_handle.Column(db_handle.BIGINT)            
        
        entry_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'entry.entry_id'
        ))
    
        entry = db_handle.relationship(
            'Entry',
            foreign_keys=[entry_id]
        )
        
        division_machine_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
            'division_machine.division_machine_id'
        ))
    
        division_machine = db_handle.relationship(
            'DivisionMachine',
            foreign_keys=[division_machine_id]
        )
        
        def to_dict_simple(self):
            return to_dict(self)
                    
    return Score
