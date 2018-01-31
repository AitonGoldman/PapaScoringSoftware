def generate_finals_class(db_handle):
    class Finals(db_handle.Model):        
        final_id=db_handle.Column(db_handle.Integer, primary_key=True)
        tournament_id=db_handle.Column('tournament_id', db_handle.Integer, db_handle.ForeignKey('tournaments.tournament_id'))
        name=db_handle.Column(db_handle.String(1000))
    return Finals
