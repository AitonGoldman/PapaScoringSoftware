# How to help with PSS development
Work through this tutorial.  The tutorial consists of use cases which will highlight all the things you need to do (on the backend and frontend) when you want to add a new feature/fix a bug/refactor code, and will give some overview of all the individual components of PSS.  There will be links to quickstarts for external libraries/frameworks - if you want to dive deeper into the library/framework you can follow the links.  Once you have reached the end of the tutorial, you should be able to jump in and start submiting pull requests!

Do not hesitate to ask questions - this will become a reference to our slack instance once we have one.

# Overview of PSS
TD is made up of two parts : the backend and the frontend.  The backend is a [Flask](http://flask.pocoo.org/) wsgi application that offers a REST api and interfaces with databases using [SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.1/).  The frontend is an [Ionic](http://ionicframework.com/) application.

# Use Case 0 : Hello World
The goal of this is to let you dip your toes into the code, and get familiar with how to the PSS code is organized.  You'll be creating an endpoint that returns `Hello World` in json.  

## Step 0 : Checkout the Tutorial branch and install pre-requisites
Before you do anything, make sure you have checked out the TUTORIAL branch.

If you have never used git, you'll need to run the following command : 

```
git clone https://github.com/AitonGoldman/PapaScoringSoftware.git
cd PapaScoringSoftware
git checkout TUTORIAL
```

This will clone the git repository to your local machine, and then check out the TUTORIAL branch.  If you have never used git before - don't worry!  All the commands you will need for this tutorial will be in the tutorial.   If you want to learn more about git than what is in this tutorial and get some hands experience with git quickly, see [link here](https://try.github.io/levels/1/challenges/1).  All the following steps assume you have checked out the TUTORIAL branch.  This branch has all the core PSS code, but only has a minimal number of REST endpoints and SQLAlchmey models defined.  It's main purpose is to provide a starting point for new people to dive into the code. 

Next, you'll need to install the pre-requisites.  These instructions assume you running on Ubuntu (these instructions have been tested on Ubunutu 16.04).  Please follow the instructions in (install instructions here).

Finally, we are now ready to create our Hello World

## Step 1 : Create Hello World endpoint

Our goal is to add a Hello World endpoint to the PSS - this endpoint will return the string "Hello World" wrapped in a json object.  This means that if I goto the url `http://localhost/hello_world` then I will get back json with the text "Hello World" in it.

Note that you must have the PSS backend running for this to work - follow the end of the installation instructions to start the backend (if you have not already done so). 

The `routes` directory is where we keep the code that defines our endpoints, so we are going to create a file called `helloworld.py` to the `routes` directory.  The following will be the contents of that file : 

```
from lib.flask_lib import blueprints
from flask import jsonify

@blueprints.pss_admin_event_blueprint.route('/hellow_world',methods=['GET'])
def hello_world():
    return jsonify({'result':'Hello World'})

```

Let's look at this file line by line.  

Line 1 imports Flask Blueprints that we have defined in the `back/lib/flask_lib/blueprints.py` - we'll need the blueprints to define our endpoint.  If you want to know more about Flask Blueprints, follow this link : http://flask.pocoo.org/docs/0.12/blueprints/.  The TLDR is that the PSS uses Flask Blueprints for easily grouping endpoints - as we progress you'll see how we use those groupings. Note that the The `back/lib` directory is where keep all our shared code.   

Line 2 imports the method `jsonify` from Flask.  This method converts whatever it is passed into a json string and then puts that into a Flask Response object, assuming that thing can be serialized into json.  Any native python type will work - more complex objects probably won't.        

Line 4 is where we define a url which the PSS will respond to.  We use the `route()` method on the `pss_admin_event_blueprint` we imported, and we pass it two arguments : the url and the HTTP method.  In this case, we are telling the PSS to respond when someone requests the `/hello_world` url with a HTTP GET.  The `/hello_world` endpoint is now associated with the `pss_admin_event_blueprint` - when the code that instatiates our Flask Application gets run, it can just say 'use all the routes associated with the pss_admin_event_blueprint' (we'll get into how we use blueprints later on).

Line 5 defines the function that wil actually be called when the `hello_world` endpoint is hit. 

Line 6 returns the results of the jsonify() call.  Note that if a method is decorated with the `.route()` method then the results MUST be the results of a jsonify() call - PSS is setup to ONLY send json in response to HTTP requests.  The only exception to this rule is ... exceptions.  The PSS will take exceptions that are uncaught, format them as json, and return them (along with the appropriate HTTP error code) to the requestor.

So, let's try this bad boy out.  Try the following command: 

`curl http://localhost:8000/pss_test/hello_world`

and you should get back the following : 

`{"result":"Hello World"}`

You might have noticed the `pss_test` added to the url we requested - what is that about?  The short answer : the PSS has a concept of Events (i.e. PAPA 20 would be a PSS Event), and we tell the PSS which event we want to use by putting the event name in the url.  The pss_test Event is a special event that is created when you bootstrap the database.  We'll use it initially in this tutorial (mainly because it means we don't have to worry about creating a new event to work with ), but eventually we'll get more into Events and how they work.

Also, note that the PSS application you have running in the background automatically picked up your changes.  For development, the PSS is setup to automatically restart the server when changes are detected in order to pickup those changes.




