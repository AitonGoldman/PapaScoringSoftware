seq 1 20 | xargs -n1 -Izzz curl -b /tmp/cookie -H "Content-Type: application/json" -X POST -d "{\"division_machine_id\":\"1\",\"player_id\":\"zzz\"}" http://localhost:8000/elizabeth/queue
