def generate_multi_division_tournaments_class(db_handle):
    class MultiDivisionTournaments(db_handle.Model):        
        # pylint: disable=no-init
        # pylint can't find SQLAlchemy's __init__() method for some reason                        

        multi_division_tournament_id = db_handle.Column(db_handle.Integer, primary_key=True)
        multi_division_tournament_name = db_handle.Column(db_handle.String(1000))                
    return MultiDivisionTournaments
