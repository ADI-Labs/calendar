from flask import Flask, jsonify, render_template
from schema import db, Event,User
from cal.fb import update_fb_events
import flask.ext.whooshalchemy as whooshalchemy

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)
whooshalchemy.whoosh_index(app, Event)

@app.before_request
def before_request():
    """ Do something before every request """
    return


@app.after_request
def after_request(resp):
    """ Do something after every request """
    return resp


@app.errorhandler(404)
def page_not_found(e):
    return "Page not found"


@app.route('/')
def home():
    events = Event.query.order_by(Event.start).all()

    sunday_events = [event for event in events if event.start.weekday() == 0]
    monday_events = [event for event in events if event.start.weekday() == 1]
    tuesday_events = [event for event in events if event.start.weekday() == 2]
    wednesday_events = [event for event in events if event.start.weekday() == 3]
    thursday_events = [event for event in events if event.start.weekday() == 4]
    friday_events = [event for event in events if event.start.weekday() == 5]
    saturday_events = [event for event in events if event.start.weekday() == 6]

    events = [sunday_events, monday_events, tuesday_events, wednesday_events, thursday_events, friday_events, saturday_events]

    return render_template('index.html', events=events)
