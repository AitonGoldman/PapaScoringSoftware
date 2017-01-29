curl -c /tmp/cookie -H "Content-Type: application/json" -X PUT -d "{\"username\":\"test_admin\",\"password\":\"test_admin\"}" $POPULATE_URL:8000/test/auth/login
