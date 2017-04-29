#export URL="/elizabeth/token/paid_for/1"
#curl -b /tmp/cookie -s -o /tmp/test_out_$1.out -w "\npeekaboo - $1 - %{time_total}" -H "Content-Type: application/json" -d "{\"player_id\":1,\"divisions\":{\"1\":[\"25\",\"0\"]},\"teams\":{\"5\":[\"0\",\"0\"]},\"metadivisions\":{\"1\":[\"0\",\"0\"]}}" http://localhost:8000/$URL > /tmp/time_$1.out 2>&1 &

export URL="http://0.0.0.0:8000/elizabeth/results/player/$1"
sleep .1
curl -b /tmp/cookie -s -o /tmp/test_out_player_results_$1.out -w "\npeekaboo - $1 - %{time_total}" -H "Content-Type: application/json" $URL > /tmp/time_player_results_$1.out 2>&1 &
