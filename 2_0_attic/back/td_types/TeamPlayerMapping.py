def generate_player_team_mapping(db_handle):
    Team_Player_mapping = db_handle.Table(
        'team_player_mapping',
        db_handle.Column('player_id', db_handle.Integer, db_handle.ForeignKey('player.player_id')),
        db_handle.Column('team_id', db_handle.Integer, db_handle.ForeignKey('team.team_id'))
)
    return Team_Player_mapping
