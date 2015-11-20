Calendar
---


[![Build Status](https://travis-ci.org/adicu/calendar.svg?branch=master)](https://travis-ci.org/adicu/calendar)<F37>

Calendar is a project to provide easy access to campus events at a centralized location.

## Development Setup
Please be sure to fork this repository to your own repository before beginning any work. 

We use [vagrant](http://www.vagrantup.com/) to run our server. First [install vagrant](https://www.vagrantup.com/downloads.html)

Run `vagrant up` to provision the virtual machine for you.

Once vagrant is setup, run:
```bash
vagrant ssh
cd /vagrant
source config/settings.dev
```
and you should be good to go.

## Local Dev

To setup the database, run
```bash
python create.py
```

To run the server, run:
```bash
python run.py
````

If you want to run the event updater every 30 minutes, run:
```bash
celery worker -A cal.celery & python run.py
```

Try to avoid running this, since killing Celery is annoying. When finished, run:
```bash
ps
```
and kill the processes with the name "celery":
```bash
kill -9 <process-id>
```

I recommend running the database setup script to refresh the data.

## Importing Dev Data
Running create.py will fill the database with real data.

## Routes
Supported routes currently include:
```
/       : Calendar homepage with upcoming events
/events   : Returns all events [For development purposes, will be removed eventually]
```

## Data Sources
For now, we get events from Facebook using their API. The Facebook groups that we get events from are listed `cal/fb.py`

## app structure

```
|-- config/ (config settings and install scripts)
|-- README.md (This file)
|-- run.py    (runs the server)
|-- cal/
\
  |-- __init__.py   (Sets up Flask app)
  |-- schema.py     (Our SQLAlchemy ORM schema)
  |-- fb.py         (Facebook utilities)
  |-- groups.yml    (Contains the clubs' information)
  |-- logs/         (Log files will be added here)
  |-- static/       (Your static files, such as js, css, imgs)
  |-- templates/    (Flask Jinja2 templates)
```


## Developers
* Alan Du
* David Hao
* Pooja Kathail
* Kevin Lin
* Emily Pakulski
* Angela Wang

## Developers 2.0
* Jonathan
* Gabrielle
* Diana
* Sophie

