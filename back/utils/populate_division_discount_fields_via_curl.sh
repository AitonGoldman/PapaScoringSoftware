POPULATE_URL=http://0.0.0.0
curl -b /tmp/cookie -H "Content-Type: application/json" -X PUT -d "{\"division_id\":\"1\",\"discount_ticket_count\":\"9\"}" $POPULATE_URL:8000/elizabeth/division/1
curl -b /tmp/cookie -H "Content-Type: application/json" -X PUT -d "{\"division_id\":\"2\",\"discount_ticket_count\":\"9\"}" $POPULATE_URL:8000/elizabeth/division/2
curl -b /tmp/cookie -H "Content-Type: application/json" -X PUT -d "{\"division_id\":\"3\",\"discount_ticket_count\":\"9\"}" $POPULATE_URL:8000/elizabeth/division/3
curl -b /tmp/cookie -H "Content-Type: application/json" -X PUT -d "{\"division_id\":\"3\",\"discount_ticket_count\":\"9\"}" $POPULATE_URL:8000/elizabeth/division/4
curl -b /tmp/cookie -H "Content-Type: application/json" -X PUT -d "{\"division_id\":\"5\",\"discount_ticket_count\":\"9\"}" $POPULATE_URL:8000/elizabeth/division/5
curl -b /tmp/cookie -H "Content-Type: application/json" -X PUT -d "{\"discount_ticket_count\":\"3\"}" $POPULATE_URL:8000/elizabeth/meta_division/1
