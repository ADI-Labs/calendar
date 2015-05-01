from datetime import datetime

from icalendar import Calendar as iCalendar, Event as iEvent, vText, \
    vDatetime, vCalAddress


def to_icalendar(events):
    """ Converts events to .ics format
    :param events = Iterable(cal.schema.Event)
    :return bytes
    """
    summary = "Calendar for Columbia University made by ADI (adicu.com)"
    cal = iCalendar(dtstart=vDatetime(datetime.now()),
                    summary=summary)

    for e in events:
        # for every event, create an event object
        organizer = vCalAddress("MAILTO:''")
        organizer.params['cn'] = e.user.name
        vevent = iEvent(summary=e.name, organizer=organizer,
                        location=vText(e.location), dtstart=vDatetime(e.start),
                        description=e.url)

        cal.add_component(vevent)

    return cal.to_ical()
