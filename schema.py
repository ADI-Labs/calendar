from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Event(db.Model):
    __tablename__ = "event"

    id = db.Column(db.Integer, primary_key=True)

    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime)
    location = db.Column(db.String(64))
    url = db.Column(db.String(128), unique=True)
    name = db.Column(db.String(128))

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)

    events = db.relationship("Event", backref="user")
    # name = db.Column(db.String(64), unique=True)
    url = db.Column(db.String, unique=True)


if __name__ == "__main__":
    from run import app
    with app.app_context():
        db.create_all()
