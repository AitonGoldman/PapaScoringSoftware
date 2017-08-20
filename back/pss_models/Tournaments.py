def generate_tournaments_class(db_handle,event_name):
    class Tournaments(db_handle.Model):        
        # pylint: disable=no-init
        # pylint can't find SQLAlchemy's __init__() method for some reason                
        __tablename__="tournaments_"+event_name                

        tournament_id = db_handle.Column(db_handle.Integer, primary_key=True)
        tournament_name = db_handle.Column(db_handle.String(1000))                
    return Tournaments
    
