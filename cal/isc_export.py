import sqlite3
from icalendar import Calendar, Event
import tempfile, os # being able to write a file

def main():
    cal = Calendar()
    cal['dtstart'] = '20050404T080000'
    cal['summary'] = 'Calendar for Columbia University.'

    event = Event()
    event['uid'] = '42'    

    cal.add_component(event)
    
    f = open('example.ics', 'wb')
    f.write(cal.to_ical())
    f.close()

    print cal

main()
