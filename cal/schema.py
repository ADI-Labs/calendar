import datetime as dt

from flask_sqlalchemy import BaseQuery
from fuzzywuzzy import process, fuzz
from pytz import timezone
from sqlalchemy_searchable import SearchQueryMixin, make_searchable
from sqlalchemy_utils.types import TSVectorType

from . import db

make_searchable()

class EventQuery(BaseQuery, SearchQueryMixin):
    pass

class Event(db.Model):
    query_class = EventQuery

    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=True)
    location = db.Column(db.String, nullable=True)
    url = db.Column(db.String, nullable=True)
    description = db.Column(db.Text, nullable=False)
    fb_id = db.Column(db.String, unique=True, nullable=True)
    sundial_id = db.Column(db.String, unique=True, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    search_vector = db.Column(TSVectorType('location', 'description', 'name'))

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
    def fuzzy_contains(event):
        """Checks if an event exists in the database.

        Searches by name and date range in case name or date is
        slightly different.

        :event Event - The event being checked
        :return Boolean - True if event exists in database, False otherwise
        """
        time_fuzz = dt.timedelta(days=3)

        query = (Event.start < event.start + time_fuzz) & \
                (Event.start > event.start - time_fuzz)
        if event.end is not None:
            query &= (Event.end is None) | \
                ((Event.end < event.end + time_fuzz) &
                 (Event.end > event.end + time_fuzz))

        # Search for good date matches.
        date_matches = Event.query.filter(query).all()

        # Filter for good name matches.
        res = [e for e in date_matches
               if fuzz.partial_ratio(e.name, event.name) >= 70]

        # Return None if no results come up.
        if not res:
            return None

        # Get best search result from the results.
        e = max(res, key=lambda e: (fuzz.partial_ratio(e.name, event.name),
                                    fuzz.ratio(e.name, event.name)))
        return e


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    fb_id = db.Column(db.String, unique=True, nullable=True)

    events = db.relationship("Event", backref="user")

    def to_json(self):
        return {"id": self.id, "name": self.name}

    @staticmethod
    def find_by_name(name):
        """Finds the best user match for a club name.

        Does fuzzy querying by name, and returns nothing
        if no good matches are found.

        :name str - The club name
        :returns User - if good match is found, None otherwise
        """
        group_names = [user.name for user in User.query.all()]
        result, score = process.extract(name, group_names, limit=1)[0]

        # Set search quality threshold (cutoff is arbitrary)
        if score < 50:
            return None
        else:
            return User.query.filter_by(name=result).first()
