from os import path
import datetime as dt

import pytest

from config import BASEDIR

@pytest.fixture(scope="module")
def app(request):
    from cal import app

    context = app.app_context()
    context.push()

    def teardown():
        context.pop()

    request.addfinalizer(teardown)

    return app


@pytest.fixture(scope="module")
def db(app, request):
    from cal import db
    db.init_app(app)
    db.create_all()

    def teardown():
        db.drop_all()
    request.addfinalizer(teardown)

    return db

@pytest.fixture(scope="module")
def User(app, db):
    from cal import User

    db.session.add_all([User(id=1, name="Cthulhu", fb_id=1),
                        User(id=2, name="Gandalf", fb_id=2)])
    db.session.commit()

    return User

@pytest.fixture(scope="module")
def Event(app, db, User):
    from cal import Event

    now = dt.datetime.now()
    day = dt.timedelta(days=1)

    events = [
        Event(name="Cthulhu Awakens", start=now + day, user_id=1),
        Event(name="Cthulhu Sleeps", start=now - day, user_id=1),
        Event(name="Ph'nglui mglw'nafh Cthulhu", start=now + day * 3, user_id=1),
        Event(name="Cthulhu R'lyeh wgah'nagl", start=now + day * 6, user_id=1),
        Event(name="Cthulhu fhtagn!", start=now + day * 9, user_id=1),
        Event(name="Mithrandir", start=now + day, user_id=2),
    ]

    db.session.add_all(events)
    db.session.commit()

    return Event

def test_homepage(app, db, User, Event):
    client = app.test_client()
    r = client.get('/')

    assert r.status_code == 200

