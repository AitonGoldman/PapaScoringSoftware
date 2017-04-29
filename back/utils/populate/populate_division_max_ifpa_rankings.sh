curl -b /tmp/cookie -H "Content-Type: application/json" -X PUT -d "{\"ifpa_range_start\":\"0\",\"division_id\":\"1\"}" $POPULATE_URL:8000/elizabeth/division/1
curl -b /tmp/cookie -H "Content-Type: application/json" -X PUT -d "{\"ifpa_range_start\":\"200\",\"division_id\":\"2\"}" $POPULATE_URL:8000/elizabeth/division/2
curl -b /tmp/cookie -H "Content-Type: application/json" -X PUT -d "{\"ifpa_range_start\":\"600\",\"division_id\":\"3\"}" $POPULATE_URL:8000/elizabeth/division/3
curl -b /tmp/cookie -H "Content-Type: application/json" -X PUT -d "{\"ifpa_range_start\":\"7500\",\"division_id\":\"4\"}" $POPULATE_URL:8000/elizabeth/division/4
