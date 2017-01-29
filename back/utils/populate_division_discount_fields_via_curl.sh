curl -b /tmp/cookie -H "Content-Type: application/json" -X PUT -d "{\"division_id\":\"1\",\"discount_ticket_count\":\"3\"}" http://localhost:8000/elizabeth/division/1
curl -b /tmp/cookie -H "Content-Type: application/json" -X PUT -d "{\"division_id\":\"1\",\"discount_ticket_count\":\"3\"}" http://localhost:8000/elizabeth/division/2
curl -b /tmp/cookie -H "Content-Type: application/json" -X PUT -d "{\"division_id\":\"1\",\"discount_ticket_count\":\"3\"}" http://localhost:8000/elizabeth/division/3
curl -b /tmp/cookie -H "Content-Type: application/json" -X PUT -d "{\"division_id\":\"1\",\"discount_ticket_count\":\"3\"}" http://localhost:8000/elizabeth/division/5
curl -b /tmp/cookie -H "Content-Type: application/json" -X PUT -d "{\"discount_ticket_count\":\"3\"}" http://localhost:8000/elizabeth/meta_division/1
