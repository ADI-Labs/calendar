import asyncio

import aiohttp
from icalendar import Calendar

from cal.schema import db, User, Event

async def get_individual_event(event, user):
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
    except TypeError:  # dtstart is a date, not a datetime
        cevent.start = event["dtstart"].dt

    try:
        cevent.end = event["dtend"].dt.replace(tzinfo=None)
    except TypeError:  # dtend is a date, not a datetime
        cevent.end = event["dtend"].dt
    except KeyError:  # no dtend
        pass

    return cevent

async def get_eventsatcu():
    # Parameters for query:
    #    sort=dtstart.utc     - sorts by start date
    #    format=text/calendar - to return in ics format
    #    count=200            - to return max number of events

    url = "https://events.columbia.edu/feeder/main/eventsFeed.gdo" + \
          "?sort=dtstart.utc:asc&format=text/calendar&count=200"
    async with aiohttp.get(url) as resp:
        cal = Calendar.from_ical(await resp.text())
    user = User.query.filter(User.name == "Sundial").first()

    coroutines = [get_individual_event(event, user)
                  for event in cal.walk('VEVENT')]
    for f in asyncio.as_completed(coroutines):
        db.session.add(await f)
    db.session.commit()


def update_from_eventsatcu():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_eventsatcu())
