# How to help with TD development
Read through all the quickstarts/tutorials listed below ( you can read the optional ones if you want, but they are not neccessary to get started ).  Once you have read the quickstarts/tutorials, you can read the use case.  This will highlight all the things you need to do (on the backend and frontend) when you want to add a new feature/fix a bug/refactor code, and will give some overview of all the individual components of TD.  At that point, you can jump in and start submiting pull requests!


Do not hesitate to ask questions - this will become a reference to our slack instance once we have one.


# Overview of TD
TD is made up of two parts : the backend and the frontend.  The backend is a [Flask](http://flask.pocoo.org/) application that offers a REST api and interfaces with databases using [SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.1/).  The frontend is an [Ionic](http://ionicframework.com/) application.


# Prerequisite Quickstarts/Turotials 
The following list might look daunting, but it should only take a you a single weekend to make it through most of them.  When you are done, you should have a good grasp on all the frameworks/librarys that TD uses.


## Git 
* Git is AWESOME - but the learning curve can be a steeper than other source control systems - the good news you can get started with it without having to wrap your brain around the complex stuff :
  * https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control ( this is the begining of the introduction chapter )
  * https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository ( this is the begining of the Basics chapter)


## Frameworks/Libraries used by the backend
* Flask : A python framework we use for building the REST API : http://flask.pocoo.org/docs/0.11/quickstart/
* SQLAlchemy : A python ORM library that lets TD talk to any supported database : http://docs.sqlalchemy.org/en/latest/orm/tutorial.html
* Flask-SQLAlchemy : An extension for Flask that adds support for SQLAlchemy to TD : http://flask-sqlalchemy.pocoo.org/2.1/quickstart/
* Optional Reading : You do not need to have read the following docs tp contribute, but if you want to get deeper into TD development then you should know about these Flask extensions that TD uses
  * Flask-Principal : Allows us to define different roles, and use those roles to control who can do what with TD : http://pythonhosted.org/Flask-Principal/
  * Flask-Login : Provides user session management for Flask : https://flask-login.readthedocs.io/en/latest/
  * Stripe : Credit Card payment processing service : https://stripe.com/docs/api


## Frameworks/Libraries used by the backend
* AngularJs 1.x : Javascript framework that the frontend uses
  * https://docs.angularjs.org/tutorial 
  * https://docs.angularjs.org/guide
* angular-ui-router : An AngularJs extension that allows us to do client-side Single Page Application routing : https://github.com/angular-ui/ui-router/wiki (read the "In depth guide" links)
* Ionic : A framework built ontop of AngularJS that provides UI elements and allows us to package the AngularJS code into native mobile apps : http://ionicframework.com/docs/guide/


# Use Case : Adding a player
In the course of running our tournament, we'd like to be able to add players to the system.  In this use case, we will walk though all the steps that are required to do this.  In the course of walking through the steps, general explanations will be given of the code that the changes touch.


## Step 0 : Checkout the Tutorial branch
Before you do anything, make sure you have checked out the Tutorial branch.  All the following steps assume you have checked out the Tutorial branch.  This branch is has all the core TD code, but only has a minimal number of REST endpoints and SQLAlchmey models defined.  It's main purpose is to provide a starting point for new people to dive into the code. 


## Step 1 : Add a SQLAlchemy model
The first step is to define the database tables which will store information about players.  We do this using SQLAlchemy - specifically, we define a SQLAlchemy model.  All SQLAlchemy models are kept in `back/td_types/`.  We'll need to create the file `back/td_types/Player.py` add the following SQLAlchemy model for the player db table :


```
from flask_restless.helpers import to_dict

def generate_player_class(db_handle):
    class Player(db_handle.Model):
        player_id = db_handle.Column(db_handle.Integer,primary_key=True)
        first_name = db_handle.Column(db_handle.String(1000))
        last_name = db_handle.Column(db_handle.String(1000))
    return Player

```


This should look familiar to you if you have read the SQLAlchemy and Flask-SQLAlchemy quickstarts - we are defining a Class called `Player` which represents the db table which will contain information about our players.  That information is the first name, last name, and a player id.  Note that the player id is defined as the primary_key, which means it will auto-increment by default.


But what is the deal with the `generate_player_class()` function?  And why is the class definition wrapped inside this function?  To answer this question, we first need to understand one of the design requirements for TD 


* It should be able to handle seperate events (i.e. keep the data from PAPA 20 seperate from the PAPA 19 data)


To satisfy the first requirement, TD stores each event in a seperate database.  Unfortunately, Flask-SQLAlchemy won't let you point to more than one database (i.e. it won't let you say "point to a different database based on the incoming request").  So each event has it's own Flask application - when the application starts up, it needs it's SQLAlchemy models pointed to the correct database.  So when each app starts up it gets a connection to the correct database, and then calls the `generate_player_class()` and passes in a SQLAlchemy database connection handle.  `generate_player_class()` returns the generated class. 


