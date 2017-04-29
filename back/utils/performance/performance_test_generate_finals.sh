export URL="http://0.0.0.0:8000/elizabeth/finals/division/1"
sleep .1
curl -X POST -b /tmp/cookie -s -o /tmp/test_out_generate_finals_$1.out -w "\npeekaboo - $1 - %{time_total}" -H "Content-Type: application/json" -d "[[\"1\",\"1\"],[\"2\",\"2\"],[\"3\",\"3\"],[\"4\",\"4\"],[\"5\",\"5\"],[\"6\",\"6\"],[\"7\",\"7\"],[\"8\",\"8\"],[\"9\",\"9\"],[\"10\",\"10\"],[\"11\",\"11\"],[\"12\",\"12\"],[\"13\",\"13\"],[\"14\",\"14\"],[\"15\",\"15\"],[\"16\",\"16\"],[\"17\",\"17\"],[\"18\",\"18\"],[\"19\",\"19\"],[\"20\",\"20\"],[\"21\",\"21\"],[\"22\",\"22\"],[\"23\",\"23\"],[\"24\",\"24\"]]" $URL > /tmp/time_generate_finals_$1.out 2>&1 &

#/tmp/test_out_add_to_machine_$1.out
#/tmp/time_add_to_machine_$1.out
