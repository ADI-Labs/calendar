from icalendar import Calendar as iCalendar, Event as iEvent
import tempfile, os # being able to write a file
from cal.schema import Event as OurEvent
from cal import app

"""
    id = db.Column(db.Integer, primary_key=True)

    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime)
    location = db.Column(db.String(64))
    url = db.Column(db.String(128), unique=True)
    name = db.Column(db.String(128), nullable=False)
""" 

# TODO:
# set dtstart to something real
# give calendar a logical name

def main():
    # create Calendar object
    cal = iCalendar()
    cal['dtstart'] = '20050404T080000'
    cal['summary'] = 'Calendar for Columbia University.'

    events = OurEvent.query.all()

    for e in events:    
        # for every event, create an event object
        vevent = iEvent()
        vevent['name'] = e.name

        # add each event to calendar
        cal.add_component(vevent)
    
    # write file to calendar
    f = open('example.ics', 'wb')
    f.write(cal.to_ical())
    f.close()

    print 'Exported events to .isc file.'

with app.app_context():
    main()
