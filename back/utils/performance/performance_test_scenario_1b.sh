while [  1 -eq 1 ]; do
    echo "getting player results"    
    rm /tmp/time_player_results*    
    seq 1 10 | xargs -n1 -Izzz ./utils/performance_test_player_results.sh zzz;        
    echo "sleeping for 3"
    sleep 3    
done
