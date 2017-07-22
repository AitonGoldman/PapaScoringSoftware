import requests
import json
import datetime
import time
import random
import sys

headers = {'Content-Type': 'application/json'}

r_login = requests.put("http://localhost:8000/elizabeth/auth/player_login",data=json.dumps({"player_pin":"7780","player_id":"1"}),headers=headers)

r2_login = requests.put("http://localhost:8001/elizabeth/auth/player_login",data=json.dumps({"player_pin":"7780","player_id":"1"}),headers=headers)

if len(sys.argv) > 2 and sys.argv[2] == "tokens_only":
    r_test_stripe = requests.post("http://localhost:8000/elizabeth/stripe/test_player_purchase/%s"%sys.argv[1],
                                  cookies=r_login.cookies)
    print "quitting without creating tickets"
    sys.exit()
f = open('/tmp/tokens_%s.json' % sys.argv[1])
token = json.loads(f.read())['stripe_token']
token_count = {"divisions":{"1":[5,10]},
               "metadivisions":{"1":[5,10]},
               "teams":{"5":[5,0]},
               "player_id":sys.argv[1]}
a = datetime.datetime.now()
r_add_tokens = requests.post("http://localhost:8000/elizabeth/token/paid_for/0",
                             data=json.dumps(token_count),
                             cookies=r_login.cookies)
b = datetime.datetime.now()
c = b - a
print "%s - %s - %s - add_tokens" % (sys.argv[1], r_add_tokens.status_code, c.total_seconds())
r_add_tokens_result = json.loads(r_add_tokens.text)['data']
a = datetime.datetime.now()
r_test_stripe = requests.post("http://localhost:8001/elizabeth/stripe",
                              data=json.dumps({"addedTokens":token_count,
                                               "tokens":r_add_tokens_result['tokens'],
                                               "email":"blahblah@blah.com",
                                               "stripeToken":token}),
                              cookies=r2_login.cookies)
b = datetime.datetime.now()
c = b - a
print "%s - %s - %s - stripe_tokens" % (sys.argv[1], r_test_stripe.status_code ,c.total_seconds())


