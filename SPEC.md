
# Facebook API

The Facebook API is used to store event data locally with SQLite.

## Data

TODO

## Updating Data

A separate daemon process should watch for new files to be added to the server.
Upon receiving a new digest it should be processed and inserted to the database.
The updates should be logged.
The details of this implementation are very flexible.



# API

TODO


### Response Format:
TODO




#### Individual Queries

TODO


#### Ranged Queries

Keys:

TODO


### Endpoints:

TODO

## Tools

#### Language

For ease of development we will use Python 2.7 with the [Flask framework](http://flask.pocoo.org/).
Flask allows simple monkey patching of [Gevent](http://www.gevent.org/) for performance. 



#### Database

The database used is [SQLite] (http://sqlite.org/) with [Flask SQLAlchemy] (http://pythonhosted.org/Flask-SQLAlchemy/).

#### Authentication

TODO



## Roadmap
Data sources
* Facebook Events (priority)
* Columbia UEM
* Google Calendar
Export
* Google Calendar
* iCal
Event Creation (far future)
* Register and allow users to create events
* Automatically create Facebook and Google Calendar events

