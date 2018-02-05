def remove_player_with_notification(player,app,tournament_machine, event_id):
    with app.table_proxy.db_handle.session.no_autoflush:                
        try:                                    
            existing_queue = app.table_proxy.get_queue_player_is_already_in(player,event_id)                        
            if existing_queue:                
                tournament_machine_to_remove_from = app.table_proxy.get_tournament_machine_by_id(existing_queue.tournament_machine_id)
                existing_position = existing_queue.position                                                                
                app.table_proxy.remove_player_from_queue(player,
                                                         tournament_machine_to_remove_from,
                                                         position_in_queue=existing_position)
                
                #if app.event_settings[event_id].ionic_api_key:                
                #    notification_helpers.notify_list_of_players(queues[existing_position:],"test message")
                    
        except Exception as e:            
            app.table_proxy.db_handle.session.commit()            
            raise e            
