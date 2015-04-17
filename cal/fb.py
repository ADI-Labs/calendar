from facebook import GraphAPI
from cal.schema import db, User, Event
from config import FACEBOOK_ACCESS_TOKEN
import iso8601
from flask import current_app

graph = GraphAPI(FACEBOOK_ACCESS_TOKEN)


def update_fb_events():
    for user in User.query.all():
        if user.fb_id is None:
            continue
        print user.fb_id, type(user.fb_id)

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
