import requests
from icalendar import Calendar
# from cal.schema import db, User, Event

def update_from_eventsatcu():

    url = "https://events.columbia.edu/feeder/main/eventsFeed.gdo?sort=dtstart.utc:asc&format=text/calendar&count=200"
    r = requests.get(url)
    cal = Calendar.from_ical(r.text)
    user = User.query.filter(User.name == "events.columbia.edu").first() 

    for event in cal.walk('VEVENT'):
        print(event.get('uid'))
    
        event_id = event.get('uid')
        event_name = event.get('description')
        event_url = event.get('url')

        cevent = Event.query.filter(Event.sundial_id == event_id).first()
        if cevent is None:
            cevent = Event(name = event_name, url = url, sundial_id = event_id, user_id = user.id)

        cevent.start = event.get('dtstart').dt.replace(tzinfo=None)
        cevent.end = event.get('dtend').dt.replace(tzinfo=None)
        cevent.description = event_name
        cevent.location = event.get('location')

        db.session.add(cevent)
        
    db.session.commit()


update_from_eventsatcu()
