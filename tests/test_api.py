import datetime as dt
import json

import pytest


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
