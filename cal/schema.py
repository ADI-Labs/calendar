import datetime as dt

from flask.ext.sqlalchemy import SQLAlchemy
from pytz import timezone

db = SQLAlchemy()


class Event(db.Model):
    __tablename__ = "event"
    __searchable__ = ['location', 'name']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime)
    location = db.Column(db.String(64))
    url = db.Column(db.String(128), unique=True)
    description = db.Column(db.Text)

    source = db.Column(db.Enum("facebook"), nullable=False)
    source_id = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def to_json(self):
        eastern = timezone('US/Eastern')
        end_time = self.end
        if end_time:
            end_time = eastern.localize(end_time).isoformat()
        return {
            "id": self.id,
            "start": eastern.localize(self.start).isoformat(),
            "end": end_time,
            "location": self.location,
            "url": self.url,
            "name": self.name,
            "user_id": self.user_id
        }

    @staticmethod
    def fuzzy_match(event):
        tfuzz = dt.timedelta(days=1)

        start_match = (Event.start > event.start - tfuzz) & \
                      (Event.start < event.start + tfuzz)
        end_match = (Event.end is None) | ((Event.end > event.end - tfuzz) &
                                            Event.end < event.end + tfuzz)
        name_match = (Event.name == event.name) # TODO fuzzy string match

        return Event.query.filter(start_match & end_match & name_match) \
                          .filter(Event.id != event.id)
    @staticmethod
    def fuzzy_contains(event):
        query = Event.fuzzy_match(event)
        return query.first() is not None


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

    events = db.relationship("Event", backref="user")

    def to_json(self):
        return {"id": self.id, "name": self.name}
