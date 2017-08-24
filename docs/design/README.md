# Papa Scoring Software Architecture

## Overview
The Papa Scoring Software is pinball tournament scoring software that is designed to meet the following requirements:

- It must support desktop and mobile browsers
- It must be scalable 
- It must be easy to add on new features
- It must be fast
- It must use off the shelf libraries/frameworks when possible

The PSS backend is a REST server built on Flask with a SQLAlchemy talking to a Postgres database.  The PSS frontend is built on Ionic.  The rest of this document describes the design of the PSS.

## Some Definitons...

Before we begin, we need to go over some definitions :
- An `Event` (i.e. PAPA 20) contains a number of `Tournaments`.
- A `Event Owner` can create and edit `Events`.
- A `Event User` is a user involved in running the tournament (i.e. deskworker, scorekeeper, TD, etc).
- A `Event User` who has TD permissions can create `Tournaments` in a `Event`. 
- A `Player` is a player registered in a specific event.
- A `PSS Instance` is an instance of the PSS that is running
- A `Flask Application` is an instantiated instance of a `Flask` object

## Database Schema overview

We want the following from our database :
- A global list of `Players` across all events
- A global list of all `Event Users` across all events
- A global list of `Events` and any configuration information specific to each event
- The ability to designate players as participating in a specific `Event`
- The ability to designate `Event Users` as participating in a specific event
- The ability to keep scores and ticket purchases seperate between `Events`

We do this by keeping everything in one postgres database, but keeping event specific information in seperate tables (i.e. there is a `Player` table for PAPA 20 and a seperate `Player` table for Pittsburgh Pinball Open).

Please see the [Database Schema] document for in depth details (DATABASE_SCHEMA_EXPLANATION.md)

## Flask App Dispatching and scalability

The goal for the PSS is to be able to scale up by simply starting another instance of the PSS.  We do this by...
- storing all `Event` and tournament configuration information in a single postgres database.
- not requiring the PSS instance to run on the same machine as the postgres database.
- having each PSS instance be able to handle requests for all `Events`.

In turns out acheiving point 3 is a little tricky because SQLAlchemy can't point at different tables once the `Flask Application` has been instantiated.  So, we do something called application dispatching (see this link for the nitty gritty : ).  The TLDR; is that the PSS looks at the incoming url, determines the `Event` the request is directed at, and then directs the request to a `Flask Application` that is pointed only to the tables that are relevant to that `Event`.

If you want more details on the implementation, you can start by looking at [back/app/__init__.py](../../back/app/__init__.py).

## Event Users and Players

The PSS has three types of users :
- a `Event Owner`
- a `Event User`
- a `Player`

## Permissions and Roles

Roles determine what the users/players can (and can not do) and are assigned to indiviual users/players. Roles for Event Users (i.e. deskworker, scorekeeper, tournament director, etc) are assigned by Event Owners.  For example, let's say I am an Event Owner and Elizabeth is a scorekeeper at my event - then I will get the `Tournament_Director` role assigned to my account automatically for my event and I will assign the `Scorekeeper` role to Elizabeth's account for my event.  Note that event roles are specific to `Events` - for example, let's say for PAPA 20 my event roles are scorekeeper and deskworker.  But for PPO 6 it is just scorekeeper.  Having the deskworker role in PAPA 20 does not mean I get deskworker permissions in PPO 6.

Note that the frontend uses a user/player roles to determine what to show.  If a user/player with incorrect permissions tries to perform an action on the backend, that action will be rejected.

## The Pss Admin interface and Events

The Pss Admin interface is a seperate `Flask Application` and allows you to do the following things :
- Create an `Event`
- Edit `Event` level settings ( for `Events` you created)
- Create a new `Event User`
- Edit a `Event User` 

Each `Event` will have a seperate `Flask Application`.  You will be able to do the following within each `Event` (depending on your roles):
- Create and edit Tournaments
- Create and edit `Event Users`
- Register players for the `Event`
- Create tickets for players in the system
- Purchase tickets directly (if you are a player)
- Queue players or Self-queue
- Record Scores
- View Results

