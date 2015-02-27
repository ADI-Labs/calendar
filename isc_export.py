from datetime import datetime

from icalendar import Calendar as iCalendar, Event as iEvent, vText, vDatetime

from cal.schema import Event as OurEvent
from cal import app


def query_events():
    events = OurEvent.query.all()
    return events


def create_calendar(events):
    # create Calendar object
    summary = "Calendar for Columbia University made by ADI (adicu.com)"
    cal = iCalendar(dtstart=vDatetime(datetime.now()),
                    summary=summary)

    for e in events:
        # for every event, create an event object
        vevent = iEvent(summary=e.name, organizer=e.user.name,
                        location=vText(e.location), dtstart=vDatetime(e.start),
                        description=e.url)

        cal.add_component(vevent)

    return cal


def write_to_file(calendar_obj):
    time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    fname = "calendar_adi_{}.ics".format(time)

    with open(fname, 'wb') as f_out:
        f_out.write(calendar_obj.to_ical())


def main():
    events = query_events()
    our_cal = create_calendar(events)
    write_to_file(our_cal)

    print 'Exported events to .isc file.'

if __name__ == "__main__":
    with app.app_context():
        main()
