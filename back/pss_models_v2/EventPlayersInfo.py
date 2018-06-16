
def generate_event_players_info_class(db_handle):    
    class EventPlayersInfo(db_handle.Model):        
        player_id=db_handle.Column('player_id', db_handle.Integer,
                                   db_handle.ForeignKey('players.player_id'),primary_key=True)
        event_id=db_handle.Column('event_id', db_handle.Integer, db_handle.ForeignKey('events.event_id'),primary_key=True)
        player_id_for_event=db_handle.Column(db_handle.Integer())
        ifpa_ranking=db_handle.Column(db_handle.Integer())
        selected_division_in_multi_division_tournament=db_handle.Column('tournament_id',
                                                                        db_handle.Integer,
                                                                        db_handle.ForeignKey('tournaments.tournament_id'))
        team_id = db_handle.Column('team_id', db_handle.Integer, db_handle.ForeignKey('teams.team_id'))
        email_address = db_handle.Column(db_handle.String(80))
    return EventPlayersInfo
    

                                                     
