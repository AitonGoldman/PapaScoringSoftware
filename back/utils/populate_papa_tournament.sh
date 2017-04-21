curl -b /tmp/cookie -H "Content-Type: application/json" -X PUT -d "{\"ifpa_range_start\":\"$3\",\"division_id\":\"$2\"}" $POPULATE_URL:8000/$1/division/$2
