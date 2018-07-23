#export URL="/elizabeth/token/paid_for/1"
#curl -b /tmp/cookie -s -o /tmp/test_out_$1.out -w "\npeekaboo - $1 - %{time_total}" -H "Content-Type: application/json" -d "{\"player_id\":1,\"divisions\":{\"1\":[\"25\",\"0\"]},\"teams\":{\"5\":[\"0\",\"0\"]},\"metadivisions\":{\"1\":[\"0\",\"0\"]}}" http://localhost:8000/$URL > /tmp/time_$1.out 2>&1 &

export URL="http://0.0.0.0:8000/elizabeth/team"
sleep .1
curl -X POST -b /tmp/cookie -s -o /tmp/test_out_add_team_$1.out -d "{\"player_one_id\":\"$1\",\"player_two_id\":\"$2\"}" -w "\npeekaboo - $1 - %{time_total}" -H "Content-Type: application/json" $URL > /tmp/time_add_team_$1.out 2>&1 &


#/tmp/test_out_add_to_machine_$1.out
#/tmp/time_add_to_machine_$1.out
