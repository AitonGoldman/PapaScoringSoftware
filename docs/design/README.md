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
- A `PSS User` can create and edit `Events`.
- A `PSS Event User` is a user involved in running the tournament (i.e. deskworker, scorekeeper, TD, etc).
- A `PSS Event User` who has TD permissions can create `Tournaments` in a `Event`. 
- A `Player` is a player registered in a specific event.
- A `PSS Instance` is an instance of the PSS that is running
- A `Flask Application` is an instantiated instance of a `Flask` object


## Database Schema overview

We want the following from our database :
- A global list of `Players` across all events
- A global list of all `PSS Event Users` across all events
- A global list of `Events` and any configuration information specific to each event
- The ability to designate players as participating in a specific `Event`
- The ability to designate `PSS Event Users` as participating in a specific event
- The ability to keep scores and ticket purchases seperate between `Events`

We do this by keeping everything in one postgres database, but keeping event specific information in seperate tables (i.e. there is a `Player` table for PAPA 20 and a seperate `Player` table for Pittsburgh Pinball Open).

Please see the [Database Schema] document for in depth details (DATABASE_SCHEMA_EXPLANATION.md)

## Flask App Dispatching and scalability

The goal for the PSS is to be able to scale up by simply starting another instance of the PSS.  We do this by...
- storing all `Event` and tournament configuration information in a single postgres database.
- not requiring the PSS instance to run on the same machine as the postgres database.
- having each PSS instance be able to handle requests for all `Events`.

In turns out acheiving point 3 is a little tricky because SQLAlchemy can't point at different tables once the `Flask Application` has been instantiated.  So, we do something called application dispatching (see this link for the nitty gritty : ).  The TLDR; is that the PSS looks at the incoming url, determines the `Event` the request is directed at, and then directs the request to a `Flask Application` that is pointed only to the tables that are relevant to that `Event`.

If you want more details on the implementation, look at [back/app/__init__.py](../../back/app/__init__.py).

## Permissions and Roles
The PSS has three types of users :
- a `Pss User`
- a `Pss Event User`
- a `Player`

All three are stored in the same table ( in the `PssUser` table ) - the thing that differentiates them are their assigned `Roles`.  For example, a `Pss User` will have the `PssUser` role assigned to them, while a `Pss Event User` will have the `PssEventUser` role assigned to them.  Note that event `Roles` are specific to `Events` - for example, for PAPA 20 my event `Roles` are scorekeeper and deskworker.  But for PPO 6 it is just scorekeeper.  Having the deskworker `Role` in PAPA 20 does not mean I get deskworker permissions in PPO 6.

`Roles` are used by the backend to determine what a user/player can and can not do.  The frontend uses a user/player `Roles` to determine what to show.  If a user/player with incorrect permissions tries to perform an action on the backend, that action will be rejected.

## The Pss Admin interface and Events

The Pss Admin interface is a seperate `Flask Application` and allows you to do the following things :
- Create an `Event`
- Edit `Event` level settings ( for `Events` you created)
- Create a new `PssUser`
- Edit a `PssUser` (your own or one you created)

Each `Event` will have a seperate `Flask Application`.  You will be able to do the following within each `Event` (depending on your `Roles`):
- Create and edit Tournaments
- Create and edit `Pss Event Users`
- Register players for the `Event`
- Create tickets for players in the system
- Purchase tickets directly (if you are a player)
- Queue and Self-queue players
- Record Scores
- View Results

## Logging in

The backend provides three different ways to login - they are :
- Login for a `Pss User` to the admin interface
- Login for a `Pss Event User` or a `Pss User` to an `Event`
- Login for a `Player` to an `Event`

A `Pss User` can log into the Pss Admin interface or into a specific `Pss Event`.  A `Pss Event User` can log into a specific event.  A `Player` will also be able to log into a specific event, but will need to use a different login endpoint than the `Pss Event User` (due to using different credentials than the `Pss Event User` i.e. player number/pin vs username/password)

The admin interface is a seperate `Flask Application` - this means that if you login to the admin interface, the cookie with your credentials will not give you access to a `Event` - you will need to explicitly login to an Event seperately.  The reverse is also true (i.e. logging into an event will not give you access to the admin interface).  Note that this is also true of seperate `Events` (i.e. I'm a deskworker in both the PAPA 20 event and the PPO 6 event - if I login to the PAPA 20 event, that does not log me into the PPO 6 event).


