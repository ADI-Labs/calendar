import asyncio
from urllib import parse as urlparse

import aiohttp
from bs4 import BeautifulSoup
from icalendar import Calendar

from cal.schema import db, User, Event

async def get_individual_event(event, user):
    event_name = event.find('title').text
    url = event.find('link').get_text()
    u = urlparse.urlparse(url)
    event_id = urlparse.parse_qs(u.query)["id"][0]

    base = "http://calendar.columbia.edu/sundial/webapi/"
    ical_url = base + "iCalendar.php?EventID={}".format(event_id)
    url = base + "get.php?vt=detail&id={}&con=standalone".format(event_id)

    async with aiohttp.get(ical_url) as r_event:
        cal = Calendar.from_ical(await r_event.text())

    cevent = Event.query.filter(Event.sundial_id == event_id).first()
    if cevent is None:
        cevent = Event(name=event_name, url=url, sundial_id=event_id,
                       user_id=user.id)

    for event in cal.walk('vevent'):
        cevent.start = event.get('dtstart').dt.replace(tzinfo=None)
        cevent.end = event.get('dtend').dt.replace(tzinfo=None)
        cevent.description = event.get('description')
        cevent.location = event.get('location')
    return cevent

async def get_engineering_events():
    url = 'http://engineering.columbia.edu/feeds/events'
    async with aiohttp.get(url) as resp:
        soup = BeautifulSoup(await resp.text())

    events = soup.find_all('item')
    user = User.query.filter(User.name == "Columbia Engineering").first()

    coroutines = [get_individual_event(event, user) for event in events]

    for f in asyncio.as_completed(coroutines):
        db.session.add(await f)
    db.session.commit()

def update_engineering_events():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_engineering_events())
