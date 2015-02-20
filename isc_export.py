from icalendar import Calendar as iCalendar, Event as iEvent, vText, vDatetime
import tempfile, os # being able to write a file
from cal.schema import Event as OurEvent
from cal import app
from time import strftime
from datetime import datetime

def main():
    # create Calendar object
    cal = iCalendar()
    cal['dtstart'] = vDatetime(datetime.now()) # formats to .ics compatible datetime
    cal['summary'] = 'Calendar for Columbia University made by ADI (adicu.com).'

    events = OurEvent.query.all()

    for e in events:    
        # for every event, create an event object
        vevent = iEvent()
        vevent['name'] = e.name
        vevent['organizer'] = e.user.name
        vevent['location'] = vText(e.location)
        vevent['dtstart'] = vDatetime(e.start)

        # add each event to calendar
        cal.add_component(vevent)
    
    # write file to calendar
    filename = 'calendar_adi_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.ics'
    f = open(filename, 'wb')
    f.write(cal.to_ical())
    f.close()

    print 'Exported events to .isc file.'

with app.app_context():
    main()
