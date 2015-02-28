from flask.ext.sqlalchemy import SQLAlchemy
import flask.ext.whooshalchemy as whooshalchemy
from pytz import timezone

db = SQLAlchemy()


class Event(db.Model):
    __tablename__ = "event"
    __searchable__ = ['location', 'name']

    id = db.Column(db.Integer, primary_key=True)

    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime)
    location = db.Column(db.String(64))
    url = db.Column(db.String(128), unique=True)
    name = db.Column(db.String(128), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def to_JSON(self):
        eastern = timezone('EST')
        end_time = self.end
        if end_time:
            end_time = end_time.replace(tzinfo=eastern).isoformat()
        return {
            "id": self.id,
            "start": self.start.replace(tzinfo=eastern).isoformat(),
            "end": end_time,
            "location": self.location,
            "url": self.url,
            "name": self.name,
            "user_id": self.user_id
        }


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

    events = db.relationship("Event", backref="user")
