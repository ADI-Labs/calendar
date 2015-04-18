import json

import requests
from flask import current_app
import iso8601
from external import utils

from cal.schema import db, User, Event
from config import FACEBOOK_ACCESS_TOKEN


def depaginate(data):
    if "paging" in data and "next" in data["paging"]:
        r = requests.get(data["paging"]["next"])
        data["data"] += depaginate(json.loads(r.text))

    return data["data"]


def get_users():
    url = "https://graph.facebook.com/v2.3/events"
    payload = {"access_token": FACEBOOK_ACCESS_TOKEN, "limit": 500}

    users = {}

    for chunk in utils.grouper(User.query.all()):
        ids = ",".join(str(user.fb_id)
                       for user in chunk
                       if user.fb_id is not None)
        payload["ids"] = ids

        r = requests.get(url, params=payload)
        users.update(json.loads(r.text))

    return {key: depaginate(value)
            for key, value in users.items()}


def update_fb_events():
    for user in User.query.all():
        if user.fb_id is None:
            continue

        events = graph.get_connections(id=user.fb_id, connection_name="events")
        events = events["data"]
        for event in events:
            event = graph.get_object(id=event["id"])
            event_id = int(event['id'])

            current_event = Event.query.filter_by(fb_id=event_id).first()
            if current_event is None:   # create new event
                current_app.logger.debug("New fb event from {}: {}"
                                         .format(user.fb_id, event['id']))
                current_event = Event(fb_id=event_id)

            # Parse the start and end times.
            start = iso8601.parse_date(event["start_time"])
            current_event.start = start.replace(tzinfo=None)
            end = event.get('end_time', None)
            if end is not None:
                end = iso8601.parse_date(end)
                current_event.end = end.replace(tzinfo=None)

            # Update other fields.
            current_event.user_id = user.id
            current_event.description = event.get("description", None)
            current_event.location = event.get('location', None)
            current_event.name = event['name']
            current_event.url = "https://www.facebook.com/" + event['id']

            db.session.add(current_event)

    db.session.commit()
