from cal import app
from cal.schema import db, Event, User
from cal.fb.fb import update_events

with app.app_context():
    db.create_all()
    update_events()

