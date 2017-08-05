seq 1 8 | xargs -n1 -Izzz curl -b /tmp/cookie -H "Content-Type: application/json" -X PUT -d "{\"division_id\":\"zzz\",\"number_of_relevant_scores\":\"6\"}" $POPULATE_URL:8000/elizabeth/division/zzz
