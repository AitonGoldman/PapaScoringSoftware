from passlib.hash import sha512_crypt
from sqlalchemy.schema import Sequence
"""Model object for a EventPlayers"""
def generate_event_players_class(db_handle,event_name):
    class EventPlayers(db_handle.Model):
        # pylint: disable=no-init
        # pylint can't find SQLAlchemy's __init__() method for some reason        
        __tablename__="event_players_"+event_name                
        #FIXME : rename this event_player_number
        event_player_id = db_handle.Column(db_handle.Integer, Sequence('event_player_seq_'+event_name))
        player_id = db_handle.Column('player_id', db_handle.Integer, db_handle.ForeignKey('players.player_id'),primary_key=True)
        event_player_pin = db_handle.Column(db_handle.Integer)        
        ifpa_ranking = db_handle.Column(db_handle.Integer)        
        multi_division_tournament_id = db_handle.Column("tournament_id", db_handle.Integer, db_handle.ForeignKey("tournaments_"+event_name+".tournament_id"))
        active=db_handle.Column(db_handle.Boolean(),default=True)
        team_id = db_handle.Column('team_id', db_handle.Integer, db_handle.ForeignKey('teams_'+event_name+'.team_id'))
        team = db_handle.relationship('Teams',uselist=False)        
        
    return EventPlayers
    