SCORE=$2
if [ -z "$2" ]
  then
  SCORE=$RANDOM    
fi
echo $SCORE
export URL="http://0.0.0.0:8000/test/entry/division_machine/$1/score/$SCORE"
sleep .1
curl -X POST -b /tmp/cookie -s -o /tmp/test_out_record_score_$1.out -w "\npeekaboo - $1 - %{time_total}" -H "Content-Type: application/json" $URL > /tmp/time_record_score_$1.out 2>&1 &


#/tmp/test_out_add_to_machine_$1.out
#/tmp/time_add_to_machine_$1.out
