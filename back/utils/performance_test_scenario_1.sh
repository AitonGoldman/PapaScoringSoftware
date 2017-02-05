rm /tmp/token*
rm /tmp/out
while [  1 -eq 1 ]; do
    echo "Buying player tickets"
    PYTHONPATH=. python ./utils/performance_test.py 11 tokens_only    
    seq 1 10 | xargs -n1 -Izzz ./utils/performance_test_wrapper.sh zzz >> /tmp/out
    echo "Sleeping for 3 seconds"
    sleep 3
done
