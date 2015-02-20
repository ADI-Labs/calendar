from cal import app
from cal.schema import db, Event, User

from mixer.backend.flask import Mixer

mixer = Mixer(app, session_commit=True)

with app.app_context():
    db.create_all()

    # Uncomment if you want fake data.
    
    #mixer.init_app(app)

    #for i in xrange(5):
    #    user = mixer.blend(User)
    #
    #    for j in xrange(10):
    #        event = mixer.blend(Event, user=user)
