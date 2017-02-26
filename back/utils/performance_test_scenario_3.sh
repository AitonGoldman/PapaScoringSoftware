while [  1 -eq 1 ]; do
    echo "buying tickets"    
    rm /tmp/time_*    
    rm /tmp/test_out_*    
    seq 1 10 | xargs -n1 -Izzz ./utils/performance_test_add_token_desk.sh zzz;
    for i in {1..10}
    do
        for j in {1..10}
        do
            echo "Adding player $i to machine $j"
            ./utils/performance_test_add_to_machine.sh $j $i;
            sleep 60
            ./utils/performance_test_record_score.sh $j;
            echo "Recorded score!"            
            sleep 1
            ./utils/performance_test_add_to_machine.sh $j $i;
            sleep 120            
            ./utils/performance_test_void.sh $j;
            echo "Voided score!"            
            sleep 1
            ./utils/performance_test_add_to_machine.sh $j $i;
            sleep 180                        
            ./utils/performance_test_jagoff.sh $j;
            echo "Jagoff!"            
            sleep 1
        done
    done
done
