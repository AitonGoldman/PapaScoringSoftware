curl -X POST -H "Content-Type: application/json" -b /tmp/cookie -d "[[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7],[8,8],[9,9],[10,10],[11,11],[12,12],[13,13],[14,14],[15,15],[16,16],[17,17],[18,18],[19,19],[20,20],[21,21],[22,22],[23,23],[24,24]]" http://0.0.0.0:8000/elizabeth/finals/division/1
curl -X PUT -H "Content-Type: application/json" -b /tmp/cookie http://0.0.0.0:8000/elizabeth/finals/finals_match_game_result/1/game_name/poop

curl -X PUT -H "Content-Type: application/json" -b /tmp/cookie http://0.0.0.0:8000/elizabeth/finals/finals_match_game_player_result/1/finals_player/9/play_order/1
curl -X PUT -H "Content-Type: application/json" -b /tmp/cookie http://0.0.0.0:8000/elizabeth/finals/finals_match_game_player_result/2/finals_player/16/play_order/2
curl -X PUT -H "Content-Type: application/json" -b /tmp/cookie http://0.0.0.0:8000/elizabeth/finals/finals_match_game_player_result/3/finals_player/17/play_order/3
curl -X PUT -H "Content-Type: application/json" -b /tmp/cookie http://0.0.0.0:8000/elizabeth/finals/finals_match_game_player_result/4/finals_player/24/play_order/4

curl -X PUT -H "Content-Type: application/json" -b /tmp/cookie http://0.0.0.0:8000/elizabeth/finals/finals_match_game_player_result/5/finals_player/9/play_order/1
curl -X PUT -H "Content-Type: application/json" -b /tmp/cookie http://0.0.0.0:8000/elizabeth/finals/finals_match_game_player_result/6/finals_player/16/play_order/2
curl -X PUT -H "Content-Type: application/json" -b /tmp/cookie http://0.0.0.0:8000/elizabeth/finals/finals_match_game_player_result/7/finals_player/17/play_order/3
curl -X PUT -H "Content-Type: application/json" -b /tmp/cookie http://0.0.0.0:8000/elizabeth/finals/finals_match_game_player_result/8/finals_player/24/play_order/4

curl -X PUT -H "Content-Type: application/json" -b /tmp/cookie http://0.0.0.0:8000/elizabeth/finals/finals_match_game_player_result/9/finals_player/9/play_order/1
curl -X PUT -H "Content-Type: application/json" -b /tmp/cookie http://0.0.0.0:8000/elizabeth/finals/finals_match_game_player_result/10/finals_player/16/play_order/2
curl -X PUT -H "Content-Type: application/json" -b /tmp/cookie http://0.0.0.0:8000/elizabeth/finals/finals_match_game_player_result/11/finals_player/17/play_order/3
curl -X PUT -H "Content-Type: application/json" -b /tmp/cookie http://0.0.0.0:8000/elizabeth/finals/finals_match_game_player_result/12/finals_player/24/play_order/4

curl -X PUT -H "Content-Type: application/json" -b /tmp/cookie http://0.0.0.0:8000/elizabeth/finals/finals_match_game_player_result/1/score/2
curl -X PUT -H "Content-Type: application/json" -b /tmp/cookie http://0.0.0.0:8000/elizabeth/finals/finals_match_game_player_result/2/score/1
curl -X PUT -H "Content-Type: application/json" -b /tmp/cookie http://0.0.0.0:8000/elizabeth/finals/finals_match_game_player_result/3/score/0
curl -X PUT -H "Content-Type: application/json" -b /tmp/cookie http://0.0.0.0:8000/elizabeth/finals/finals_match_game_player_result/4/score/4

curl -X PUT -H "Content-Type: application/json" -b /tmp/cookie http://0.0.0.0:8000/elizabeth/finals/finals_match_game_result/1/completed

curl -X PUT -H "Content-Type: application/json" -b /tmp/cookie http://0.0.0.0:8000/elizabeth/finals/finals_match_game_player_result/5/score/2
curl -X PUT -H "Content-Type: application/json" -b /tmp/cookie http://0.0.0.0:8000/elizabeth/finals/finals_match_game_player_result/6/score/4
curl -X PUT -H "Content-Type: application/json" -b /tmp/cookie http://0.0.0.0:8000/elizabeth/finals/finals_match_game_player_result/7/score/1
curl -X PUT -H "Content-Type: application/json" -b /tmp/cookie http://0.0.0.0:8000/elizabeth/finals/finals_match_game_player_result/8/score/0

curl -X PUT -H "Content-Type: application/json" -b /tmp/cookie http://0.0.0.0:8000/elizabeth/finals/finals_match_game_result/2/completed

curl -X PUT -H "Content-Type: application/json" -b /tmp/cookie http://0.0.0.0:8000/elizabeth/finals/finals_match_game_player_result/9/score/2
curl -X PUT -H "Content-Type: application/json" -b /tmp/cookie http://0.0.0.0:8000/elizabeth/finals/finals_match_game_player_result/10/score/1
curl -X PUT -H "Content-Type: application/json" -b /tmp/cookie http://0.0.0.0:8000/elizabeth/finals/finals_match_game_player_result/11/score/4
curl -X PUT -H "Content-Type: application/json" -b /tmp/cookie http://0.0.0.0:8000/elizabeth/finals/finals_match_game_player_result/12/score/0

curl -X PUT -H "Content-Type: application/json" -b /tmp/cookie http://0.0.0.0:8000/elizabeth/finals/finals_match_game_result/3/completed

curl -X PUT -H "Content-Type: application/json" -b /tmp/cookie http://0.0.0.0:8000/elizabeth/finals/division_final_match/1/completed

#curl -b /tmp/cookie -H "Content-Type: application/json" -X PUT -d "{\"finals_player_selection_type\":\"ppo\",\"finals_num_qualifiers_ppo_a\":\"1\",\"finals_num_qualifiers_ppo_b\":\"2\",\"ppo_a_ifpa_range_end\":\"150\",\"division_id\":\"1\",\"finals_num_qualifiers\":\"2\"}" $POPULATE_URL:8000/elizabeth/division/1
