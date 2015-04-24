from __future__ import absolute_import


def update_engineering_events():
    from cal.schema import db, User, Event
    from bs4 import BeautifulSoup
    import requests
    from icalendar import Calendar
    import urlparse

    r = requests.get('http://engineering.columbia.edu/feeds/events')
    soup = BeautifulSoup(r.text)

    events = soup.find_all('item')
    user = User.query.filter(User.name == "Columbia Engineering").first()
    for event in events:
        current_soup = BeautifulSoup(event.renderContents())

        event_name = current_soup.find('title').text
        url = current_soup.find('link').get_text()
        # event url
        u = urlparse.urlparse(url)
        event_id = urlparse.parse_qs(u.query)["id"][0]

        base = "http://calendar.columbia.edu/sundial/webapi/"
        ical_url = base + "iCalendar.php?EventID={}".format(event_id)
        url = base + "get.php?vt=detail&id={}&con=standalone".format(event_id)

        r_event = requests.get(ical_url)
        cal = Calendar.from_ical(r_event.text)

	current_event = Event.query.filter(Event.sundial_id == event_id).first()
        if current_event is None:
            current_event = Event(name=event_name, url=url, 
                                  sundial_id=event_id, user_id=user.id)

        # only one event in cal
        for event in cal.walk('vevent'):
            current_event.start = event.get('dtstart').dt.replace(tzinfo=None)
            current_event.end = event.get('dtend').dt.replace(tzinfo=None)
            current_event.description = event.get('description')
            current_event.location = event.get('location')


        db.session.add(current_event)
    db.session.commit()
