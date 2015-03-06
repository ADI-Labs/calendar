from facebook import GraphAPI
from cal.schema import db, User, Event
from config import FACEBOOK_ACCESS_TOKEN
import iso8601
import yaml
from flask import current_app

graph = GraphAPI(FACEBOOK_ACCESS_TOKEN)


def update_fb_events():
    f = open('cal/fb_groups.yml')
    page_ids = yaml.load(f).keys()
    f.close()
    for page_id in page_ids:
        user = User.query.filter_by(id=page_id).first()
        if user is None:
            u = graph.get_object(id=page_id)
            user = User(id=page_id, name=u["name"])
            db.session.add(user)

        events = graph.get_connections(id=page_id, connection_name="events")
        events = events["data"]
        for event in events:
            event = graph.get_object(id=event["id"])
            event_id = int(event['id'])

            current_event = Event.query.filter_by(source="facebook",
                                                  source_id=event_id).first()
            if current_event is None:   # create new event
                current_app.logger.debug("New fb event from %s: %s" % (page_id, event['id']))
                current_event = Event(source="facebook", source_id=event_id)

            # Parse the start and end times.
            start = iso8601.parse_date(event["start_time"])
            current_event.start = start.replace(tzinfo=None)
            end = event.get('end_time', None)
            if end is not None:
                end = iso8601.parse_date(end)
                current_event.end = end.replace(tzinfo=None)

            # Update other fields.
            current_event.user = user
            current_event.description = event["description"]
            current_event.location = event.get('location', None)
            current_event.name = event['name']
            current_event.url = "https://www.facebook.com/" + event['id']

            db.session.add(current_event)

    db.session.commit()
