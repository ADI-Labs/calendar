import json

import requests
import iso8601
from external import utils

from cal.schema import db, User, Event
from config import FACEBOOK_ACCESS_TOKEN


def depaginate(data):
    """Depaginates facebook data.

    Facebook only returns a certain number of results for each request.
    To get the full results, we have to follow "next" urls.

    :param json - Full json of front page
    :return List[json] - List of all result data
    """
    if "paging" in data and "next" in data["paging"]:
        r = requests.get(data["paging"]["next"])
        data["data"] += depaginate(json.loads(r.text))

    return data["data"]


def get_users():
    """Gets list of Facebook users and their events.

    :return Dict[str, List[str]] - Maps user id to (incomplete) event blobs
    """
    url = "https://graph.facebook.com/v2.3/events"
    payload = {"access_token": FACEBOOK_ACCESS_TOKEN, "limit": 500}

    users = {}

    query = User.query.filter(User.fb_id.isnot(None))
    for chunk in utils.grouper(query):
        payload["ids"] = ",".join(str(user.fb_id) for user in chunk)

        r = requests.get(url, params=payload)
        users.update(json.loads(r.text))

    return {key: depaginate(value) for key, value in users.items()}


def update_fb_events():
    url = "https://graph.facebook.com/v2.3/"
    payload = {"access_token": FACEBOOK_ACCESS_TOKEN}

    for user_id, events in get_users().items():
        user = User.query.filter(User.fb_id == user_id).first()

        for chunk in utils.grouper(events):
            ids = ",".join(event_data["id"] for event_data in chunk)
            payload["ids"] = ids

            # new request to get complete information
            r = requests.get(url, params=payload)
            data = json.loads(r.text)

            for event_id, event_data in data.items():
                event = Event.query.filter(Event.fb_id == event_id).first()
                if event is None:
                    event = Event(fb_id=event_id)

                start = iso8601.parse_date(event_data["start_time"])
                event.start = start.replace(tzinfo=None)

                if "end_time" in event_data:
                    end = iso8601.parse_date(event_data["end_time"])
                    event.end = end.replace(tzinfo=None)

                event.user_id = user.id
                event.description = event_data.get("description", "")
                event.location = event_data.get('location', None)
                event.name = event_data['name']
                event.url = "https://www.facebook.com/" + event_data['id']

                db.session.add(event)
    db.session.commit()
