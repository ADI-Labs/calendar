import datetime as dt

from flask import Flask, g, jsonify, render_template, json, request
import flask.ext.whooshalchemy as whooshalchemy


from cal.schema import db, Event, User
from cal.fb import update_fb_events
from celery import Celery

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
    return jsonify(error="Page not found")


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/events/")
def events():
    now = dt.datetime.now()
    events = Event.query.filter(Event.start > now).\
                         filter(Event.start < now + dt.timedelta(weeks=1))
    return jsonify(data=[event.to_json() for event in events.all()])


@app.route("/users/")
def users():
    now = dt.datetime.now()
    events = Event.query.filter(Event.start > now)\
        .filter(Event.start < now + dt.timedelta(weeks=1))

    users = {event.user for event in events}    # use set to make users unique
    return jsonify(data=[user.to_json() for user in users])
