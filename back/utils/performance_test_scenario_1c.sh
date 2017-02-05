while [  1 -eq 1 ]; do
    echo "queuing player"    
    rm /tmp/time_add_to_queue_*
    rm /tmp/test_out_add_to_queue_*    
    seq 12 15 | xargs -n1 -Izzz ./utils/performance_test_add_to_queue.sh zzz 11;
    seq 12 15 | xargs -n1 -Izzz ./utils/performance_test_add_to_queue.sh zzz 12;    
    Sleep 3
done
