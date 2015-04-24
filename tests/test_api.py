import json
from urllib.parse import urlencode


def assert_json_equal(response, query):
    assert response.status_code == 200
    rdata = json.loads(response.data.decode())
    data = [d.to_json() for d in query.all()]

    # "data" is only key in rdata
    assert "data" in rdata and len(rdata) == 1

    # check equality, but ignore order
    assert len(rdata["data"]) == len(data)
    for d in rdata["data"]:
        assert d in data


def test_homepage(app, User, Event):
    client = app.test_client()
    assert client.get("/").status_code == 200


def test_events(app, User, Event):
    events = Event.query.filter(Event.id.in_([1, 3, 4, 6]))

    client = app.test_client()
    for i in range(7):  # 7 days a week
        url = '/events/2015/3/{}'.format(15 + i)
        assert_json_equal(client.get(url), events)


def test_users(app, User, Event):
    users = User.query.filter(User.id.in_([1, 2]))

    client = app.test_client()
    for i in range(7):  # 7 days a week
        url = '/users/2015/3/{}'.format(15 + i)
        assert_json_equal(client.get(url), users)


def test_search(app, User, Event):
    events = Event.query.filter(Event.id.in_([1, 3, 4]))

    client = app.test_client()
    for i in range(7):
        url = '/events/2015/3/{}'.format(15 + i)
        url += "?" + urlencode({"search": "Cthulhu"})

        assert_json_equal(client.get(url), events)
