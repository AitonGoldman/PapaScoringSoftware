# How to help with PSS development
Work through this tutorial.  The tutorial consists of use cases which will highlight all the things you need to do (on the backend and frontend) when you want to add a new feature/fix a bug/refactor code, and will give some overview of all the individual components of PSS.  There will be links to quickstarts for external libraries/frameworks - follow the links if you need to.  Once you have reached the end of the tutorial, you should be able to jump in and start submiting pull requests!

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

This will clone the git repository to your local machine, and then check out the TUTORIAL branch.  If you have never used git before and want to get up to speed quickly on it, see [link here](https://try.github.io/levels/1/challenges/1) for a git tutorial.  Note that the git tutorial is not required to continue with this tutorial.  All the following steps assume you have checked out the TUTORIAL branch.  This branch has all the core PSS code, but only has a minimal number of REST endpoints and SQLAlchmey models defined.  It's main purpose is to provide a starting point for new people to dive into the code. 

Next, you'll need to install the pre-requisites.  These instructions assume you running on Ubuntu (these instructions have been tested on Ubunutu 16.04).  Please follow the instructions in (install instructions here).



