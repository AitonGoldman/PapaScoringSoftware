export URL="http://0.0.0.0:8000/test/token/paid_for/1"
sleep .1
curl -X POST -b /tmp/cookie -s -o /tmp/test_out_add_token_desk_$1.out -w "\npeekaboo - $1 - %{time_total}" -H "Content-Type: application/json" -d "{\"player_id\":\"$1\",\"divisions\":{\"1\":[\"25\",\"0\"],\"2\":[\"25\",\"0\"]},\"teams\":{\"5\":[\"0\",\"0\"]},\"metadivisions\":{\"1\":[\"0\",\"0\"]}}" $URL > /tmp/time_add_token_desk_$1.out 2>&1 &

#/tmp/test_out_add_to_machine_$1.out
#/tmp/time_add_to_machine_$1.out
