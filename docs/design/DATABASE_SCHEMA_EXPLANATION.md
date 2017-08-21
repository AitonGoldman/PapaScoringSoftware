# The Database Schema (in plain english)

## Events
This table represents each Event (i.e. PAPA20 vs PAPA 19 vs LAX 2017).  Anything that is a Event level configuration parameter is recorded in this table.  For example, if you plan on using Stripe to allow players to purchase their own tickets, you would enter a Stripe API key into the stripe_api_key column for the Event.

## Event specific tables
In the rest of this document, you will see something like the following sentance : "Each event has it own <X> table".  That means that a seperate table will be created for each event - the table that is created will have the event name appended to the table.  The Flask Application created for that event will ONLY point to the table for the event.  For example : we'll need a table to record scores - if the event is named PAPA20, then we would call the table scores-papa20.  The Flask Application for PAPA20 will be passed the event name at initialization, and that Flask Application will ONLY look at the scores-papa20 table when looking up/recording scores.

Note that because event creation happens AFTER the Flask Application is initialized, tables that are event specific have to be explicitly created - see (link here) for details on how this happens.

## PssUsers, AdminRoles, EventUsers, Events, and EventRoles

Events are represented in the Events table.  Event Owners and Event Users are represented in the PssUsers table.  The AdminRoles table represents the roles that Event Owners will have.  The EventRoles table represents the roles Event User will have.  For example, a Event Owner will have the role `PSS_USER` from the Roles table, while a scorekeeper has the role `scorekeeper` from the EventRoles table.  The EventUsers table represents event-specific information for a Event User and is event specific.

There is a many-to-many relationship between...
- the PssUsers table and the Events table (i.e. captures which events each user has been added to).
- the PssUsers table and the AdminRoles table (i.e. captures which AdminRoles have been assigned to user).
- the PssUsers table and the EventRoles table - this is reperesented by an event specific table (i.e. captures which EventRoles have been assigned to a user for a given Event).

Note that this means there is a global list of users - i.e. you don't have to re-enter users for each event, and user history can be tracked from event to event.

## Players, PlayerRoles, EventPlayers

Basically the same as PssUsers, AdminRoles, EventUsers - except for players.  In addition, the EventPlayers table has different columns (since we need to record different event specific info for players).

Note that this means there is a global list of players - i.e. you don't have to re-enter players for each event, and player history can be tracked from event to event.

## Teams

Teams are represented by the Teams table.  There is a one-to-many relationship between Teams and Players (i.e. multiple players can be on one team).  Note that the PSS puts no hard-coded upper limit on the number of players on a team.

## A little bit more about PssUsers/Players and EventUsers/EventPlayers

Event Users/Players need the ability to have a seperate password/pin number (and other information) for each event.  There 2 reasons for this :
- Event Users/Players don't have to remember their password/pin number between events - TDs will reset/change the password/pin at the begining of each event for that event. 
- Prevents other Event Owners from (accidently or purposely) screwing with a Event User's/Players account.
- Provides a deterrent to people who might discover a Event Users/Players password/pin number and use it at a different event.

We provide this functionality by creating a EventUsers/EventPlayers tables for each event.  This table contains the encrypted password/pin number for a Event User/Player which is only valid for the given event.  There is a 1-to-1 relationship between the PssUsers/Players table and the event specific EventUsers/EventPlayers table.

## Tournaments, MultiDivisionTournaments, DivisionMachines, Machines!
Tournaments are represented in the Tournaments table.  It captures any configuration information for that tournament.  MultiDivisionTournaments represent a tournament with multiple divisions.  DivisionMachines represents machines in the tournament bank.  Machines represents the list of machines that the PSS knows about.

There is a one-to-many relationship between DivisionMachines and Machines (i.e. there can be 3 different Metallica's in 3 different Tournaments in an Event)
There is a one-to-many relationship between Tournaments and MultiDivisionTournaments (i.e. multiple Tournaments can be linked to a single MultiDivisionTournament)
There is a one-to-many relationship between Tournaments and DivisionMachines (i.e. one Tournament can have multiple DivisionMachines)

Note that in the case of a multi-division tournament, the "divisions" will be represented as seperate Tournaments with a entry in the MultiDivisionTournaments table.  This information will only be used at 2 times : 1) at ticket purchase time (to make sure the player doesn't accidently buy tickets for a division they are not registered for).  2) if a player wants to move between divisions, it will not allow players to move "down".









