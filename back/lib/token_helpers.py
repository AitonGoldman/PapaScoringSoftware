from sqlalchemy import and_,or_
from sqlalchemy import func

def get_number_of_unused_tickets_for_player_in_all_tournaments(player,app,remove_empty_tournaments=False):
    token_count_per_tournament=[]
    token_count_per_meta_tournament=[]
    #query = app.tables.Tokens.query.filter_by(used=False,voided=False,paid_for=True,deleted=False)
    #if player.event_player.team_id:
    #    tokens = query.filter(or_(app.tables.Tokens.player_id==player.player_id,app.tables.Tokens.team_id==player.event_player.team_id)).all()
    #else:
    #    tokens = query.filter(or_(app.tables.Tokens.player_id==player.player_id,app.tables.Tokens.team_id==player.event_player.team_id)).all()
    #token_tally={}
    tournament_results = app.tables.db_handle.session.query(func.count(app.tables.Tokens.tournament_id),app.tables.Tokens.tournament_id,app.tables.Tournaments.tournament_name).join(app.tables.Tournaments).group_by(app.tables.Tokens.tournament_id,app.tables.Tournaments.tournament_name).all()
    for result in tournament_results:
        token_count_per_tournament.append({'tournament_name':result.tournament_name,
                                           'tournament_id':result.tournament_id,
                                           'count':int(result[0])})
    meta_tournament_results = app.tables.db_handle.session.query(func.count(app.tables.Tokens.meta_tournament_id),app.tables.Tokens.meta_tournament_id,app.tables.MetaTournaments.meta_tournament_name).join(app.tables.MetaTournaments).group_by(app.tables.Tokens.meta_tournament_id,app.tables.MetaTournaments.meta_tournament_name).all()
    for result in meta_tournament_results:
        token_count_per_meta_tournament.append({'meta_tournament_name':result.meta_tournament_name,
                                                'meta_tournament_id':result.meta_tournament_id,
                                                'count':int(result[0])})

    
    # for tournament in app.tables.Tournaments.query.filter_by(meta_tournament_id=None).all():
    #     count = get_number_of_unused_tickets_for_player(player,app,tournament=tournament)
    #     token_count_per_tournament.append({'tournament_name':tournament.tournament_name,
    #                                        'tournament_id':tournament.tournament_id,
    #                                        'count':count})
    # for meta_tournament in app.tables.MetaTournaments.query.all():
    #     count = get_number_of_unused_tickets_for_player(player,app,meta_tournament=meta_tournament)
    #     token_count_per_meta_tournament.append({'meta_tournament_name':meta_tournament.meta_tournament_name,
    #                                             'meta_tournament_id':meta_tournament.meta_tournament_id,
    #                                             'count':count})
    # token_count_per_tournament=[token_count for token_count in token_count_per_tournament if token_count['count'] != 0 ]
    # token_count_per_meta_tournament=[token_count for token_count in token_count_per_meta_tournament if token_count['count'] != 0 ]
    return token_count_per_tournament,token_count_per_meta_tournament

def get_number_of_unused_tickets_for_player(player,flask_app,meta_tournament=None,tournament=None):
    #FIXME : explore if it makes sense to query al tokens (for all divisions) at once
    query = flask_app.tables.Tokens.query.filter_by(used=False,voided=False,paid_for=True,deleted=False)
    if player.event_player.team_id is None and tournament and tournament.team_tournament:
        return 0
    if tournament:
        if tournament.team_tournament is True:
            token_count = query.filter_by(tournament_id=tournament.tournament_id,team_id=player.event_player.team_id).count()            
        else:            
            token_count = query.filter_by(player_id=player.player_id,tournament_id=tournament.tournament_id).count()
    if meta_tournament:
        token_count = query.filter_by(meta_tournament_id=meta_tournament.meta_tournament_id).count()    
    return token_count

def get_normal_and_discount_amounts(tournament,amount):
    if tournament.number_of_tickets_for_discount:
        if amount < tournament.number_of_tickets_for_discount:
            return (amount,0)
        if amount == tournament.number_of_tickets_for_discount:
            return (0,1)        
        return (amount%tournament.number_of_tickets_for_discount,int(amount/tournament.number_of_tickets_for_discount))
    else:
        return (amount,0)
    pass

