export URL="http://0.0.0.0:8000/elizabeth/queue"
sleep .1
curl -X POST -b /tmp/cookie -s -o /tmp/test_out_add_to_queue_$1.out -w "\npeekaboo - $1 - %{time_total}" -H "Content-Type: application/json" -d "{\"player_id\":\"$1\",\"division_machine_id\":\"$2\"}" $URL > /tmp/time_add_to_queue_$1.out 2>&1 &

#/tmp/test_out_add_to_machine_$1.out
#/tmp/time_add_to_machine_$1.out
