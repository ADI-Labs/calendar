from __future__ import absolute_import
from datetime import tzinfo, timedelta, datetime, datetime, date, time

from cal.schema import db, User, Event
from bs4 import BeautifulSoup
import requests

import re

from icalendar import Calendar
from datetime import datetime


r = requests.get('http://engineering.columbia.edu/feeds/events')
text = r.text
soup = BeautifulSoup(text)

def update_engineering_events():
	events = soup.find_all('item')
	user = User.query.filter(User.name=="Columbia Engineering").first()
	for event in events:
		current_soup = BeautifulSoup(event.renderContents())

		event_name = current_soup.find('title').text
		url = current_soup.find('link').get_text() #event url
		url = url.encode('ascii','ignore')
		event_id = url[len(url) - 5: len(url)]

		url = "https://calendar.columbia.edu/sundial/webapi/iCalendar.php?EventID=" + event_id

		print url
		r_event = requests.get(url) 
		r_text = r_event.text #the individual html for each event
		individual_soup = BeautifulSoup(r_text)

		cal = Calendar.from_ical(individual_soup.get_text())

		for event in cal.walk('vevent'):
			date_start = event.get('dtstart')
			date_end = event.get('dtend')
			description = event.get('description')
			location = event.get('location')

		current_event = Event()

		current_event.start = date_start.dt
		current_event.end = date_end.dt
		current_event.description = description
		current_event.location = location
		current_event.name = event_name
		current_event.url = url
		current_event.user_id = user.id

		db.session.add(current_event)
	db.session.commit()

