Calendar
---

Calendar is a project to provide easy access to campus events at a centralized location.

## Development Setup
We use [vagrant](http://www.vagrantup.com/) to run our server. First install vagrant, and then run `vagrant up` to provision the virtual machine for you.

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

## Importing Dev Data
Start the app, then hit the home URL once. The events will start updating in the background.

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
  |-- __init__.py (sets up Flask app)
  |-- schema.py   (our SQLAlchemy ORM schema)
  |-- fb.py       (Facebook utilities)
  |-- static/     (your static files, such as js, css, imgs)
  |-- templates/  (Flask Jinja2 templates)
```


## Developers
* Alan Du
* David Hao
* Pooja Kathail
* Kevin Lin
* Emily Pakulski
* Angela Wang
