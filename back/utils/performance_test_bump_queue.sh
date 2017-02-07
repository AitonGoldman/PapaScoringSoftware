export URL="http://0.0.0.0:8000/elizabeth/queue/division_machine/$1/bump"
sleep .1
curl -X PUT -b /tmp/cookie -s -o /tmp/test_out_bump_queue_$1.out -w "\npeekaboo - $1 - %{time_total}" -H "Content-Type: application/json" $URL > /tmp/time_bump_queue_$1.out 2>&1 &

#/tmp/test_out_add_to_machine_$1.out
#/tmp/time_add_to_machine_$1.out
