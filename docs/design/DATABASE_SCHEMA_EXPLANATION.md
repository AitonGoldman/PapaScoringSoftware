# The Database Schema (in plain english)

## Events
This table represents each `Event` (i.e. PAPA20 vs PAPA 19 vs LAX 2017).  Anything that is a `Event` level configuration parameter is recorded in this table.  For example, if you plan on using Stripe to allow players to purchase their own tickets, you would enter a Stripe API key into the `stripe_api_key` column for the `Event`.

## Event specific tables
In the rest of this document, you will see something like the following sentance : "Each event has it own <X> table".  That means that a seperate table will be created for each event - the table that is created will have the event name appended to the table.  The Flask Application created for that event will ONLY point to the table for the event.  For example : we'll need a table to record scores - if the event is named PAPA20, then we would call the table scores-papa20.  The Flask Application for PAPA20 will be passed the event name at initialization, and that Flask Application will ONLY look at the scores-papa20 table when looking up/recording scores.

## PssUsers, Roles, and EventRoles 

`Pss Users`, `Pss Event Users`, and `Players` are represented in the PssUsers table.  The Roles table represents the `Roles` that differentiate `Pss Users` from `Pss Event Users` and `Players`.  For example, scorekeeper_a has an entry in the PssUsers table and is a `Pss User` which means they have the scorekeeper `Role`, while player_a has an entry in the PssUsers table but has the player `Role`.  There is a many-to-many relationship between the PssUsers table and the Roles table.

There are two tables that capture the many-to-many relationship between PssUser and Roles.  The first is role_pssuser_mapping - this captures what type of user the user is (i.e. Pss User, Pss Event User, or Player).  The second table is role_pssuser_event_mapping - this captures event specific roles for the user (i.e. scorekeeper, tournament_director, etc).  Note that this means roles from one event do not carry over to other events - i.e. if I am assigned the deskworker role for PAPA 20, it doesn't mean my user for PAPA 21 automatically has that same role.

Note that this means there is a global list of users and players - i.e. you don't have to re-enter users or players for each event, and player history can be tracked from event to event.


## PssUsers and Events

All users/players represented in the PssUsers table should only be able to login to events that they are part of.  This means we want a many-to-many relationship between PssUser and Events.  This relationship is captured with the event_pssuser_mapping table.




