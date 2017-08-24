def get_number_of_unused_tickets_for_player_in_all_tournaments(player,app,remove_empty_tournaments=False):
    token_count_per_tournament=[]
    token_count_per_meta_tournament=[]
    for tournament in app.tables.Tournaments.query.filter_by(meta_tournament_id=None).all():
        count = get_number_of_unused_tickets_for_player(player,app,tournament=tournament)
        token_count_per_tournament.append({'tournament_name':tournament.tournament_name,
                                           'tournament_id':tournament.tournament_id,
                                           'count':count})
    for meta_tournament in app.tables.MetaTournaments.query.all():
        count = get_number_of_unused_tickets_for_player(player,app,meta_tournament=meta_tournament)
        token_count_per_meta_tournament.append({'meta_tournament_name':meta_tournament.meta_tournament_name,
                                                'meta_tournament_id':meta_tournament.meta_tournament_id,
                                                'count':count})
    token_count_per_tournament=[token_count for token_count in token_count_per_tournament if token_count['count'] != 0 ]
    token_count_per_meta_tournament=[token_count for token_count in token_count_per_meta_tournament if token_count['count'] != 0 ]
    return token_count_per_tournament,token_count_per_meta_tournament

def get_number_of_unused_tickets_for_player(player,flask_app,meta_tournament=None,tournament=None):
    #FIXME : explore if it makes sense to query al tokens (for all divisions) at once
    query = flask_app.tables.Tokens.query.filter_by(used=False,voided=False,paid_for=True,deleted=False)
    if player.team_id is None and tournament and tournament.team_tournament:
        return 0
    if tournament:
        if tournament.team_tournament is True:
            token_count = query.filter_by(tournament_id=tournament.tournament_id,team_id=player.team_id).count()            
        else:            
            token_count = query.filter_by(player_id=player.player_id,tournament_id=tournament.tournament_id).count()
    if meta_tournament:
        token_count = query.filter_by(meta_tournament_id=meta_tournament.meta_tournament_id).count()    
    return token_count
