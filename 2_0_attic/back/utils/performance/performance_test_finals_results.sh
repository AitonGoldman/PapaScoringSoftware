export URL="http://0.0.0.0:8000/test/finals/scorekeeping/division_final/1"
sleep .1
curl -b /tmp/cookie -s -o /tmp/test_out_finals_results_$1.out -w "\npeekaboo - $1 - %{time_total}" -H "Content-Type: application/json" $URL > /tmp/time_finals_results_$1.out 2>&1 &
