import os
from celery_app.celery_app import send_indiv_message

def nth(d):
    if(d>3 and d<21):
        return 'th'
    remainder = d % 10
    if remainder == 1:
        return "st"
    if remainder == 2:
        return "nd"
    if remainder == 3:
        return "rd"
    return "th"

def remove_player_with_notification(player,app,tournament_machine, event_id):
    with app.table_proxy.db_handle.session.no_autoflush:                
        try:                                    
            existing_queue = app.table_proxy.get_queue_player_is_already_in(player,event_id)                        
            if existing_queue:                
                tournament_machine_to_remove_from = app.table_proxy.get_tournament_machine_by_id(existing_queue.tournament_machine_id)
                existing_position = existing_queue.position                                                                
                players_to_alert = app.table_proxy.remove_player_from_queue(player,
                                                                            tournament_machine_to_remove_from,
                                                                            position_in_queue=existing_position)
                if os.getenv('FCM_API_KEY') and len(players_to_alert)>0:
                    title="Queue Position Changed"
                    for player in players_to_alert:
                        if player['token'] is None:
                            continue
                        position = nth(player['position'])
                        msg = "You're queue position for %s is now %s%s" % (player['machine_name'],player['position'],nth(player['position']))
                        if player['position']==1:
                            msg = "You are next to play %s" % (player['machine_name']) 
                        
                        send_indiv_message.delay(title,msg,player['token'])
                #if app.event_settings[event_id].ionic_api_key:                
                #    notification_helpers.notify_list_of_players(queues[existing_position:],"test message")
                    
        except Exception as e:            
            app.table_proxy.db_handle.session.commit()            
            raise e            
