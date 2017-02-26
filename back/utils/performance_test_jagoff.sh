export URL="http://0.0.0.0:8000/elizabeth/entry/division_machine/$1/jagoff"
sleep .1
curl -X PUT -b /tmp/cookie -s -o /tmp/test_out_jagoff_$1.out -w "\npeekaboo - $1 - %{time_total}" -H "Content-Type: application/json" $URL > /tmp/time_jagoff_$1.out 2>&1 &
