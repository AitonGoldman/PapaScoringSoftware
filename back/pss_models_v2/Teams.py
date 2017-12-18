def generate_teams_class(db_handle):
    class Teams(db_handle.Model):        
        # pylint: disable=no-init
        # pylint can't find SQLAlchemy's __init__() method for some reason                
        team_id=db_handle.Column(db_handle.Integer, primary_key=True)
        event_id=db_handle.Column('event_id', db_handle.Integer, db_handle.ForeignKey('events.event_id')) 
        team_name=db_handle.Column(db_handle.String(100))        
    return Teams
    
