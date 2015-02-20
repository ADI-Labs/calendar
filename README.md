Calendar
---

Calendar is a project to provide easy access to campus events at a centralized location.




## Local Dev

This is the recommend means of setting up Calendar for development.
Next, install [vagrant](http://www.vagrantup.com/).
Once vagrant is installed, you can run `vagrant up`, and vagrant will provision the virtual machine for you.

To run the app, follow the these steps:

```bash
vagrant ssh
cd /vagrant
source config/settings.dev
python run.py
```

To setup the database, run:
```bash
vagrant ssh
cd /vagrant
source config/settings.dev
python create.py
=======
```



## Importing Dev Data
TODO


## Routes
TODO


## Data Sources
TODO

# app structure

```
|-- config/ (config settings and install scripts)
|-- README.md (This file)
|-- calendar/
\
|-- calendar.py  (the executable for this application)
|-- static/     (your static files, such as js, css, imgs)
|-- tests/      (unittest scripts that should be used during development)
```


# List of Developers

- Pooja Kathail
- Kevin Lin
- David Hao
- Alan Du
- Angela Wang
- Emily Pakulski
