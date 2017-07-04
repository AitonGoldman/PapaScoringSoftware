while [  1 -eq 1 ]; do
    echo "buying tickets"    
    rm /tmp/time_add_to_machine*;
    rm /tmp/time_record*;
    rm /tmp/test_out_record*
    rm /tmp/test_out_add_to_machine*    
    seq 100 300 | xargs -n1 -Izzz ./utils/performance/performance_test_add_token_desk.sh zzz;
    for i in {100..300}
    do
        for j in {1..4}
        do
            echo "Adding player $i to machine $j"
            ./utils/performance/performance_test_add_to_machine.sh $j $i;
            sleep .2
            ./utils/performance/performance_test_record_score.sh $j;
            echo "Recorded score!"
            sleep .2
        done
    done
done
