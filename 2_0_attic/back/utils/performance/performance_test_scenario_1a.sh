while [  1 -eq 1 ]; do
    echo "adding players to machines"    
    rm /tmp/time_add_to_machine*;
    rm /tmp/time_record*;
    rm /tmp/test_out_record*
    rm /tmp/test_out_add_to_machine*    
    seq 1 5 | xargs -n1 -Izzz ./utils/performance_test_add_to_machine.sh zzz;
    seq 1 5 | xargs -n1 -Izzz ./utils/performance_test_record_score.sh zzz;
    echo "sleeping for 4"
    sleep 4
done