So how does the application call `generate_player_class()`?  If we look in `back/td_types/__init__.py`, we find the following : 


```
from User import generate_user_class

class ImportedTables():
    def __init__(self,db_handle):
        self.User = generate_user_class(db_handle)                
        self.db_handle = db_handle

```


When the ImportedTables class is instantiated, it calls the generate() function for all the SQLAlchemy models (with the SQLAlchemy db handle that is passed in) and stores the resulting classes.  As a conveinience, it also stores the SQLAlchemy db handle.  Let's add our Player class generator...


```
from User import generate_user_class
from Player import generate_player_class
class ImportedTables():
    def __init__(self,db_handle):
        self.Player = generate_player_class(db_handle)
        self.User = generate_user_class(db_handle)                
        self.db_handle = db_handle

```


So what code instatiates ImportedTables()?  A full explanation of this is beyond the scope of this document - if you are interested in the full explanation, please look at `back/util/dispatch.py`.  The short answer is this : we have some fancy code (in `back/util/dispatch.py`) that routes a request to the appropriate flask applciation, and handles instatiating the flask application if has not yet been instantiated.  This fancy code also handles instatiating the ImportedTables correctly and associating it with the appropriate flask application instance.  Note that this fancy code will also take care of creating the database and tables if they have not already been created. 


## Step 2 : Add REST endpoints
Now that we have defined our table, we need to give users a way to access and change that data.  We do this by defining REST endpoints, which are just urls that TD will respond to.  For example, let's say our service will be running at the following url : http://localhost:8000/, then the REST endpoint to get all existing users will be http://localhost:8000/user (definied in `back/routes/user.py`).  When we hit this url/endpoint with a browser, a list of all existing users will be returned in JSON format.  Note that all REST endpoints in TD MUST return json.


We want to define two endpoints to let people interact with the Player db table - an endpoint to add players, and an endpoint to retrieve player info.  Let's start with the "add players" endpoint.


### Add Player Endpoint


All REST endpoints are defined in `back/routes`.  Let's create the file `back/routes/player.py` and add the following to it : 


```
from blueprints import admin_manage_blueprint
from flask import jsonify,current_app,request
import json
from werkzeug.exceptions import BadRequest,Conflict
from util import db_util
from util.permissions import Admin_permission, Desk_permission
from flask_login import login_required,current_user
from flask_restless.helpers import to_dict

@admin_manage_blueprint.route('/player',methods=['POST'])
@login_required
@Desk_permission.require(403)
def route_add_player():
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    input_data = json.loads(request.data)
    for key in ['first_name','last_name']:
        if key not in input_data:
            raise BadRequest("You did not specify a first name and/or a last name")        
    player = tables.Player.query.filter_by(first_name=input_data['first_name'],last_name=input_data['last_name']).first()
    if player is not None:
        raise Conflict('Duplicate player')

    new_player = tables.Player(
        first_name=input_data['first_name'],
        last_name=input_data['last_name']        
    )
    db.session.add(new_player)
    db.session.commit()                        
    return jsonify({'data':to_dict(new_player)})

```


