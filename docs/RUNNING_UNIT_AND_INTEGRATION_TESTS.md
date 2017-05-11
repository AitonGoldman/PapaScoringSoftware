# Difference between unit and integration tests
In this project a unit test requires no seperate process running, and only tests the functionality of an individual method.  It uses mocks (and SQLAlchemy objects not connected to an actual database) when needed.

An integration test uses the Flask test client to test the REST endpoints (see http://flask.pocoo.org/docs/0.12/testing/ for more details), and will either test an individual endpoint or act as an end to end test.   

# Before running any tests
You must make sure the `back` directory is on your python path and you have used pyenv to activate the correct version of python (i.e. run `back/utils/ops/setup_runtime_environment.sh`).

All commands below assume you start at the root of the repo

# Running backend unit or integration tests

You can run individual unit test files with a command like the following : 

```
python -m unittest tests.unit.test_model_player
```

or you can run individual integration test files with a command like the following : 

```
python -m unittest tests.integration.test_route_token
```

note that the package `tests.unit.test_model_player` corresponds to the file `tests/unit/test_model_player.py`, and the package `tests.integration.test_route_token` corresponds to the file `tests/integration/test_route_token.py` 

If you want to run all the unit tests, use the following command : 

```
cd back
python -m unittest discover -s tests/unit
```

If you want to run all the integration tests (which will take a while), use the following command : 

```
cd back
python -m unittest discover -s tests/integration
```

# Writing your own integration tests

Look at existing `tests/integration/test_route_user.py`.  It has the following lines : 

```
class RouteUserTD(td_integration_test_base.TdIntegrationDispatchTestBase):
   def setUp(self):
      super(RouteUserTD,self).setUp()
      response,results = self.dispatch_request('/%s/util/healthcheck' % self.poop_db_name)                
      self.flask_app = self.app.instances[self.poop_db_name]
      orm_creation.create_stanard_roles_and_users(self.flask_app)
```

This represents the minimum you will need to write a integration test.  You need to inherit from `td_integration_test_base.TdIntegrationDispatchTestBase`.  

Don't worry about the following two lines...
```
response,results = self.dispatch_request('/%s/util/healthcheck' % self.poop_db_name)
self.flask_app = self.app.instances[self.poop_db_name]
``` 
...for now, just know that they basically are steps in the setup.  

Once you reach this point, a test database has been created for you.       

The line `orm_creation.create_stanard_roles_and_users(self.flask_app)` creates standard users in the test database.  

You can look at other integration tests to get an idea of how to insert other test data into the test database.  