## Logging in

The backend provides three different ways to login - they are :
- Login for a `Event Owner` to the admin interface
- Login for a `Event User` or a `Event Owner` to an `Event`
- Login for a `Player` to an `Event`

A `Event Owner` can log into the Pss Admin interface or into a specific `Pss Event`.  A `Event User` can log into a specific event with their username and password.  A `Player` will also be able to log into a specific event, but will need to use a different login endpoint than the `Event User`.  This is because a player will use different credentials to login - specifically, the player will use their player number and player pin (both assigned when players are added to an Event)

The admin interface is a seperate `Flask Application` - this means that if you login to the admin interface, the cookie with your credentials will not give you access to a `Event` - you will need to explicitly login to an Event seperately.  The reverse is also true (i.e. logging into an event will not give you access to the admin interface).  Note that this is also true of seperate `Events` (i.e. I'm a deskworker in both the PAPA 20 event and the PPO 6 event - if I login to the PAPA 20 event, that does not log me into the PPO 6 event).

## Creating and editing Events and Tournaments

Only a Event Owner can create an Event through the admin interface.  Event Owners can only edit Events they have created.  In order to create/edit a Tournament they must login to an event.  Event Owners can only create/edit tournaments in their own Events or in Events they have been given the Tournament Director role.

Once a Tournament is created it is possible to add Machines to that tournament.  Once a Machine is added to a tournament, it is possible to disable or remove the machine.  Disabling the machine means no new games can be started on the machine and the machine will be marked as DOWN in the UI - you would use this when a machine is down for tech repair.  Removing a machine means that no new games can be started on the game and the machine will be removed from the UI (except for results) - you would use this when a machine is pulled from the bank.

A tournament can be marked as active or inactive.  In an active tournament, players can buy tickets, start new games, and have scores recored.  In an inactive, players can buy tickets and have scores recorded but can't start new games.

Tournaments have a property "allow_ticket_purchases" - if the property is set to false, then ticket purchases will not be allowed (from the desk or directly by players).  Note that this can be set independently of the tournament active/inactive flag (i.e. you can cut off ticket sales before the tournament ends).

## MetaTournaments

Let's say you are running a multi-day tournament, and you want to have a seperate classics tournament on each day of the event.  MetaTournaments allow players to purchase classics tickets that are good for any of the classics tournaments.  Event users with the Tournament_Director role can create MetaTournaments and add existing divisions to them.  Note that MetaTournaments are only relevant when purchasing tickets, and are not used during scorekeeping or displaying results. 

## Creating users and players, or adding existing users and players to events

A Event Owner user can be created in 2 ways

- The Pss Instance admin creates the user (i.e. the person who setup and is running the PSS instance)
- The person who wants the account goes through the email valiation process

The end result is an Event Owner user is created.

Once the Event Owner is created, they can create Events and Event Users.  As an example, let's say the Event Owner Doug wants to add Fred as a scorekeeper to his Event.  He would go through the following steps : 

- Doug logs into his Event
- Doug enters Freds name into the Event User creation screen
- The system determines if Fred already has an account
- If he does, then Doug assigns Fred's account the scoreekeeper role for Doug's event and set's Fred's password (which is only valid for Doug's event)
- If he doesn't, Doug does all the same steps as if the account was there but the system creates Fred's account silently

Note that when Doug created his event, his account was automatically added to his event as a Tournament Director.

The process for adding players to an event is similar to adding Event Users - with the additional steps :
- Players are assigned a player number (i.e. 123) and a player pin ( for logging into the Event i.e. 4444) that are specific to each Event
- Players can have an ifpa id associated with them
- Players can have a wppr ranking associated with them (which is updated upon being added to an event) 

## Teams

The PSS allows you to create teams and assign players to teams.  Teams are event specific. 

Each Tournament allows you to configure.. 
- whether or not the Tournament is a team tournament.
- the max number of people per team.






