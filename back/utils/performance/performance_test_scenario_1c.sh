while [  1 -eq 1 ]; do
    echo "queuing player"    
    rm /tmp/time_add_to_queue_*
    rm /tmp/test_out_add_to_queue_*    
    seq 13 20 | xargs -n1 -Izzz ./utils/performance_test_add_to_queue.sh zzz 11;
    echo "queueing on 11 done"
    Sleep 6
    seq 13 20 | xargs -n1 -Izzz ./utils/performance_test_add_to_queue.sh zzz 12;    
    echo "queueing on 12 done"
    Sleep 6
done
