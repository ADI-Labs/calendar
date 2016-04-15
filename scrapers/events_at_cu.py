import requests
from icalendar import Calendar

from cal.schema import db, User, Event


def update_from_eventsatcu():
    # Parameters for query:
    #    sort=dtstart.utc     - sorts by start date
    #    format=text/calendar - to return in ics format
    #    count=200            - to return max number of events

    url = "https://events.columbia.edu/feeder/main/eventsFeed.gdo" + \
          "?sort=dtstart.utc:asc&format=text/calendar&count=200"
    r = requests.get(url)
    cal = Calendar.from_ical(r.text)
    user = User.query.filter(User.name == "Sundial").first()

    for event in cal.walk('VEVENT'):
        sundial_id = str(event['uid'])

        cevent = Event.query.filter(Event.sundial_id == sundial_id).first()
        if cevent is None:
            cevent = Event(sundial_id=sundial_id, user_id=user.id)

        cevent.name = event["summary"]
        cevent.description = event["description"]
        cevent.location = event.get('location')
        cevent.url = event.get("url")

        try:
            cevent.start = event["dtstart"].dt.replace(tzinfo=None)
        except TypeError:   # dtstart is a date, not a datetime
            cevent.start = event["dtstart"].dt

        try:
            cevent.end = event["dtend"].dt.replace(tzinfo=None)
        except TypeError:   # dtend is a date, not a datetime
            cevent.end = event["dtend"].dt
        except KeyError:    # no dtend
            pass

        db.session.add(cevent)
    db.session.commit()
