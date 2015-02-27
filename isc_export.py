from icalendar import Calendar as iCalendar, Event as iEvent, vText, vDatetime
import tempfile, os # being able to write a file
from cal.schema import Event as OurEvent
from cal import app
from time import strftime
from datetime import datetime

def query_events():
    events = OurEvent.query.all()
    return events

def create_calendar(events):
    # create Calendar object
    cal = iCalendar(dtstart = vDatetime(datetime.now()), # formats to .ics compatible datetime
	summary = 'Calendar for Columbia University made by ADI (adicu.com).')

    for e in events:    
        # for every event, create an event object
        vevent = iEvent(summary=e.name, organizer=e.user.name, 
                        location=vText(e.location), dtstart=vDatetime(e.start),
                        description=e.url)

        # add each event to calendar
        cal.add_component(vevent)

    return cal

def write_to_file(calendar_obj):
    filename = 'calendar_adi_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.ics'
    with open(filename, 'wb') as f_out:
    	f_out.write(calendar_obj.to_ical())

def main():
    events = query_events()
    our_cal = create_calendar(events)
    write_to_file(our_cal)    

    print 'Exported events to .isc file.'

with app.app_context():
    main()
