# TD : Pinball Scoring Software

TD is Pinball Scoring Software. Features include : 
* Native apps (Android and iOS) for administration and for players
* Players can buy tickets directly through the website
* Integrated with the IFPA website and Challonge
* Can be run on your laptop or in a cloud environment

# Quickstart
These instructions will allow you to get an instance of TD running on your machine so you can try it out.

### Prereqisites for Quickstart
The following are pre-requsites before you can run TD.

* You must be running on OS X or Ubuntu 
* You must have [docker](http://www.docker.com) installed
* You have checked out this git repo

NOTE : This quickstart is for demo purposes only.  If you want to run you own instance of TD, you do NOT want the quickstart.

### Starting up backend
`cd <top of checked out git repo>/back`

`docker build -t td_backend .`

`docker run -d -t -p 8000:8000 td_backend`

### Starting up frontend
`cd <top of checked out git repo>/front`

`docker build -t td_frontend .`

`docker run -t -d -p 8100:8100 -p 35729:35729 td_frontend`

### Try it out!
1. Visit the following url : http://localhost:8100/ 
2. You can login with one of the following userids/passwords :
  * test_admin/test_admin (full admin)
  * test_scorekeeper/test_scorekeeper (scorekeeper)
  * test_desk/test_desk (deskworker)
3. Have Fun!

# Contributing

If you want to help out, read [CONTRIBUTING.md](CONTRIBUTING.md)

# Reporting Bugs

something here about reporting bugs


