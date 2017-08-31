def generate_teams_class(db_handle,event_name):
    class Teams(db_handle.Model):        
        # pylint: disable=no-init
        # pylint can't find SQLAlchemy's __init__() method for some reason        
        __tablename__="teams_"+event_name                
        team_id=db_handle.Column(db_handle.Integer, primary_key=True)
        team_name=db_handle.Column(db_handle.String(100))
        event_players = db_handle.relationship('EventPlayers')

    return Teams
    