Let's look at this line by line, and start at `@admin_manage_blueprint.route('/player',methods=['POST'])`.  This line is defining the endpoint and the HTTP method for the endpoint - in this case, the endpoint is `/player` and the method is `POST`.  Note that if I were to hit the `/player` url with a HTTP GET, this endpoint would not respond.  We'll be defining a GET endpoint later on.  



Note that this looks a little different than what you saw in the Flask quickstart - this is because TD uses Flask blueprints.  Explaining blueprints is outside the scope of this document (although if you want to know more, look here : http://flask.pocoo.org/docs/0.10/blueprints/).  All you need to know is that if you want to define a endpoint in TD, you need to use the `@admin_manage_blueprint.route()` decorator.  The function that is wrapped by this decorator will define what the endpoint does.


Let's look at the next two lines : `@login_required` and `@Desk_permission.require(403)`.  These control who can access this endpoint - the first line checks that whatever is trying to access this endpoint is logged in to TD, and the second line checks that the logged in user has permission to access this endpoint.  It's not important at this point to understand how these work - you just need to know that a `@login_required` decorator will make sure only logged in users can use this endpoint, and `@Desk_permission.require(403)` will make sure that only users with the `desk` permission can use this endpoint.  If you want to see the other permissions you can control on, see `back/util/permissions.py`.  You'll notice that there is no way in this branch to set user permissions through the UI.  This is implemented in the main branch, but for this branch there is a util which will allow you to bootstrap the database with an admin user with all permissions.  


Now lets start looking at the actual function that will define what the enddpoint does : 


```
def route_add_player():
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    input_data = json.loads(request.data)
```


First note the use of `current_app` in these 3 lines - `current_app` is provided by flask and represents the current flask application.  Whenever we need to get access to our flask application instance, we need `current_app` due to the multiple flask application setup we discussed in Step 1.  We pass `current_app` into `db_util.app_db_handle` to get back the SQLAlchemy db handle (which we will need later to commit changes to the db).  We also pass `current_app` into `db_util.app_db_tables` to get the `ImportedTables` instance for this flask application instance (which we talked about in Step 1, and which we will need for querying the database).  


On the third line, we parse out the player information for the new player we are trying to create.  Note that TD assumes that all POSTs will contain JSON encoded objects.  We use the `request` object (which is provided by flask, and represent the HTTP request that was recieved) - specifically, we pass the `request.data` attribute (which contains the body of the HTTP request) to `json.loads()`, and get back a python dict with the contents of json object that was in the request body.


```
    for key in ['first_name','last_name']:
        if key not in input_data:
            raise BadRequest("You did not specify a first name and/or a last name")        

```


This is an example of how to properly handle problems in your endpoints - by throwing one of the exceptions defined here : http://werkzeug.pocoo.org/docs/0.11/exceptions/.  These exceptions correspond to HTTP codes (i.e. 400, 401, 403, etc) - when these exceptions are raised they will be caught by the flask application, and flask will send a proper http response for you.  In this case, information we must have to proceed (i.e. players first AND last name) is not present, so we raise a BadRequest exception, and add information about what went wrong.


Going on to the next few lines : 


```
    player = tables.Player.query.filter_by(first_name=input_data['first_name'],last_name=input_data['last_name']).first()
    if player is not None:
        raise Conflict('Duplicate player')

```


Here we are using the ImportedTables() (which the variable `tables` points to) which we got earlier.  In this case, we are running a query which looks for an existing player with the same first name andd last name as the player we are trying to create.  This query should look familiar if you read the SQLAlchemy and Flask-SQLAlchemy quickstarts/tutorials.  If the result is not None, it means a player with that name already exists, so we throw a `Conflict` exception.


Finally, we want to actually create a new player and commit that info to the db.  We do that with these lines :


```
    new_player = tables.Player(
        first_name=input_data['first_name'],
        last_name=input_data['last_name']        
    )
    db.session.add(new_player)
    db.session.commit()                        
    return jsonify({'data':to_dict(new_player)})

```


Once again, we use `tables` to create the Player object, and we use the values we got from the HTTP body to set the first and last name.  We use the `db` variable to actually add it to the database and then commit the changes.  Finally, we create a python dict of the `new_player` object, and then we return a jsonified version of the dict.  Note that TD assumes all endpoints will return json (even if it's an empty JSON object)


You can now add players to the database through the REST API.  But it would be nice if we could use the REST api to actually SEE the players we have added.


### Get Player Endpoint


We're going to add the following to `back/routes/player.py` : 


```
@admin_manage_blueprint.route('/player/<player_id>',methods=['GET'])
def route_get_player(player_id):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    player = tables.Player.query.filter_by(player_id=player_id).first()
    if player is None:
        raise BadRequest('No such player exists')
    return jsonify({'data':to_dict(player)})
```


This should all now be looking familiar.  We specify a player_id (which was generated by the database when the player was adde to the db) in the url, and this endpoint will lookup the appropriate player and return a JSON object with the player info.  Note the `<player_id>` part of the endpoint definition - this tells flask that it should expect something in that part of the url, and that it should pass the wrapped function that value.  If you look at the `route_get_player()` function, you see that it's expecting a single argument - this will contain the value that flask found in the <player_id> part of the url.


Finally, we need to tell TD about this new file with the new endpoints - we add the following to `back/routes/__init__.py`


```
import player
```


## Step 3 : Trying out the new endpoint
Let's take this baby out for a spin!  Before we actually start things up, we need to change the followings line in `back/routes.player.py` 


```
@admin_manage_blueprint.route('/player',methods=['POST'])
@login_required
@Desk_permission.require(403)
def route_add_player():
```


to


```
@admin_manage_blueprint.route('/player',methods=['POST'])
#@login_required
#@Desk_permission.require(403)
def route_add_player():
```


This is because we want to make demonstrating the two endpoints as easy as possible - commenting these lines out means we don't have to login to use these endpoints


Now, follow the quickstart steps in the README.md to try this out (i.e. only the "Starting up backend" steps).  Once you have started up the docker container, try the following command in a terminal on your computer (this will hit the Add User endpoint and create a user named "mister sister") 


```
curl -H "Content-Type: application/json" -X POST -d '{"first_name":"mister","last_name":"sister"}' http://localhost:8000/test/player
```


and you will get the following back


```
{'data':{'first_name':'mister','last_name':'sister','player_id':1}}
```


Next, run the following command (which will request the player info for the player with player_id 1)


```
curl http://localhost:8000/test/player
```


And you will get the following output


```
{'data':{'first_name':'mister','last_name':'sister','player_id':1}}
```


You might have noticed the url has "test" in it before the "/player".  Why is that "test" there?  As we discussed in Step 1, we need to be able to have seperate flask app instances for seperate events(i.e. PAPA20 vs PAPA19).  You'll also remember we discussed the fancy code that handles routing requests to the appropriate app.  Well, the way that fancy code does the routing is it looks at the first part of the url after the host name.  It uses that to decide which flask app instance to route to, and then it removes that part of the url before passing the request onto the flask app instance.  The docker container you spun up bootstraps a flask app instance that handles all request for the "test" event.  So in the case of the url http://localhost:8000/test/player, the fancy code found "test", removed test from the url (so it was now "http://localhost:8000/player") and routed the request to the appropriate flask app instance.  As far as the flask app instance is concerned, it just got a request for the GET "/player" endpoint.


If you have a decent grasp on what was just covered, you should be able to look at any of the enpoints on the main branch and understand what is going on.  If weird stuff neeed to happen in the endpoint, it will be well documented.


## Step 4 : Implement "Add Player" in Fronted 
We need to do several things in order to implement an "Add Player" page in the frontend :
* Create the "Add Player" page and controller - this will be responsible for collecting the player information
* Tell the frontend how to reach the appropriate backend endpoints
* Create the "Process Add Player" page and controller - this will be responsible for submitting the info to the backend
* Create links to the "Add Player" page


### Create the "Add Player" page and controller
There is a utility that takes care of a lot of this step.  Run the following commands (assuming you start in the top level dir of your checked out repo): 


```
cd front
util/add_new_controller.pl --name app.add_player --path `pwd`/www/js 
```


What did this script do?  It did the following things : 
* Created the directory add_player under `front/www/js/app`
* Created a angular module (called `app.add_player`) in the file `front/www/js/app/add_player/add_player.js`
* Inside the file `front/www/js/app/add_player/add_player.js` is a angular controller called `app.add_player`
* In the directory `front/www/js/app/add_player/` a file called `add_player.html` (which is mostly empty)


The script does other things that we aren't going to discuss here, but if you are interested in a more in-depth discussion about what is going here there is a section at the bottom for more advanced topics.  The short story is : all the generated files are being included automatically, and angular-ui-router routes have been added for the controller and page we have generated with the same name as the module/controller we created.


### Fill in the generated add_player.html page
This page will have the form inputs to collect the player info.  We'll add the following to the page inside the `<ion-content>` tag:


```
    <div class="skinny-list list">
      <div class="item-divider item" id='add_user_user_info_title'>
        Player Info
      </div>
      <label  class="item-input item">
        <span>First Name : </span>
        <input ng-model='player_info.first_name' type="text" placeholder="First Name">
      </label>
      <label  class="item-input item">
        <span>First Name : </span>
        <input ng-model='player_info.last_name' type="text" placeholder="Last Name">
      </label>
      <button id='add_user_add_button' ui-sref='.process({process_step:{process:true}, player_info:player_info})' class="item item-icon-right button button-full button-calm input-list-button" style='text-align:left' ng-disabled='utils.var_empty(player_info.first_name) && utils.var_empty(player_info.last_name)'>
        <i class="icon ion-chevron-right"></i>
        <span >Apply Changes</span>
      </button>
    </div>
```


We're making heavy use of the Ionic UI components here - please refer to the ionic documentation for more information on the css components and associated javascript.  Here are the things to pay attention to from above :
* the ui-sref for the <button> points to the `app.add_player.process` angular-ui-router route (which we have not created yet), and has two arguments that get passed on - `process_step` and `player_info` - player_info is set to the `player_info` scope object (which contains the player first_name and last_name) - we'll explain in a bit what `process_step` is for 
* utils.var_empty() is a helper function which checks if a variable is empty (i.e. undefined or just empty) - we'll see where this comes from in the next step.


### Fill in the controller in add_player.js 
The `add_player.js` will not be doing much.  This is what `add_player.js` should look like :


```
angular.module('app.player.add_player',[/*REPLACEMECHILD*/]);
angular.module('app.player.add_player').controller(
    'app.player.add_player',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;

        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
             
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
```


Here is what to pay attention to in this generated controller:
* we inject the following angular services into the controller : `TimeoutResources`,`Utils`,`Modals`.  These are TD services that are defined in `front/www/js/services`.  As we go through this use case, we'll talk more about what each of these does.
* $scope.controller_bootstrap() is a bootstraping function that takes care of a number of things that are needed by the controller - it's defined in `front/www/js/app/app.js`.  `front/www/js/app/app.js` contains the top level angular module, which is used for the ng-app tag in index.html 


We only have to make a small change to this controller - let's make the following change :


```
$scope.utils = Utils;
//Modals.loading()
```


What we did was add the line `$scope.utils = Utils;` - What does `Utils` do?  It's a angular service that is defined in `front/www/js/services/utils.js` - and like the name implies, it contains utility and convienience functions that do not fit into any of other services.  By assigning `Utils` to `$scope.utils`, it makes it possible for the `add_player.html` to use the functions in the `Utils` service.


### Tell the frontend how to reach the appropriate backend endpoints
In the previous section, we saw the TimeoutResources service being injected into the `app.add_player` controller.  The TimeoutResources service is responsible for provide functions that allow the TD frontend to make http calls against the backend.  In the step, we are going to add some code to the `TimeoutResources` service so that the TD frontend can access the two backend REST endpoints we defined earlier.  This is the first peice of code we are going to add :


```
var addPlayerResource = generate_resource_definition(':site/player', 'POST'); //add a player
var getPlayerResource = generate_resource_definition(':site/player/:player_id','GET'); //get player info                                    
```


So what does `generate_resource_definition()` do?  The simple answer is that it generates an angular resource ( see here for a larger explanation : https://docs.angularjs.org/api/ngResource/service/$resource).  If you don't feel like reading through that link, the simple explanation of angular resources are they make it easier to call a REST API and parse the results.  The only part you need to know about them is that you can specify parts of the url to be replaced with variables when the REST API call is made.  If you look at the first argument to `generate_resource_definition`, you'll see this being demonstrated - the first argument is the url for the REST endpoint, and the `:site` and `:player_id` strings tell the resource to expect variables called `site` and `player_id`.  The second argument to `generate_resource_definition` is the http method.  


But what is the deal with that ':site' part of the REST endpoint we are passing into `generate_resource_definition()` - remember that on the backend side, we needed to put 'test' into the url when testing the endpoint?  This is the same thing - on the frontend side, we call the that information the "site".  


Once we have generated an angular resource, how do we use them?  This leads to our next peice of code (which will be added inside the existing `return` block):


```
return {
.
.
.
GetPlayer: generate_custom_http_executor(getPlayerResource,'player','get'),
AddPlayer: generate_custom_http_executor(addPlayerResource,'added_player','post'),
.
.
}
```


So what does `generate_custom_http_executor()` do?  It generates a function - when that function is called, it makes the REST api call defined by the angular resource we passed in to `generate_custom_http_executor()` and then stores the results of the REST api call.  For example, `GetPlayer()` will hit the REST endpoint we definied on the backend to get player info and then store the results.  How do we get those results?  We call TimeoutResources.GetAllResources(), which returns an object with all the resources that have been retrieved - the second argument to `generate_custom_http_executor()` defines which key the results get stored in.  For example, in the first line of code above, the second argument is 'player' - after calling `TimeoutResources.GetPlayer()`, you would use something like `resources = TimeoutResources.GetAllResources()`  and then to access the player info, you would use `resources.player`.  


The third argument to `generate_custom_http_executor()` is one of two strings : 'get' or 'post'.  This tells the generator whether or not the genrated function should expect arguments that represent the POST/PUT body.


In the next step, we'll see the `GetPlayer()` and `AdddPlayer()` in action.


### Create the "Process Add Player" page and controller
Let's use that utility again to generate the "Process Add Player page and controller"


```
cd front
util/add_new_controller.pl --name app.add_player.process --path `pwd`/www/js --post_param player_info
```


Note the new argument to the utility - `--post_param player_info` - what does that do?  It tells the utility that the module and controller should expect a parameter to be passed in named `player_info` (via the angular-ui-router route) and we are expecting the controller will be doing an HTTP POST/PUT.  We'll see in the next steps what the utility does with that information. 


### Fill in the app.add_player.process controller
This controller will be responsible for making the REST api call to the backend in order to add a player.  Remember the `add_page.html` ui-sref that pointed to the `app.add_player.process` route?  That route points to this controller. So, let's look at this controller.  The file `front/www/js/app/player_add/process/process.js` looks like this :


```
angular.module('app.user.add_user.process',[/*REPLACEMECHILD*/]);
angular.module('app.user.add_user.process').controller(
    'app.user.add_user.process',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                

        $scope.process_step=$state.params.process_step;
        if(_.size($scope.process_step)==0){
            Modals.error('Tried to reload a page that submits data.',$scope.site,'app');
            return;
        }
        
        $scope.player_info=$state.params.player_info;        
        //Modals.loading();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
```


Things you should pay attention to in this controller :
* The if block that starts with `if(_.size($scope.process_step)==0){` - what is going on here?  `_.size()` is provided by lodash (https://lodash.com/docs), which is a collection of utilities - it is EXTREMELY usefull and I highly recommend reading through the docs.  In this case, we are asking for the size of $scope.process_step (which was passed in from `add_player.html`).  Why are we doing this?  Because we want to protect against people hitting the reload button and causing double submits to the backend.  It turns out there are 2 ways to pass paramters between angular-ui-router routes - the first way preserves the passed parameters between page reloads, and the second way does not.  In this case, `process_step` is passed in using the second method - the end result is if someone reloads the process page, then `process_step` ends up being empty, and we stop the controller from proceeding.
* Also inside the same if block is the function `Modals.error()` - what does Modals.error() do?  Modals is one of the injected angular services - it's responsible for popping up Ionic modal dialogs.  Modals.error() specifically pops up an error modal.   The first argument is the message that the error modal will display.  The second argument will always be `$scope.site` - we'll get into why later on.  The third argument is the angular-ui-router route to go to after the user clicks 'ok' on the modal.
* The script has automatically addded the line `$scope.player_info=$state.params.player_info;`, which means that the passed in `player_info` will be easily accessible


Let's add the `AddPlayer()` function to this controller.  First uncomment all the commented lines and then change them as seen below :


```       
        add_player_promise = TimeoutResources.AddPlayer(undefined,{site:$scope.site},player_info)
        Modals.loading();        
        add_player_promise.then(function(data){
         $scope.resources = TimeoutResources.GetAllResources();
          Modals.loaded();
        })

```


`Modals.loading()` puts up a "loading" modal which prevents users from doing something stupid.


Let's look at the arguments to TimeoutResources.AddPlayer():
* the first argument can be a promise or `undefined` - if it's a promise, then `AddPlayer()` will wait for that promise to be resolved before it does anything.  If it's undefined, it will start immediately.  
* the second argument is an object, and the keys correspond to the url arguments we defined back in the angular resources - for example, the rest endpoint we defined for `addPlayerResource` was ':site/player' - so in this case the angular resource will substitue ':site' in the url with the contents of $scope.site.  We'll explain later where $scope.site is coming from. 
* the third argument is an object that will be placed in the POST request body - for example, `AddPlayer()` ends up sending a POST request to add player REST endpoint we defined earlier, and it will put the contents of the `player_info` object into that POST request body.


`AddPlayer()` returns a promise - this promise is resolved when the REST call returns a result.  


If you are not familiar with promises, stop right now and google "angular promise guide" and read any of the top results.  If you don't understand promises, you will NOT understand what is going on in TD.


When the promise that `AddPlayer()` returns is resolved, it will trigger the block of code that starts with `add_player_promise.then(function(data){` - this block just retrieves the result of the REST call and calls `Modals.loaded()`, which removes the 'loading' modal.


### Fill in the process.html
This page will be displayed as the `app.add_player.process` is making the REST api calls and when it done.  We'll fill it in with the following :


```
    <div class='col icon-label first-element'>
      <div class='row'>
        <div><i class="icon ion-person-add"></i></div>
        <div>{{resources.added_player.data.first_name}}</div>
      </div>
      <div class='row'>
        <div>Has Been Created</div>
      </div>
    </div>
    <center>
      <a id='AddAnotherPlayer' class='button button-large button-positive tablet-friendly-button' ui-sref='.^.^'>
        <span>Add Another Player</span>
      </a>
    </center>
```


Things to note in this page:
* `resources.added_player.data.first_name` will initially be undefined - but as soon as the REST api call completes and results are returned, it will be filled in with the appropriate results.
* in the AddAnotherPlayer button, the ui-sref is set to '.^.^', which means "goto the parent of this routes parent" - see the angular-ui-router docs for more information about this syntax.


### Create links to the "Add Player" page
The last step is to add links to the Add Player page so that users can reach it.  We want to add a link in the side menu.  We do this in `front/www/js/app/home.html`, and we are going to add the following to it (inside the <ion-list> tag):


```
        <a id='player_add_link' class='item item-icon-right' menu-close ui-sref='.add_player' ng-if="User.logged_in() == true && User.has_role('desk') == true">
          <div>
            Add Player
          </div>
          <i class="icon ion-chevron-right"></i>
        </a>
```


Before we look at the html we added, let's explain how home.html fits into things. If we look in `front/www/js/app/routes.js`, we find a angular-ui-router route defined.  Specifically, we find the `app` route defined (which is the parent route for all other routes), which uses the controller `IndexController` (which is defined in `front/www/js/app/app.js`) and uses home.html as the html template.  We also find insdie home.html the `ion-nav-view` tag - within this tag is where the content will be loaded when we move to routes that are children of `app` (see Ionic documentation for more information about the ion-nav-view tag).  You'll also notice that there are only two routes in `front/www/js/app/routes.js` - where are the routes for pages and controllers we just created?  In order to keep the routes.js from getting enormous, we split the routes.js file up.  If you look in `front/www/js/app/add_player` you will find a routes.js which defines all angular-ui-router routes under `app.player_add`.  The utility that generated the modules/controllers/html also created the routes.js and made sure it was inclued properly. Note that if we add a new module under `app.add_player.process`, the route for that will be added to `front/www/js/app/add_player/routes.js` automatically. 


Now lets look at the html we added to home.html
* the ui-sref is for `.add_player` - which we can do, because home.html is associated with the `app` route.
* the `User` service provides functions that lets you get information about the logged in user - in this case, we are checking that whatever is accessing this page is logged in and we are checking that the user has the 'desk' role assigned to them.  If either of those conditions are not true, you won't see the "Add Player" link.


NOTE : The User service prevents unauthorized users from viewing pages they are not authorized to see - but it does not stop them from calling the REST endpoints directly.  If a REST endpoint needs to be protected, you MUST also protect it on the backend side as we demonstrated above.


## Step 6 : Trying out the additions to the frontend
Before we try this out, uncomment the lines we commented out in `back/routes/player.py` in Step 2, and rebuild and restart the backend docker container 


Now, follow the quickstart steps in the README.md to try this out (i.e. the "Starting up frontend" steps).  Once you have started up the docker container, go to the following url in a browser : http://localhost:8100/


This will bring up the home page (which will be blank because you are not yet logged in).  Click on the menu icon (in the top right), and select the "Login" link.  Login with the following information : 


Username : test_desk

Password : test_desk


Once you are logged in, open the side menu again and you will see the "Add Player" link.  Select it and try adding a Player!


You might have noticed that when you went to http://localhost:8100/ it redirected to http://localhost:8100/#/test/app -  the "test" part of the url is how the "site" parameter is passed into TD - this is what gets used every time you saw $state.params.site in the code.  The value of site is the same as the Event we talked about when dealing with the backend.  For example, if we want to access http://localhost:8000/test/player on the backend, we would goto http://localhost:8100/#/test/app in our browser.


If you have a decent grasp on what was just covered, you should be able to look at any of the routes/controllers/html pages on the main branch and understand what is going on.  If weird stuff neeeded to happen, it will be well documented.


# Advanced Topics

## Next steps in understanding the Models
If you want to look at more complex examples of routes and models, the next step is to look at `back/td_types/User.py` to see the User SQLAlchemey model, and `back/routes/user.py` for the endpoints for adding and deleting users.


Some things to note about the User model:
* You can see an example of a many-to-many relationship - in this case, the relationship is between the User model and the Role model.  In plain english, the relationship is "A user can have mulitple roles, and each role can be assigned to multiple users".
* You don't have to understand most of the methods in the User class - they are mostly related to authentication (via the Flask-login extension).  What you should note is that you can define methods for the class, and you can use those methods on objects that are returned by SQLAlchemey queries.
* There is one method in the User class that you should pay attention to - `to_dict_simple()`.  This produces a dict representation of the User object that can be jsonified.  Why not just use `to_dict()` like we did in the player routes?  Because to_dict() ignores relationships - so we need a method which will include the results of that relationship in the returned dict.  Note that most Models will need a method like this.


Some things to note about the User endpoints:
* Note the way you use relationships - specifically, the way roles are added to users.
* Note the use of the `to_dict_simple()` on the returned `User` object.

## Next steps in understanding the Flask app instances (advanced)
If you are feeling adventerous, you can look at the code in `back/util` (which is used by the flask application for things like initialization and talking with the database), but it's not neccessary to be able to jump in. 










