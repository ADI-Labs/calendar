import datetime as dt
from StringIO import StringIO

from celery import Celery

from flask import Flask, jsonify, render_template, request, send_file
import flask.ext.whooshalchemy as whooshalchemy

from cal.schema import db, Event, User  # noqa
from cal.fb import update_fb_events
from cal.isc import to_icalendar

# Initialize the app
app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)
whooshalchemy.whoosh_index(app, Event)

# Initialize celery
celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
TaskBase = celery.Task


class ContextTask(TaskBase):
    abstract = True

    def __call__(self, *args, **kwargs):
        with app.app_context():
            return TaskBase.__call__(self, *args, **kwargs)
celery.Task = ContextTask


# Background task
@celery.task(name="cal.fb_task")
def fb_task_test():
    app.logger.debug("Facebook Updater starting")
    update_fb_events()
    app.logger.debug("Facebook Updater finished")
    # Update every 30 minutes
    fb_task_test.apply_async(countdown=1800)


# Unfortunate hack, you will need to hit a url once to initialize the updater.
@app.before_first_request
def intiialize():
    app.logger.debug("Starting Facebook Updater")
    fb_task_test.apply_async()


@app.before_request
def before_request():
    """ Do something before every request """
    if request.path != '/favicon.ico':
        app.logger.info(request.path)
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
    return render_template('index.html')


@app.route("/events/<int:year>/<int:month>/<int:day>")
def events(year, month, day):

    search = request.args.get("search")
    if search is not None:
        events = Event.query.whoosh_search(search)
    else:
        events = Event.query

    start = dt.date(year, month, day)
    start -= dt.timedelta(days=start.isoweekday() % 7)  # Sunday 7 -> 0

    events = events.filter(start <= Event.start) \
                   .filter(Event.start < start + dt.timedelta(weeks=1))

    return jsonify(data=[event.to_json() for event in events.all()])


@app.route("/users/<int:year>/<int:month>/<int:day>")
def users(year, month, day):
    start = dt.date(year, month, day)
    start -= dt.timedelta(days=start.isoweekday() % 7)  # Sunday 7 -> 0
    one_week = dt.timedelta(weeks=1)

    events = Event.query.filter(Event.start >= start) \
                        .filter(Event.start < start + one_week)
    users = {event.user for event in events}    # use set to make users unique
    users = [user.to_json() for user in sorted(users, key=lambda u: u.name)]
    return jsonify(data=users)


@app.route("/isc/", methods=["GET"])
def to_isc():
    # get list of ids from GET request
    event_ids = request.args.getlist("event_ids[]", type=int)
    events = Event.query.filter(Event.id.in_(event_ids))

    return send_file(StringIO(to_icalendar(events)), mimetype="text/calendar",
                     as_attachment=True, attachment_filename="calendar.isc")
