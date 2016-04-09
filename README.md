[![Stories in Ready](https://badge.waffle.io/ADI-Labs/calendar.png?label=ready&title=Ready)](https://waffle.io/ADI-Labs/calendar)
[![Build Status](https://travis-ci.org/ADI-Labs/calendar.svg?branch=master)](https://travis-ci.org/ADI-Labs/calendar)
Calendar
---

Calendar is a project to provide easy access to campus events at a
centralized location. It's written using
[Flask](http://flask.pocoo.org/) and
[SQLAlchemy](http://www.sqlalchemy.org/), using PostgreSQL for the
database.

The front-end is written using React and is being developed at
[calendar-web](http://github.com/adi-labs/calendar-web).

## Environment Setup

We use [Vagrant](http://www.vagrantup.com/) to set up our development
environment. Behind the scenes, it runs `config/bootstrap.sh` to set-up
everything up.

To set-up the development environment, run:

```bash
vagrant up
vagrant ssh
cd /vagrant
source config/settings.dev
```

## Running the app

To run the app, just run:

```bash
python run.py
```

You'll need to setup the database first though.

## Interacting with the database

`manage.py` is the main way to interact with the database. It has a
number of different subcommands:

```bash
python manage.py create     # create the database and fill it with data
python manage.py update     # update the database with new data
python manage.py delete     # delete everything in the database
python manage.py connect    # opens a pgcli REPL to Postgres
```

## Tests

We use the `flake8` linter to help ensure the Python code quality.  Unit
and integration tests live in the `tests/` folder and are written with
[pytest](http://pytest.org/latest/). To run the tests:

```bash
python test.py
```

`test.py` accepts all arguments and options that `pytest` does, so you
can run things like:

```bash
python test.py --pdb        # opens up the Python Debugger on test failure
python test.py --verbose
```

### App Structure
```
├── cal                         -- the Flask app
│   ├── ics.py
│   ├── __init__.py             -- routes
│   ├── schema.py               -- database schemas
│   └── templates/
├── config
│   ├── bootstrap.sh            -- script used for Vagrant bootstrapping
│   ├── environment.yml         -- specifies app dependencies
│   ├── groups.yml              -- stores User information
│   ├── __init__.py
│   └── settings.dev            -- environment variables
├── external/                   -- utility functions
├── manage.py
├── run.py
├── scrapers/                   -- list of scrapers
├── setup.cfg                   -- flake8 and pytest config settings
├── test.py
└── tests/                      -- tests
```
