from datetime import datetime

from icalendar import Calendar as iCalendar, Event as iEvent, vText, vDatetime


def to_icalendar(events):
    """ Converts events to .isc format
    :param events = Iterable(cal.schema.Event)
    :return str
    """
    summary = "Calendar for Columbia University made by ADI (adicu.com)"
    cal = iCalendar(dtstart=vDatetime(datetime.now()),
                    summary=summary)

    for e in events:
        # for every event, create an event object
        vevent = iEvent(summary=e.name, organizer=e.user.name,
                        location=vText(e.location), dtstart=vDatetime(e.start),
                        description=e.url)

        cal.add_component(vevent)

    return cal.to_ical()
