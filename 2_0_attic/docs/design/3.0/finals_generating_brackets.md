# resolve tiebreakers - overview
- for each group of tied players, display tied players
  - input box for machine to record score on
  - for each player, list name and input box to record score
  - save scores for each tiebreaker 
- button to click when tiebreakers are resolved  

# resolve tiebreakers - backend
- /initialize_division_final
 - includes initialize_division_final_players()
- /get_list_of_tiebreakers
- /record_scores_for_tiebreaker

# resolve tiebreakers - /initialize_division_final 
- create division_final
- create division_final_players
  - get rankings for division
  - loop through and create division_final_player
  

# resolve tiebreakers - tables
- division_final
  - division_final_id
  - name
  - division_id (fk)
- division_final_player
  - division_final_player_id
  - player_id(fk)
  - player_name
  - final_rank
  - adjusted_rank
  - division_final_id(fk)
- division_final_qualifier_tiebreaker
  - division_final_qualifier_tiebreaker_id
  - division_final_id
  - machine_name
- division_final_qualifier_tiebreaker_results
  - division_final_qualifier_tiebreaker_results_id
  - division_final_qualifier_tiebreaker_id  
  - division_final_player_id
  - score
  
  
