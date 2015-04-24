import datetime as dt
import json
from os.path import join

import pytest

from config import BASEDIR, TESTING


@pytest.fixture(scope="session")
def app(request):
    from cal import app
    context = app.app_context()
    context.push()

    def teardown():
        context.pop()
    request.addfinalizer(teardown)

    return app


@pytest.fixture(scope="session")
def db(app, request):
    from cal import db
    db.init_app(app)
    db.create_all()

    def teardown():
        db.drop_all()
    request.addfinalizer(teardown)

    return db


@pytest.fixture(scope="session")
def User(app, db):
    from cal import User

    db.session.add_all([User(id=1, name="Cthulhu", fb_id=1),
                        User(id=2, name="Monty Python", fb_id=2),
                        User(id=3, name="Sauron", fb_id=3)])
    db.session.commit()

    return User


@pytest.fixture(scope="session")
def Event(app, db, User):
    from cal import Event

    start = dt.datetime(2015, 3, 14)  # Saturday
    day = dt.timedelta(days=1)

    with open(join(BASEDIR, "tests/events.json")) as fin:
        events = json.load(fin)

    for event in events:
        event["start"] = start + day * event["start"]
        if "end" in event:
            event["end"] = start + day * event["end"]
        db.session.add(Event(**event))

    db.session.commit()

    return Event

assert TESTING, ("\n\nYou are not in a testing environment. Please run:\n"
                 "   source config/settings.test")
