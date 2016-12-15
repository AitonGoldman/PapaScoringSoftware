import unittest
import os
from mock import MagicMock
import td_integration_test_base
import json
from routes import orm_creation
from util import db_util
import stripe

class RouteStripeTD(td_integration_test_base.TdIntegrationDispatchTestBase):
    def setUp(self):
        super(RouteStripeTD,self).setUp()
        response,results = self.dispatch_request('/%s/util/healthcheck' % self.poop_db_name)                
        self.flask_app = self.app.instances[self.poop_db_name]
        self.admin_user, self.scorekeeper_user,self.desk_user = orm_creation.create_stanard_roles_and_users(self.flask_app)

        db_util.load_machines_from_json(self.flask_app,True)
        #FIXME : This should be passed in from env variables?
        orm_creation.init_papa_tournaments_divisions(self.flask_app,use_stripe=True,stripe_sku=["sku_8bY4j0VdBxGmPu",
                                                                                                "sku_8zGvY92kgyMlx1",
                                                                                                "sku_8cVf2tetzJ4f8D",
                                                                                                "sku_8beHMnaBSdH4NA",
                                                                                                "sku_8beJOPdNmnoQgw",
                                                                                                "sku_8beFqmlhh0y6Wa",
                                                                                                "sku_8bU4ZwvW1UMtxy",
                                                                                                "sku_9jugzXV5S8oafx",
                                                                                                "sku_9juhywxXYAFfW7"])
        self.player = orm_creation.create_player(self.flask_app,{'first_name':'test','last_name':'player','ifpa_ranking':'123','linked_division_id':'1'})
        self.player_pin = self.player.pin
        self.player_two = orm_creation.create_player(self.flask_app,{'first_name':'test_two','last_name':'player_two','ifpa_ranking':'321','linked_division_id':'1'})        
        orm_creation.create_team(self.flask_app,{'team_name':'test_team','players':['1','2']})
    @unittest.skipIf(os.getenv('STRIPE_API_KEY',None) is None,
                     "SKIPPING BECAUSE NO TEST_STRIPE_SKU SET")
    def test_add_token(self):        
        with self.flask_app.test_client() as c:                    
            rv = c.put('/auth/player_login',
                       data=json.dumps({'player_pin':self.player_pin}))
            rv = c.post('/token/paid_for/0',
                       data=json.dumps({"player_id":1,
                                        "team_id":1,
                                        "divisions":{1:1},
                                        "teams":{5:1},
                                        "metadivisions":{1:1}}))
            self.assertEquals(rv.status_code,
                              200,
                              'Was expecting status code 200, but it was %s : %s' % (rv.status_code,rv.data))
            tokens = json.loads(rv.data)['data']                        
            #for type_of_token in ["divisions","metadivisions","teams"]
            self.assertEquals(tokens['divisions']['1'],1)
            self.assertEquals(tokens['metadivisions']['1'],1)
            self.assertEquals(tokens['divisions']['5'],1)
            new_division_tokens_count = len(self.flask_app.tables.Token.query.filter_by(division_id=1,paid_for=False).all())
            new_teams_tokens_count = len(self.flask_app.tables.Token.query.filter_by(division_id=5,paid_for=False).all())            
            new_metadivision_tokens_count = len(self.flask_app.tables.Token.query.filter_by(metadivision_id=1,paid_for=False).all())
            self.assertEquals(new_division_tokens_count,1)
            self.assertEquals(new_teams_tokens_count,1)
            self.assertEquals(new_metadivision_tokens_count,1)
            actual_tokens = tokens['tokens']
            stripe.api_key = os.getenv('STRIPE_API_KEY')

            stripe_token = stripe.Token.create(
                card={
                    "number": '4242424242424242',
                    "exp_month": 12,
                    "exp_year": 2017,
                    "cvc": '123'
                },
)
            rv = c.post('/stripe',
                       data=json.dumps({
                           'addedTokens':{"player_id":1,
                                          "team_id":1,
                                          "divisions":{1:1},
                                          "teams":{5:1},
                                          "metadivisions":{1:1}
                           },
                           'stripeToken':stripe_token.id,
                           'tokens':actual_tokens,
                           'email':'test@test.com'
                       }))
            stripe_result = json.loads(rv.data)['data']                        
            self.assertEquals(stripe_result,"success")
            new_division_tokens_count = len(self.flask_app.tables.Token.query.filter_by(division_id=1,paid_for=True).all())
            new_teams_tokens_count = len(self.flask_app.tables.Token.query.filter_by(division_id=5,paid_for=True).all())            
            new_metadivision_tokens_count = len(self.flask_app.tables.Token.query.filter_by(metadivision_id=1,paid_for=True).all())
            self.assertEquals(new_division_tokens_count,1)
            self.assertEquals(new_teams_tokens_count,1)
            self.assertEquals(new_metadivision_tokens_count,1)
            
