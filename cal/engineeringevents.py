from urllib import parse as urlparse

from bs4 import BeautifulSoup
import requests
from icalendar import Calendar

from cal.schema import db, User, Event


def update_engineering_events():
    r = requests.get('http://engineering.columbia.edu/feeds/events')
    soup = BeautifulSoup(r.text)

    events = soup.find_all('item')
    user = User.query.filter(User.name == "Columbia Engineering").first()
    for event in events:
        current_soup = BeautifulSoup(event.renderContents())

        event_name = current_soup.find('title').text
        url = current_soup.find('link').get_text()
        u = urlparse.urlparse(url)
        event_id = urlparse.parse_qs(u.query)["id"][0]

        base = "http://calendar.columbia.edu/sundial/webapi/"
        ical_url = base + "iCalendar.php?EventID={}".format(event_id)
        url = base + "get.php?vt=detail&id={}&con=standalone".format(event_id)

        r_event = requests.get(ical_url)
        cal = Calendar.from_ical(r_event.text)

        cevent = Event.query.filter(Event.sundial_id == event_id).first()
        if cevent is None:
            cevent = Event(name=event_name, url=url, sundial_id=event_id,
                           user_id=user.id)

        # only one event in cal
        for event in cal.walk('vevent'):
            cevent.start = event.get('dtstart').dt.replace(tzinfo=None)
            cevent.end = event.get('dtend').dt.replace(tzinfo=None)
            cevent.description = event.get('description')
            cevent.location = event.get('location')

        db.session.add(cevent)
    db.session.commit()
