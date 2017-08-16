# The Database Schema (in plain english)

## Events
This table represents each Event (i.e. PAPA20 vs PAPA 19 vs LAX 2017).  Anything that is a Event level configuration parameter is recorded in this table.  For example, if you plan on using Stripe to allow players to purchase their own tickets, you would enter a Stripe API key into the stripe_api_key column for the Event.

## Event specific tables
In the rest of this document, you will see something like the following sentance : "Each event has it own <X> table".  That means that a seperate table will be created for each event - the table that is created will have the event name appended to the table.  The Flask Application created for that event will ONLY point to the table for the event.  For example : we'll need a table to record scores - if the event is named PAPA20, then we would call the table scores-papa20.  The Flask Application for PAPA20 will be passed the event name at initialization, and that Flask Application will ONLY look at the scores-papa20 table when looking up/recording scores.

## PssUsers, Roles, and EventRoles 

Event Owners and Event Users are represented in the PssUsers table.  The Roles table represents the roles that Event Owners will have.  The EventRoles table represents the roles Event User will have.  For example, a Event Owner will have the role `PSS_USER` from the Roles table, while a scorekeeper has the role `scorekeeper` from the EventRoles table.  There are is a many-to-many relationship between the PssUsers table and the Roles.  There is also a many-to-many relationship between the PssUsers table and the EventRoles table.

For each Event there is a different table that captures the many-to-many relationship between the PssUsers table and the EventRoles table.  Note that this means roles from one event do not carry over to other events - i.e. if I am assigned the deskworker role for the PAPA 20 Event, it doesn't mean my user automatically has that same role for the PAPA 21 Event.

Note that this means there is a global list of users and players - i.e. you don't have to re-enter users or players for each event, and player history can be tracked from event to event.

## PssUsers and EventUsers
Event Users need the ability to have a seperate password (and other information) for each event.  There 2 reasons for this :
- Event Users don't have to remember their password between events - TDs can just reset/change the password at the begining of each event for that event. 
- Prevents other Event Owners from (accidently or purposely) screwing with a Event User's account.
- Provides a deterrent to people who might discover a Event Users password and use it at a different event.

We provide this functionality by creating a EventUsers tables for each event.  This table contains the encrypted password for a Event User which is only valid for the given event.  There is a 1-to-1 relationship between the PssUsers table and the event specific EventUsers table.

## PssUsers and Events

All Event Users represented in the PssUsers table should only be able to login to events that they are part of.  This means we want a many-to-many relationship between PssUser and Events.  This relationship is captured with the event_pssuser_mapping table.




