
from datetime import datetime
from cal import app, db, Event

with app.app_context():
	current_event = Event()

	current_event.start = datetime(2002, 12, 25)
	current_event.end = datetime(2002, 12, 26)

	current_event.user_id = 29438666163
	current_event.description = 'event description'
	current_event.location = 'location'
	current_event.name = 'event title'
	current_event.url = 'https://calendar.columbia.edu/sundial/webapi/get.php?vt=detail&id=773'
    
	print current_event
	db.session.add(current_event)
	db.session.commit()


