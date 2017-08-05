ARRAY=(324 324 323 323 322 322 321 321 320 320 319 319 318 318 317 317 316 316 315 315 314 314 313 313 313 313 312 312 311 311 310 310 309 309)
#        1   1   3   3   5   5   7   7   9   9  11  11  13  13  15  15  17  17  19  19  21  21  23  23  23  23  27  27  29  29  30  30  32  32
echo "buying tickets"    
rm /tmp/time_add_to_machine*;
rm /tmp/time_record*;
rm /tmp/test_out_record*
rm /tmp/test_out_add_to_machine*
end_player_num=$((100 + $1))
seq 100 $end_player_num | xargs -n1 -Izzz ./utils/performance/performance_test_add_token_desk.sh zzz;
COUNTER=0
for i in $(seq 100 $end_player_num)
do    
    for j in {1..2}
    do
        echo "Adding player $i to machine $j"
        ./utils/performance/performance_test_add_to_machine.sh $j $i;
        sleep .2
        ./utils/performance/performance_test_record_score.sh $j ${ARRAY[$COUNTER]};
        echo "Recorded score!"
        sleep .2
    done
    COUNTER=$(($COUNTER + 1))
done

