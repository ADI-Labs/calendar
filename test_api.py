import datetime as dt
import json

import pytest


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
    u1 = User.query.filter(User.name == "Cthulhu").first()
    u2 = User.query.filter(User.name == "Gandalf").first()

    events = [
        Event(name="Cthulhu Awakens", start=now + day, user=u1),
        Event(name="Cthulhu Sleeps", start=now - day, user=u1),
        Event(name="Ph'nglui mglw'nafh Cthulhu", start=now + day * 3, user=u1),
        Event(name="Cthulhu R'lyeh wgah'nagl", start=now + day * 6, user=u1),
        Event(name="Cthulhu fhtagn!", start=now + day * 9, user=u1),
        Event(name="Mithrandir", start=now + day, user=u2),
    ]

    db.session.add_all(events)
    db.session.commit()

    return Event


def assert_json_equal(response, data):
    assert response.status_code == 200
    rdata = json.loads(response.data)
    assert "data" in rdata and len(rdata) == 1  # "data" is only key
    assert rdata["data"] == data


def test_homepage(app, db, User, Event):
    client = app.test_client()
    r = client.get('/')

    assert r.status_code == 200


def test_events(app, db, User, Event):
    now = dt.datetime.now()
    events = Event.query.filter(Event.start > now) \
                        .filter(Event.start < now + dt.timedelta(weeks=1))
    event_data = [event.to_json() for event in events.all()]

    client = app.test_client()
    assert_json_equal(client.get('/events/'), event_data)


def test_users(app, db, User, Event):
    now = dt.datetime.now()
    events = Event.query.filter(Event.start > now) \
                        .filter(Event.start < now + dt.timedelta(weeks=1))
    users = sorted({event.user for event in events}, key=lambda u: u.name)
    user_data = [user.to_json() for user in users]

    client = app.test_client()
    assert_json_equal(client.get('/users/'), user_data)


def test_search(app, db, User, Event):
    now = dt.datetime.now()
    events = Event.query.filter(Event.start > now) \
                        .filter(Event.start < now + dt.timedelta(weeks=1)) \
                        .whoosh_search("Cthulhu")
    event_data = [event.to_json() for event in events.all()]

    client = app.test_client()
    assert_json_equal(client.get('/search/Cthulhu'), event_data)
